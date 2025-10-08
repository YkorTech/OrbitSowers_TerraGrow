"""
Data Provider Service
Hybrid data provider that uses pre-calculated data or NASA API
"""

import json
import os
import math
from .nasa_power_api import NASAPowerAPI
from .geocoding_service import GeocodingService
from .historical_data_loader import HistoricalDataLoader


class DataProvider:
    """Provides game data from static files or APIs"""

    def __init__(self):
        self.nasa_api = NASAPowerAPI()
        self.geocoding = GeocodingService()
        self.historical_loader = HistoricalDataLoader()
        self.static_regions = self._load_popular_regions()

    def _load_popular_regions(self):
        """Load popular regions from config"""
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
        from config import Config
        return Config.POPULAR_REGIONS

    def get_game_data(self, lat, lon, season_id=None, region_id=None):
        """
        Get complete game data for a location

        Args:
            lat (float): Latitude
            lon (float): Longitude
            season_id (str): Optional season ID ('spring_2024', 'summer_2024')
            region_id (str): Optional region ID ('yaounde_cameroun', etc.)

        Returns:
            dict: Game data including region info and weather
        """
        # If region_id and season_id provided, use historical data
        if region_id and season_id:
            historical_data = self.historical_loader.load_historical_data(region_id, season_id)
            if historical_data:
                return self._format_historical_data(historical_data)

        # If only season_id provided, find closest scenario
        if season_id:
            closest = self.historical_loader.find_closest_scenario(lat, lon, season_id)
            if closest and closest.get('distance_km', 999) < 50:
                historical_data = self.historical_loader.load_historical_data(
                    closest['region_id'],
                    closest['season_id']
                )
                if historical_data:
                    return self._format_historical_data(historical_data)

        # Fallback: Try to find closest popular region (any season)
        closest_region = self._find_closest_region(lat, lon)

        if closest_region and self._is_close_enough(lat, lon, closest_region['lat'], closest_region['lon']):
            # Use popular region data
            return self._get_popular_region_data(closest_region, lat, lon)
        else:
            # Use API for custom location
            return self._get_api_region_data(lat, lon)

    def _find_closest_region(self, lat, lon):
        """Find the closest popular region"""
        min_distance = float('inf')
        closest = None

        for key, region in self.static_regions.items():
            distance = self._calculate_distance(lat, lon, region['lat'], region['lon'])

            if distance < min_distance:
                min_distance = distance
                closest = region

        return closest

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates (km)"""
        # Haversine formula
        R = 6371  # Earth radius in km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c

    def _is_close_enough(self, lat1, lon1, lat2, lon2, threshold_km=50):
        """Check if two locations are close enough to use same data"""
        distance = self._calculate_distance(lat1, lon1, lat2, lon2)
        return distance < threshold_km

    def _get_popular_region_data(self, region, lat, lon):
        """Get data for a popular pre-calculated region"""
        # Check if static file exists
        data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'regions')
        region_file = os.path.join(data_dir, f"{region['name'].lower().replace(' ', '_').replace(',', '')}.json")

        # Try to load static data
        static_data = None
        if os.path.exists(region_file):
            try:
                with open(region_file, 'r', encoding='utf-8') as f:
                    static_data = json.load(f)
            except:
                pass

        # Get weather data from NASA API (always real-time)
        weather_data = self.nasa_api.get_weekly_aggregates(region['lat'], region['lon'], weeks=12)

        return {
            'name': region['name'],
            'lat': region['lat'],
            'lon': region['lon'],
            'climate': region['climate'],
            'soil_type': static_data.get('soil_type', 'loam') if static_data else 'loam',
            'weather_data': weather_data,
            'source': 'popular_region'
        }

    def _get_api_region_data(self, lat, lon):
        """Get data for a custom location using APIs"""
        # Get location name
        location_info = self.geocoding.reverse_geocode(lat, lon)

        # Determine climate based on latitude (simplified)
        climate = self._estimate_climate(lat)

        # Get weather data from NASA API
        weather_data = self.nasa_api.get_weekly_aggregates(lat, lon, weeks=12)

        # Determine soil type based on climate (simplified)
        soil_type = self._estimate_soil_type(climate)

        return {
            'name': location_info.get('name', f'Location ({lat}, {lon})'),
            'lat': lat,
            'lon': lon,
            'climate': climate,
            'soil_type': soil_type,
            'weather_data': weather_data,
            'source': 'api'
        }

    def _estimate_climate(self, lat):
        """Estimate climate type based on latitude"""
        abs_lat = abs(lat)

        if abs_lat < 10:
            return 'Tropical équatorial'
        elif abs_lat < 23.5:
            return 'Tropical savane'
        elif abs_lat < 35:
            return 'Subtropical'
        elif abs_lat < 50:
            return 'Continental tempéré'
        else:
            return 'Continental froid'

    def _estimate_soil_type(self, climate):
        """Estimate dominant soil type based on climate"""
        climate_lower = climate.lower()

        if 'tropical' in climate_lower:
            return 'loam'  # Changed from clay to loam for better drainage in rainy tropics
        elif 'arid' in climate_lower or 'sahel' in climate_lower:
            return 'sandy'
        else:
            return 'loam'  # Default

    def _format_historical_data(self, historical_data):
        """
        Format historical data to match game data structure

        Args:
            historical_data: dict with 'metadata', 'weather', 'modis'

        Returns:
            dict: Formatted game data
        """
        metadata = historical_data['metadata']
        weather = historical_data['weather']
        modis = historical_data.get('modis')

        # Convert weather weeks to expected format
        weather_weeks = []
        for week in weather['weeks']:
            # Calculate realistic ET from et0_total (daily) to weekly
            # et0_total in JSON is already weekly total, but values seem too low
            # Multiply by 7 to get realistic weekly ET (assuming et0 was daily average)
            et0_weekly = week.get('et0_total', 3.5) * 7  # ~25mm/week realistic

            weather_weeks.append({
                'temperature': week['temperature_avg'],
                'precipitation': week['precipitation_total'],
                'humidity': week['humidity_avg'],
                'wind_speed': week.get('wind_speed_avg', 0),
                'evapotranspiration': et0_weekly,  # ✅ Fixed key name
                'week_num': week['week']
            })

        # Estimate soil type based on climate
        soil_type = self._estimate_soil_type(metadata['location']['climate_zone'])

        return {
            'name': metadata['region_name'],
            'lat': metadata['location']['latitude'],
            'lon': metadata['location']['longitude'],
            'climate': metadata['location']['climate_zone'],
            'soil_type': soil_type,
            'weather_data': weather_weeks,
            'modis_reference': modis['weeks'] if modis else None,
            'period': metadata['period'],
            'season_id': metadata['season_id'],
            'region_id': metadata['region_id'],
            'data_sources': metadata.get('data_sources', {}),
            'source': 'historical'
        }

    def get_region_suggestions(self):
        """Get list of popular regions as suggestions"""
        suggestions = []

        for key, region in self.static_regions.items():
            suggestions.append({
                'id': key,
                'name': region['name'],
                'lat': region['lat'],
                'lon': region['lon'],
                'climate': region['climate']
            })

        return suggestions
