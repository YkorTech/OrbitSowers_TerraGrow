"""
GameState model for TerraGrow Academy
Orchestrates the entire game simulation
"""

import random
from .crop_v2 import Crop  # Using V2 with phenological stages
from .soil import Soil
from .region import Region


class GameState:
    """Manages the overall game state and simulation"""

    def __init__(self, region, crop_type, crop_params, soil_params, initial_budget=2000):
        """
        Initialize game state

        Args:
            region (Region): Region object
            crop_type (str): Type of crop to grow
            crop_params (dict): Crop parameters
            soil_params (dict): Soil parameters
            initial_budget (float): Starting budget (USD)
        """
        self.region = region
        self.crop = Crop(crop_type, crop_params)
        self.soil = Soil(region.soil_type, soil_params)

        self.current_week = 1
        self.max_weeks = 12
        self.budget = initial_budget
        self.total_water_used = 0
        self.total_nitrogen_used = 0

        # History tracking
        self.ndvi_history = [self.crop.ndvi]
        self.moisture_history = [self.soil.moisture]
        self.events_history = []

        # Emergency loan system
        self.loan_taken = False
        self.loan_amount = 0
        self.loan_week = None

        # Weather data (to be filled by API)
        self.weather_data = []

    def simulate_week(self, irrigation_mm, fertilizer_kg, weather_data):
        """
        Simulate one week of farming

        Args:
            irrigation_mm (float): Irrigation applied (mm)
            fertilizer_kg (float): Fertilizer applied (kg N/ha)
            weather_data (dict): Weather data for the week

        Returns:
            dict: Week simulation results
        """
        # Extract weather
        rain = weather_data.get('precipitation', 0)
        temperature = weather_data.get('temperature', 25)
        et = weather_data.get('evapotranspiration', 25)

        # Apply irrigation and fertilizer
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from config import Config

        irrigation_cost = irrigation_mm * Config.IRRIGATION_COST_PER_MM
        fertilizer_cost = fertilizer_kg * Config.FERTILIZER_COST_PER_KG
        total_cost = irrigation_cost + fertilizer_cost

        # Emergency loan system
        loan_offered = False
        if total_cost > self.budget and self.current_week >= 8 and not self.loan_taken:
            # Offer emergency loan
            loan_offered = True
            loan_info = {
                'loan_offered': True,
                'loan_amount': 500,
                'interest_rate': 0.20,
                'repayment': 600,
                'message': 'Budget critique! Pret d\'urgence disponible: $500 (remboursement $600 avec interet 20%)'
            }

        # Check budget
        if total_cost > self.budget:
            if loan_offered:
                # Return error with loan option
                return {
                    'error': 'Insufficient budget',
                    'required': total_cost,
                    'available': self.budget,
                    'loan_option': loan_info
                }
            else:
                return {
                    'error': 'Insufficient budget',
                    'required': total_cost,
                    'available': self.budget
                }

        # Deduct costs
        self.budget -= total_cost
        self.total_water_used += irrigation_mm
        self.total_nitrogen_used += fertilizer_kg

        # Add fertilizer to soil
        fertilizer_info = self.soil.add_fertilizer(fertilizer_kg)

        # Update soil moisture
        moisture_info = self.soil.update_moisture(rain, irrigation_mm, et)

        # Extract nutrients (crop uptake based on phenological stage)
        crop_uptake = self.crop.get_nitrogen_requirement()  # Dynamic uptake by growth stage
        self.soil.extract_nutrients(crop_uptake)

        # Calculate crop growth
        growth_info = self.crop.calculate_growth(
            self.soil.moisture,
            self.soil.nitrogen,
            temperature
        )

        # Check for random events
        event = self._check_random_event(weather_data)
        if event:
            self.events_history.append({
                'week': self.current_week,
                'event': event
            })

        # Update history
        self.ndvi_history.append(self.crop.ndvi)
        self.moisture_history.append(self.soil.moisture)

        # Generate feedback messages
        messages = self._generate_feedback(growth_info, moisture_info, event)

        # Check if this is the last week BEFORE incrementing
        week_just_played = self.current_week
        is_final_week = (week_just_played == self.max_weeks)

        # Advance week AFTER checking
        self.current_week += 1

        return {
            'week': self.current_week,  # Return NEXT week to play (for UI consistency)
            'week_played': week_just_played,  # Also include week that was just played (for reference)
            'budget': round(self.budget, 2),
            'crop': self.crop.to_dict(),
            'soil': self.soil.to_dict(),
            'costs': {
                'irrigation': round(irrigation_cost, 2),
                'fertilizer': round(fertilizer_cost, 2),
                'total': round(total_cost, 2)
            },
            'weather': {
                'rain': rain,
                'temperature': temperature,
                'et': et
            },
            'event': event,
            'messages': messages,
            'is_complete': is_final_week  # True only AFTER playing week 12
        }

    def _check_random_event(self, weather_data):
        """
        Check for random events based on climate and weather

        Args:
            weather_data (dict): Current weather data

        Returns:
            dict or None: Event information
        """
        # Low probability of events
        if random.random() > 0.15:
            return None

        climate_chars = self.region.get_climate_characteristics()
        possible_events = climate_chars['typical_events']

        event_type = random.choice(possible_events)

        events_config = {
            'drought': {
                'name': 'Drought',
                'description': 'No rain forecast. Critical soil moisture.',
                'icon': '🌵',
                'effect': 'Urgent irrigation needed'
            },
            'heavy_rain': {
                'name': 'Heavy rain',
                'description': 'Torrential rain! Risk of nutrient leaching.',
                'icon': '☔',
                'effect': 'Significant soil drainage'
            },
            'heatwave': {
                'name': 'Heatwave',
                'description': f'Extreme temperature {weather_data.get("temperature", 35)}°C!',
                'icon': '🌡️',
                'effect': 'High thermal stress'
            },
            'frost': {
                'name': 'Late frost',
                'description': f'Frost alert! Temperature {weather_data.get("temperature", 2)}°C',
                'icon': '❄️',
                'effect': 'Possible crop damage'
            },
            'cold_snap': {
                'name': 'Cold snap',
                'description': 'Prolonged low temperatures',
                'icon': '🥶',
                'effect': 'Slowed growth'
            }
        }

        return events_config.get(event_type, None)

    def _generate_feedback(self, growth_info, moisture_info, event):
        """
        Generate feedback messages for the player

        Args:
            growth_info (dict): Crop growth info
            moisture_info (dict): Soil moisture info
            event (dict): Event info if any

        Returns:
            list: Feedback messages
        """
        messages = []

        # NDVI feedback
        if growth_info['health'] == 'healthy':
            messages.append({
                'type': 'success',
                'text': f"✅ Healthy crop! NDVI {growth_info['ndvi']:.2f}"
            })
        elif growth_info['health'] == 'stressed':
            messages.append({
                'type': 'warning',
                'text': f"⚠️ Crop stressed. NDVI {growth_info['ndvi']:.2f}"
            })
        else:
            messages.append({
                'type': 'danger',
                'text': f"🚨 Critical crop! NDVI {growth_info['ndvi']:.2f}"
            })

        # Moisture feedback
        if moisture_info['status'] == 'critical':
            messages.append({
                'type': 'danger',
                'text': f"💧 Critical moisture {moisture_info['moisture']:.1f}%! Urgent irrigation needed"
            })
        elif moisture_info['status'] == 'low':
            messages.append({
                'type': 'warning',
                'text': f"💧 Low moisture {moisture_info['moisture']:.1f}%"
            })

        # Drainage warning
        if moisture_info.get('drainage', 0) > 10:
            messages.append({
                'type': 'info',
                'text': f"⚠️ Nutrient leaching: {moisture_info.get('nitrogen_leached', 0):.1f} kg N/ha"
            })

        # Event message
        if event:
            messages.append({
                'type': 'event',
                'text': f"{event['icon']} {event['name']} : {event['description']}"
            })

        # Smart recommendations (contextual)
        smart_recs = self._generate_smart_recommendations(growth_info)
        messages.extend(smart_recs)

        return messages

    def _generate_smart_recommendations(self, growth_info):
        """
        Generate smart contextual recommendations based on region, week, budget, and crop stage

        Args:
            growth_info (dict): Current crop growth information

        Returns:
            list: Smart recommendation messages
        """
        recommendations = []
        climate = self.region.climate.lower()
        stage = growth_info.get('stage', '')
        nitrogen_req = growth_info.get('nitrogen_requirement', 0)

        # Week 1-3: Initial guidance for region type
        if self.current_week <= 3:
            if 'sahel' in climate or 'arid' in climate:
                recommendations.append({
                    'type': 'tip',
                    'text': f"💡 Region aride detectee! Irrigation minimum: 30mm/semaine recommandee. Budget projete 12 sem: ~$900"
                })
            elif 'tropical' in climate or 'humide' in climate:
                recommendations.append({
                    'type': 'tip',
                    'text': f"💡 Region humide! Peu d'irrigation necessaire. Focus sur drainage et fertilisation optimale."
                })

        # Phenological stage guidance (weeks 4-7: vegetative peak)
        if 4 <= self.current_week <= 7:
            if stage == 'Vegetative':
                recommendations.append({
                    'type': 'tip',
                    'text': f"🌱 Stade vegetatif (PIC azote): Besoin {nitrogen_req:.1f} kg N/ha cette semaine. C'est le moment d'investir!"
                })

        # Budget warnings
        if self.budget < 300 and self.current_week < 10:
            weeks_left = self.max_weeks - self.current_week + 1
            budget_per_week = self.budget / weeks_left if weeks_left > 0 else 0
            recommendations.append({
                'type': 'warning',
                'text': f"⚠️ Budget critique: ${self.budget:.0f} pour {weeks_left} semaines (${budget_per_week:.0f}/sem). Reduire irrigation!"
            })
        elif self.budget < 500 and self.current_week < 8:
            recommendations.append({
                'type': 'warning',
                'text': f"⚠️ Budget faible: ${self.budget:.0f}. Optimiser depenses irrigation/fertilisation."
            })

        # Loan availability reminder
        if self.budget < 200 and self.current_week >= 8 and not self.loan_taken:
            recommendations.append({
                'type': 'info',
                'text': f"💰 Pret d'urgence disponible: $500 (remboursement $600). Peut vous sauver la recolte!"
            })

        # Chronic stress warning
        if growth_info.get('consecutive_stress', 0) >= 2:
            recommendations.append({
                'type': 'danger',
                'text': f"🚨 Stress chronique ({growth_info['consecutive_stress']} sem)! Augmenter irrigation ET fertilisation MAINTENANT."
            })

        # Late game guidance (maturation)
        if self.current_week >= 11:
            if stage == 'Maturation':
                recommendations.append({
                    'type': 'info',
                    'text': f"🌾 Maturation: Besoins reduits ({nitrogen_req:.1f} kg N/ha). Economiser pour maximiser profit."
                })

        return recommendations

    def calculate_final_score(self):
        """
        Calculate final score and statistics

        Returns:
            dict: Final scores and recommendations
        """
        # Yield
        crop_yield = self.crop.get_yield()

        # Economic calculations
        revenue = self.crop.get_revenue()  # Uses price_per_ton from config
        total_costs = 2000 - self.budget  # Initial budget - remaining

        # Deduct loan repayment if taken
        loan_repayment = 0
        if self.loan_taken:
            loan_repayment = self.loan_amount * 1.20  # 20% interest

        profit = revenue - total_costs - loan_repayment

        # Water efficiency (kg yield per m³ water)
        water_efficiency = crop_yield / (self.total_water_used / 100) if self.total_water_used > 0 else 0

        # Nitrogen efficiency
        nitrogen_efficiency = min(100, (crop_yield / self.total_nitrogen_used * 50)) if self.total_nitrogen_used > 0 else 0

        # Sustainability score (0-100)
        sustainability = (
            nitrogen_efficiency * 0.4 +
            min(100, water_efficiency * 20) * 0.4 +
            (self.budget / 2000 * 100) * 0.2
        )

        # Overall rating (stars)
        stars = self._calculate_stars(crop_yield, sustainability)

        # Regional comparison
        regional_avg = self._get_regional_average()

        # Recommendations
        recommendations = self._generate_recommendations()

        return {
            'yield': round(crop_yield, 2),
            'yield_unit': 't/ha',
            'regional_avg': regional_avg,
            'yield_diff': round(((crop_yield / regional_avg) - 1) * 100, 1),
            'revenue': round(revenue, 2),
            'total_costs': round(total_costs, 2),
            'loan_taken': self.loan_taken,
            'loan_repayment': round(loan_repayment, 2) if self.loan_taken else 0,
            'profit': round(profit, 2),
            'sustainability_score': round(sustainability, 1),
            'water_efficiency': round(water_efficiency, 2),
            'nitrogen_efficiency': round(nitrogen_efficiency, 1),
            'stars': stars,
            'budget_remaining': round(self.budget, 2),
            'recommendations': recommendations,
            'ndvi_history': [round(x, 3) for x in self.ndvi_history]
        }

    def _calculate_stars(self, crop_yield, sustainability):
        """Calculate star rating (1-5)"""
        combined_score = (crop_yield / 8.0 * 50) + (sustainability / 100 * 50)

        if combined_score >= 80:
            return 5
        elif combined_score >= 65:
            return 4
        elif combined_score >= 50:
            return 3
        elif combined_score >= 35:
            return 2
        else:
            return 1

    def _get_regional_average(self):
        """Get regional average yield"""
        # Simplified regional averages
        climate = self.region.climate.lower()

        if 'tropical' in climate:
            return 5.2
        elif 'sahel' in climate or 'arid' in climate:
            return 3.8
        elif 'continental' in climate:
            return 6.5
        else:
            return 5.5

    def _generate_recommendations(self):
        """Generate personalized recommendations"""
        recs = []

        # Analyze NDVI trend
        avg_ndvi = sum(self.ndvi_history) / len(self.ndvi_history)
        if avg_ndvi >= 0.65:
            recs.append({
                'type': 'success',
                'text': f"✅ Excellent! Average NDVI {avg_ndvi:.2f}"
            })
        elif avg_ndvi < 0.5:
            recs.append({
                'type': 'warning',
                'text': f"⚠️ Low average NDVI {avg_ndvi:.2f}. Increase irrigation and fertilization."
            })

        # Water usage
        if self.total_water_used < 300:
            recs.append({
                'type': 'info',
                'text': f"💡 Economical water use ({self.total_water_used:.0f}mm). Great for sustainability!"
            })
        elif self.total_water_used > 600:
            recs.append({
                'type': 'warning',
                'text': f"⚠️ High water consumption ({self.total_water_used:.0f}mm). Optimize irrigation."
            })

        # Region-specific advice
        climate = self.region.climate.lower()
        if 'tropical' in climate:
            recs.append({
                'type': 'info',
                'text': f"💡 Tip for {self.region.name}: Drainage is crucial during rainy season to avoid leaching."
            })
        elif 'sahel' in climate or 'arid' in climate:
            recs.append({
                'type': 'info',
                'text': f"💡 Tip for {self.region.name}: Water reserves are essential. Plan strict irrigation."
            })

        return recs

    def to_dict(self):
        """Export complete game state"""
        return {
            'region': self.region.to_dict(),
            'crop': self.crop.to_dict(),
            'soil': self.soil.to_dict(),
            'week': self.current_week,
            'max_weeks': self.max_weeks,
            'budget': round(self.budget, 2),
            'ndvi_history': [round(x, 3) for x in self.ndvi_history],
            'events': self.events_history
        }
