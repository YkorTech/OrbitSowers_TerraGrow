"""
Crop model V2 for TerraGrow Academy
Improved realistic growth logic with:
- Crop-specific drought/waterlog tolerance
- Progressive nitrogen needs by growth stage
- Educational feedback
"""

import math


class Crop:
    """Represents a crop with realistic growth behavior"""

    def __init__(self, crop_type, parameters):
        """
        Initialize crop

        Args:
            crop_type (str): Type of crop
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

        # New V2 parameters
        self.drought_tolerance = parameters.get('drought_tolerance', 'medium')
        self.waterlog_tolerance = parameters.get('waterlog_tolerance', 'medium')
        self.nitrogen_curve = parameters.get('nitrogen_curve', [0.20, 0.50, 0.25, 0.05])
        self.price_per_ton = parameters.get('price_per_ton', 250)

        # Current state
        self.ndvi = parameters['initial_ndvi']
        self.age_weeks = 0

        # Stress tracking
        self.consecutive_stress_weeks = 0
        self.total_stress_accumulated = 0

        # Growth stages
        self.growth_stages = ['Germination', 'Vegetative', 'Flowering', 'Maturation']
        self.stage_weeks = [3, 4, 3, 2]  # Weeks per stage

    def get_growth_stage(self):
        """Get current growth stage"""
        cumulative = 0
        for i, weeks in enumerate(self.stage_weeks):
            cumulative += weeks
            if self.age_weeks < cumulative:
                return i, self.growth_stages[i]
        return 3, self.growth_stages[3]

    def get_nitrogen_requirement(self):
        """
        Get nitrogen requirement for current week based on growth stage

        Returns:
            float: kg N/ha needed this week
        """
        stage_idx, stage_name = self.get_growth_stage()

        # Get percentage for this stage
        stage_percentage = self.nitrogen_curve[stage_idx]

        # Calculate weeks in this stage
        stage_duration = self.stage_weeks[stage_idx]

        # Weekly requirement
        weekly_need = (self.nitrogen_need * stage_percentage) / stage_duration

        return weekly_need

    def calculate_growth(self, moisture, nitrogen, temperature):
        """
        Calculate crop growth based on environmental conditions

        Args:
            moisture (float): Current soil moisture (%)
            nitrogen (float): Available nitrogen (kg/ha)
            temperature (float): Current temperature (°C)

        Returns:
            dict: Growth info with educational feedback
        """
        # Calculate stress factors
        water_stress = self._calculate_water_stress(moisture)
        nutrient_stress = self._calculate_nutrient_stress(nitrogen)
        thermal_stress = self._calculate_thermal_stress(temperature)

        # Overall stress (multiplicative)
        overall_stress = water_stress * nutrient_stress * thermal_stress

        # Track stress history
        if overall_stress < 0.5:
            self.consecutive_stress_weeks += 1
            self.total_stress_accumulated += (0.5 - overall_stress)
        else:
            self.consecutive_stress_weeks = max(0, self.consecutive_stress_weeks - 1)

        # Calculate potential growth
        potential_growth = self.growth_rate * overall_stress

        # Apply growth
        new_ndvi = min(self.ndvi + potential_growth, self.max_ndvi)

        # DECLINE system for chronic stress
        decline = 0

        if overall_stress < 0.2:
            # Critical acute stress
            decline = 0.06
        elif overall_stress < 0.4:
            # Severe stress
            decline = 0.03

        # Chronic stress penalty
        if self.consecutive_stress_weeks >= 3:
            chronic_penalty = (self.consecutive_stress_weeks - 2) * 0.015
            decline += min(chronic_penalty, 0.08)

        # Apply decline
        if decline > 0:
            new_ndvi = max(0.05, self.ndvi - decline)

        # Update state
        self.ndvi = new_ndvi
        self.age_weeks += 1

        # Get current stage
        stage_idx, stage_name = self.get_growth_stage()

        return {
            'ndvi': self.ndvi,
            'growth': potential_growth,
            'decline': decline,
            'water_stress': water_stress,
            'nutrient_stress': nutrient_stress,
            'thermal_stress': thermal_stress,
            'overall_stress': overall_stress,
            'health': self._get_health_status(),
            'stage': stage_name,
            'stage_idx': stage_idx,
            'consecutive_stress': self.consecutive_stress_weeks,
            'nitrogen_requirement': self.get_nitrogen_requirement()
        }

    def _calculate_water_stress(self, moisture):
        """
        Calculate water stress with crop-specific tolerance

        Args:
            moisture (float): Current soil moisture (%)

        Returns:
            float: Stress factor 0-1 (1 = no stress)
        """
        # Tolerance ranges
        tolerance_ranges = {
            'high': 0.35,    # ±35% of optimal
            'medium': 0.25,  # ±25%
            'low': 0.15      # ±15%
        }

        drought_range = tolerance_ranges[self.drought_tolerance]
        waterlog_range = tolerance_ranges[self.waterlog_tolerance]

        optimal_min = self.optimal_moisture * (1 - drought_range)
        optimal_max = self.optimal_moisture * (1 + waterlog_range)

        if optimal_min <= moisture <= optimal_max:
            return 1.0  # Perfect conditions

        elif moisture < optimal_min:
            # DROUGHT stress
            deficit_ratio = (optimal_min - moisture) / optimal_min

            if moisture < 25:  # Wilting point
                return 0.0

            # Stress curve based on tolerance
            if self.drought_tolerance == 'high':
                return max(0.3, 1 - deficit_ratio * 0.8)
            elif self.drought_tolerance == 'medium':
                return max(0.2, 1 - deficit_ratio * 1.2)
            else:  # low
                return max(0.1, 1 - deficit_ratio * 1.5)

        else:
            # WATERLOGGING stress
            excess_ratio = (moisture - optimal_max) / (100 - optimal_max)

            if self.waterlog_tolerance == 'high':  # Rice
                return max(0.7, 1 - excess_ratio * 0.3)
            elif self.waterlog_tolerance == 'medium':
                return max(0.4, 1 - excess_ratio * 0.6)
            else:  # low
                return max(0.2, 1 - excess_ratio * 0.9)

    def _calculate_nutrient_stress(self, nitrogen):
        """
        Calculate nutrient stress based on current growth stage

        Args:
            nitrogen (float): Available nitrogen (kg/ha)

        Returns:
            float: Stress factor 0-1 (1 = no stress)
        """
        weekly_need = self.get_nitrogen_requirement()

        if nitrogen >= weekly_need * 1.5:
            return 1.0  # Comfortable surplus
        elif nitrogen >= weekly_need:
            return 0.95  # Just enough
        elif nitrogen >= weekly_need * 0.5:
            ratio = nitrogen / weekly_need
            return 0.5 + ratio * 0.45  # Linear between 0.5 and 0.95
        elif nitrogen > 0:
            return (nitrogen / weekly_need) * 0.5  # Linear between 0 and 0.5
        else:
            return 0.0  # No nitrogen = no growth

    def _calculate_thermal_stress(self, temperature):
        """
        Calculate thermal stress

        Args:
            temperature (float): Current temperature (°C)

        Returns:
            float: Stress factor 0-1 (1 = no stress)
        """
        diff = abs(temperature - self.optimal_temp)

        if diff <= 3:
            return 1.0
        elif diff <= 6:
            return 0.85
        elif diff <= 10:
            return 0.6
        elif diff <= 15:
            return 0.3
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
        Calculate final yield based on NDVI

        Returns:
            float: Yield in tonnes/ha
        """
        # Yield is proportional to NDVI achievement
        max_yield = 8.0  # Base max yield
        yield_efficiency = self.ndvi / self.max_ndvi
        return max_yield * yield_efficiency

    def get_revenue(self):
        """
        Calculate gross revenue

        Returns:
            float: Revenue in USD
        """
        yield_tons = self.get_yield()
        return yield_tons * self.price_per_ton

    def to_dict(self):
        """Export crop state as dictionary"""
        stage_idx, stage_name = self.get_growth_stage()

        return {
            'type': self.type,
            'name': self.name,
            'ndvi': round(self.ndvi, 3),
            'age_weeks': self.age_weeks,
            'health': self._get_health_status(),
            'stage': stage_name,
            'nitrogen_requirement': round(self.get_nitrogen_requirement(), 1)
        }
