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

        # Calculate NDVI change
        potential_growth = self.growth_rate
        actual_growth = potential_growth * overall_stress

        # Limit by max NDVI
        new_ndvi = min(self.ndvi + actual_growth, self.max_ndvi)

        # Decline if severe stress
        if overall_stress < 0.3:
            decline = (0.3 - overall_stress) * 0.05
            new_ndvi = max(0.1, self.ndvi - decline)

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
        """Calculate water stress factor (0-1)"""
        if moisture >= self.optimal_moisture:
            # Slight stress if too wet
            excess = moisture - self.optimal_moisture
            return max(0.7, 1 - (excess / 100))
        else:
            # Stress increases as moisture drops
            deficit = self.optimal_moisture - moisture
            return max(0, 1 - (deficit / self.optimal_moisture) * 2)

    def _calculate_nutrient_stress(self, nitrogen):
        """Calculate nutrient stress factor (0-1)"""
        optimal_nitrogen = self.nitrogen_need / 12  # Per week
        if nitrogen >= optimal_nitrogen:
            return 1.0
        else:
            return max(0.3, nitrogen / optimal_nitrogen)

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
