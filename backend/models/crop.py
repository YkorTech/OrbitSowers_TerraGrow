"""
Crop model for TerraGrow Academy
Handles crop growth, NDVI calculation, and stress factors
"""

import math


class Crop:
    """Represents a crop in the game"""

    def __init__(self, crop_type, parameters):
        """
        Initialize crop

        Args:
            crop_type (str): Type of crop (maize, sorghum, wheat)
            parameters (dict): Crop parameters from config
        """
        self.type = crop_type
        self.name = parameters['name']
        self.optimal_temp = parameters['optimal_temp']
        self.optimal_moisture = parameters['optimal_moisture']
        self.water_need = parameters['water_need']
        self.nitrogen_need = parameters['nitrogen_need']
        self.growth_rate = parameters['growth_rate']
        self.max_ndvi = parameters['max_ndvi']

        # Current state
        self.ndvi = parameters['initial_ndvi']
        self.age_weeks = 0

        # Stress tracking for realistic decline
        self.consecutive_stress_weeks = 0
        self.total_stress_accumulated = 0

    def calculate_growth(self, moisture, nitrogen, temperature):
        """
        Calculate crop growth based on environmental conditions

        Args:
            moisture (float): Current soil moisture (%)
            nitrogen (float): Available nitrogen (kg/ha)
            temperature (float): Current temperature (°C)

        Returns:
            dict: Growth info including NDVI change and stress factors
        """
        # Calculate stress factors (0 = max stress, 1 = no stress)
        water_stress = self._calculate_water_stress(moisture)
        nutrient_stress = self._calculate_nutrient_stress(nitrogen)
        thermal_stress = self._calculate_thermal_stress(temperature)

        # Overall stress (multiplicative effect)
        overall_stress = water_stress * nutrient_stress * thermal_stress

        # Track stress history
        if overall_stress < 0.5:
            self.consecutive_stress_weeks += 1
            self.total_stress_accumulated += (0.5 - overall_stress)
        else:
            self.consecutive_stress_weeks = 0  # Reset if conditions improve

        # Calculate NDVI change
        potential_growth = self.growth_rate
        actual_growth = potential_growth * overall_stress

        # Apply growth first
        new_ndvi = min(self.ndvi + actual_growth, self.max_ndvi)

        # CRITICAL DECLINE SYSTEM
        decline = 0

        # 1. Severe acute stress (this week)
        if overall_stress < 0.2:
            # Critical stress → immediate decline
            decline += 0.08  # -0.08 NDVI per week in critical state

        elif overall_stress < 0.4:
            # Severe stress → moderate decline
            decline += 0.04  # -0.04 NDVI per week

        # 2. Chronic stress (consecutive weeks of stress)
        if self.consecutive_stress_weeks >= 3:
            # After 3 weeks of stress, accelerated decline
            chronic_penalty = (self.consecutive_stress_weeks - 2) * 0.02
            decline += min(chronic_penalty, 0.1)  # Cap at 0.1

        # 3. Cumulative stress damage
        if self.total_stress_accumulated > 2.0:
            # Long-term damage from accumulated stress
            accumulated_penalty = (self.total_stress_accumulated - 2.0) * 0.01
            decline += min(accumulated_penalty, 0.05)

        # Apply decline
        if decline > 0:
            new_ndvi = max(0.05, self.ndvi - decline)  # ✅ Can drop to near-death

        # Natural aging decline in late stage (weeks 10-12)
        if self.age_weeks >= 10 and overall_stress < 0.7:
            aging_decline = 0.02
            new_ndvi = max(0.1, new_ndvi - aging_decline)

        self.ndvi = new_ndvi
        self.age_weeks += 1

        return {
            'ndvi': self.ndvi,
            'growth': actual_growth,
            'water_stress': water_stress,
            'nutrient_stress': nutrient_stress,
            'thermal_stress': thermal_stress,
            'overall_stress': overall_stress,
            'health': self._get_health_status()
        }

    def _calculate_water_stress(self, moisture):
        """
        Calculate water stress factor (0-1)

        Realistic water stress curve:
        - Optimal range: 80-120% of optimal_moisture → stress = 1.0
        - Too dry: rapid decline below optimal
        - Too wet: waterlogging stress above 85%
        """
        # Optimal range (±20% of optimal)
        optimal_low = self.optimal_moisture * 0.8
        optimal_high = self.optimal_moisture * 1.2

        if optimal_low <= moisture <= optimal_high:
            # Perfect conditions
            return 1.0
        elif moisture > optimal_high:
            # WATERLOGGING stress (excess water)
            # Above 85% moisture = waterlogging risk
            if moisture > 85:
                excess_severity = (moisture - 85) / 15  # 0-1 scale
                return max(0.3, 1 - (excess_severity * 0.7))  # ✅ Severe penalty
            else:
                excess = moisture - optimal_high
                return max(0.7, 1 - (excess / 50))
        else:
            # DROUGHT stress (insufficient water)
            deficit = optimal_low - moisture
            deficit_ratio = deficit / self.optimal_moisture

            if moisture < 25:  # Wilting point
                return 0.0  # ✅ Complete stress below wilting point
            elif deficit_ratio > 0.5:  # Very dry
                return max(0.1, 1 - deficit_ratio * 1.5)
            else:
                return max(0.3, 1 - deficit_ratio * 1.2)

    def _calculate_nutrient_stress(self, nitrogen):
        """
        Calculate nutrient stress factor (0-1)

        CRITICAL: Without nitrogen, crops CANNOT grow
        """
        optimal_nitrogen = self.nitrogen_need / 12  # Per week

        if nitrogen >= optimal_nitrogen:
            return 1.0
        elif nitrogen <= 0:
            return 0.0  # ✅ NO growth without nitrogen
        else:
            # Linear decline: nitrogen/optimal
            # At 50% nitrogen → 50% stress
            # At 10% nitrogen → 10% stress (severe)
            return nitrogen / optimal_nitrogen

    def _calculate_thermal_stress(self, temperature):
        """Calculate thermal stress factor (0-1)"""
        temp_diff = abs(temperature - self.optimal_temp)

        if temp_diff <= 5:
            return 1.0
        elif temp_diff <= 10:
            return 0.7
        elif temp_diff <= 15:
            return 0.4
        else:
            return 0.1

    def _get_health_status(self):
        """Get crop health status based on NDVI"""
        if self.ndvi >= 0.6:
            return 'healthy'
        elif self.ndvi >= 0.4:
            return 'stressed'
        else:
            return 'critical'

    def get_yield(self):
        """
        Calculate final yield based on NDVI history

        Returns:
            float: Yield in tonnes/ha
        """
        # Simplified yield calculation
        # Assumes max yield of 8 t/ha for NDVI = 0.85
        max_yield = 8.0
        yield_efficiency = self.ndvi / self.max_ndvi
        return max_yield * yield_efficiency

    def to_dict(self):
        """Export crop state as dictionary"""
        return {
            'type': self.type,
            'name': self.name,
            'ndvi': round(self.ndvi, 3),
            'age_weeks': self.age_weeks,
            'health': self._get_health_status()
        }
