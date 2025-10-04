"""
Region model for TerraGrow Academy
Handles region-specific parameters and climate
"""


class Region:
    """Represents a geographical region in the game"""

    def __init__(self, name, lat, lon, climate, soil_type='loam', data=None):
        """
        Initialize region

        Args:
            name (str): Region name
            lat (float): Latitude
            lon (float): Longitude
            climate (str): Climate type
            soil_type (str): Dominant soil type
            data (dict): Optional pre-calculated data
        """
        self.name = name
        self.lat = lat
        self.lon = lon
        self.climate = climate
        self.soil_type = soil_type
        self.data = data or {}

    def get_recommended_crops(self):
        """
        Get recommended crops for this region

        Returns:
            list: List of recommended crop types
        """
        climate_lower = self.climate.lower()

        if 'tropical' in climate_lower or 'humid' in climate_lower:
            return ['maize', 'sorghum']
        elif 'sahel' in climate_lower or 'arid' in climate_lower or 'semi-arid' in climate_lower:
            return ['sorghum', 'maize']
        elif 'continental' in climate_lower or 'océanique' in climate_lower or 'tempéré' in climate_lower:
            return ['wheat', 'maize']
        else:
            return ['maize']  # Default

    def get_climate_characteristics(self):
        """
        Get climate characteristics for this region

        Returns:
            dict: Climate characteristics
        """
        climate_lower = self.climate.lower()

        if 'tropical' in climate_lower:
            return {
                'avg_temp': 26,
                'avg_rain': 150,  # mm per month
                'rain_variability': 'high',
                'typical_events': ['heavy_rain', 'drought']
            }
        elif 'sahel' in climate_lower or 'semi-arid' in climate_lower:
            return {
                'avg_temp': 32,
                'avg_rain': 50,
                'rain_variability': 'very_high',
                'typical_events': ['drought', 'heatwave']
            }
        elif 'continental' in climate_lower:
            return {
                'avg_temp': 15,
                'avg_rain': 80,
                'rain_variability': 'medium',
                'typical_events': ['frost', 'cold_snap']
            }
        elif 'subtropical' in climate_lower:
            return {
                'avg_temp': 20,
                'avg_rain': 100,
                'rain_variability': 'medium',
                'typical_events': ['heavy_rain', 'drought']
            }
        else:
            return {
                'avg_temp': 22,
                'avg_rain': 100,
                'rain_variability': 'medium',
                'typical_events': ['drought']
            }

    def to_dict(self):
        """Export region as dictionary"""
        return {
            'name': self.name,
            'lat': self.lat,
            'lon': self.lon,
            'climate': self.climate,
            'soil_type': self.soil_type,
            'recommended_crops': self.get_recommended_crops(),
            'characteristics': self.get_climate_characteristics()
        }
