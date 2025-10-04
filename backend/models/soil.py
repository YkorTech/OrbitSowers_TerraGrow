"""
Soil model for TerraGrow Academy
Handles soil moisture, nitrogen, and water balance
"""


class Soil:
    """Represents soil in the game"""

    def __init__(self, soil_type, parameters, initial_moisture=50):
        """
        Initialize soil

        Args:
            soil_type (str): Type of soil (loam, sandy, clay)
            parameters (dict): Soil parameters from config
            initial_moisture (float): Initial moisture percentage
        """
        self.type = soil_type
        self.name = parameters['name']
        self.field_capacity = parameters['field_capacity']
        self.wilting_point = parameters['wilting_point']
        self.drainage_rate = parameters['drainage_rate']
        self.nitrogen_retention = parameters['nitrogen_retention']

        # Current state
        self.moisture = initial_moisture
        self.nitrogen = 80  # kg/ha initial
        self.organic_matter = 2.5  # % initial

    def update_moisture(self, rain, irrigation, evapotranspiration):
        """
        Update soil moisture based on water balance

        Args:
            rain (float): Precipitation (mm)
            irrigation (float): Applied irrigation (mm)
            evapotranspiration (float): ET (mm)

        Returns:
            dict: Moisture update info
        """
        # Water inputs (1mm = ~1% moisture for simplification)
        water_in = rain + irrigation

        # Water outputs
        water_out = evapotranspiration

        # Calculate new moisture
        new_moisture = self.moisture + water_in - water_out

        # Drainage if exceeds field capacity
        drainage = 0
        if new_moisture > self.field_capacity:
            drainage = (new_moisture - self.field_capacity) * self.drainage_rate
            new_moisture -= drainage

        # Limit to physical bounds
        new_moisture = max(self.wilting_point, min(new_moisture, 100))

        # Nitrogen leaching from drainage
        nitrogen_loss = drainage * (1 - self.nitrogen_retention) * 0.5
        self.nitrogen = max(0, self.nitrogen - nitrogen_loss)

        self.moisture = new_moisture

        return {
            'moisture': self.moisture,
            'water_in': water_in,
            'water_out': water_out,
            'drainage': drainage,
            'nitrogen_leached': nitrogen_loss,
            'status': self._get_moisture_status()
        }

    def add_fertilizer(self, nitrogen_kg):
        """
        Add nitrogen fertilizer

        Args:
            nitrogen_kg (float): Nitrogen to add (kg/ha)

        Returns:
            dict: Fertilizer application info
        """
        self.nitrogen += nitrogen_kg * 0.8  # 80% efficiency

        # Limit max nitrogen accumulation
        self.nitrogen = min(self.nitrogen, 200)

        return {
            'nitrogen': self.nitrogen,
            'added': nitrogen_kg * 0.8
        }

    def extract_nutrients(self, crop_uptake):
        """
        Simulate nutrient extraction by crop

        Args:
            crop_uptake (float): Nitrogen uptake by crop (kg/ha)
        """
        self.nitrogen = max(0, self.nitrogen - crop_uptake)

    def _get_moisture_status(self):
        """Get soil moisture status"""
        if self.moisture >= self.field_capacity * 0.8:
            return 'optimal'
        elif self.moisture >= self.wilting_point * 1.5:
            return 'adequate'
        elif self.moisture >= self.wilting_point * 1.2:
            return 'low'
        else:
            return 'critical'

    def get_available_water(self):
        """Calculate available water for crops"""
        return max(0, self.moisture - self.wilting_point)

    def to_dict(self):
        """Export soil state as dictionary"""
        return {
            'type': self.type,
            'name': self.name,
            'moisture': round(self.moisture, 1),
            'nitrogen': round(self.nitrogen, 1),
            'status': self._get_moisture_status(),
            'available_water': round(self.get_available_water(), 1)
        }
