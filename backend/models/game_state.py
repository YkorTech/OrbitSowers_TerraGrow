"""
GameState model for TerraGrow Academy
Orchestrates the entire game simulation
"""

import random
from .crop import Crop
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
        irrigation_cost = irrigation_mm * 3.5  # From config
        fertilizer_cost = fertilizer_kg * 1.2  # From config
        total_cost = irrigation_cost + fertilizer_cost

        # Check budget
        if total_cost > self.budget:
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

        # Extract nutrients (crop uptake)
        crop_uptake = self.crop.nitrogen_need / 12  # Weekly uptake
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

        # Advance week
        self.current_week += 1

        # Generate feedback messages
        messages = self._generate_feedback(growth_info, moisture_info, event)

        return {
            'week': self.current_week - 1,
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
            'is_complete': self.current_week > self.max_weeks
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
                'name': 'Sécheresse',
                'description': 'Pas de pluie prévue. Humidité sol critique.',
                'icon': '🌵',
                'effect': 'Besoin irrigation urgente'
            },
            'heavy_rain': {
                'name': 'Pluies torrentielles',
                'description': 'Fortes pluies ! Risque lessivage nutriments.',
                'icon': '☔',
                'effect': 'Drainage sol important'
            },
            'heatwave': {
                'name': 'Canicule',
                'description': f'Température extrême {weather_data.get("temperature", 35)}°C !',
                'icon': '🌡️',
                'effect': 'Stress thermique élevé'
            },
            'frost': {
                'name': 'Gel tardif',
                'description': f'Alerte gel ! Température {weather_data.get("temperature", 2)}°C',
                'icon': '❄️',
                'effect': 'Dommages culture possible'
            },
            'cold_snap': {
                'name': 'Vague de froid',
                'description': 'Températures basses prolongées',
                'icon': '🥶',
                'effect': 'Croissance ralentie'
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
                'text': f"✅ Culture saine ! NDVI {growth_info['ndvi']:.2f}"
            })
        elif growth_info['health'] == 'stressed':
            messages.append({
                'type': 'warning',
                'text': f"⚠️ Culture stressée. NDVI {growth_info['ndvi']:.2f}"
            })
        else:
            messages.append({
                'type': 'danger',
                'text': f"🚨 Culture critique ! NDVI {growth_info['ndvi']:.2f}"
            })

        # Moisture feedback
        if moisture_info['status'] == 'critical':
            messages.append({
                'type': 'danger',
                'text': f"💧 Humidité critique {moisture_info['moisture']:.1f}% ! Irriguer urgent"
            })
        elif moisture_info['status'] == 'low':
            messages.append({
                'type': 'warning',
                'text': f"💧 Humidité basse {moisture_info['moisture']:.1f}%"
            })

        # Drainage warning
        if moisture_info.get('drainage', 0) > 10:
            messages.append({
                'type': 'info',
                'text': f"⚠️ Lessivage nutriments : {moisture_info.get('nitrogen_leached', 0):.1f} kg N/ha"
            })

        # Event message
        if event:
            messages.append({
                'type': 'event',
                'text': f"{event['icon']} {event['name']} : {event['description']}"
            })

        return messages

    def calculate_final_score(self):
        """
        Calculate final score and statistics

        Returns:
            dict: Final scores and recommendations
        """
        # Yield
        crop_yield = self.crop.get_yield()

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
                'text': f"✅ Excellent maintien NDVI moyen {avg_ndvi:.2f} !"
            })
        elif avg_ndvi < 0.5:
            recs.append({
                'type': 'warning',
                'text': f"⚠️ NDVI moyen faible {avg_ndvi:.2f}. Augmenter irrigation et fertilisation."
            })

        # Water usage
        if self.total_water_used < 300:
            recs.append({
                'type': 'info',
                'text': f"💡 Utilisation eau économe ({self.total_water_used:.0f}mm). Bon pour durabilité !"
            })
        elif self.total_water_used > 600:
            recs.append({
                'type': 'warning',
                'text': f"⚠️ Consommation eau élevée ({self.total_water_used:.0f}mm). Optimiser irrigation."
            })

        # Region-specific advice
        climate = self.region.climate.lower()
        if 'tropical' in climate:
            recs.append({
                'type': 'info',
                'text': f"💡 Conseil {self.region.name}: Drainage crucial en saison pluies pour éviter lessivage."
            })
        elif 'sahel' in climate or 'arid' in climate:
            recs.append({
                'type': 'info',
                'text': f"💡 Conseil {self.region.name}: Réserves eau essentielles. Planifier irrigation stricte."
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
