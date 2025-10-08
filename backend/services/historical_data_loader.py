"""
Historical Data Loader Service
Loads pre-downloaded NASA POWER and MODIS data from local files
"""

import json
import os
import math


class HistoricalDataLoader:
    """Loads historical weather and satellite data from local files"""

    def __init__(self):
        self.data_dir = os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'data',
            'regions'
        )

    def get_available_scenarios(self):
        """
        Get list of all available region/season combinations

        Returns:
            list: Available scenarios with metadata
        """
        scenarios = []

        if not os.path.exists(self.data_dir):
            return scenarios

        # Scan data/regions/ directory
        for folder_name in os.listdir(self.data_dir):
            folder_path = os.path.join(self.data_dir, folder_name)

            if not os.path.isdir(folder_path):
                continue

            # Load metadata
            metadata_path = os.path.join(folder_path, 'metadata.json')
            if not os.path.exists(metadata_path):
                continue

            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                # Check if weather data exists
                weather_path = os.path.join(folder_path, 'weather.json')
                if not os.path.exists(weather_path):
                    continue

                # Check if MODIS data exists (optional)
                has_modis = os.path.exists(
                    os.path.join(folder_path, 'modis_reference.json')
                )

                # Build scenario info
                scenario = {
                    'id': f"{metadata['region_id']}_{metadata['season_id']}",
                    'region_id': metadata['region_id'],
                    'region_name': metadata['region_name'],
                    'season_id': metadata['season_id'],
                    'season_name': metadata['season_name'],
                    'lat': metadata['location']['latitude'],
                    'lon': metadata['location']['longitude'],
                    'climate': metadata['location']['climate_zone'],
                    'period': metadata['period'],
                    'difficulty': metadata.get('difficulty', 'medium'),
                    'recommended_crops': metadata.get('recommended_crops', []),
                    'description': metadata.get('description', ''),
                    'has_modis': has_modis,
                    'data_sources': metadata.get('data_sources', {})
                }

                scenarios.append(scenario)

            except Exception as e:
                print(f"Error loading scenario {folder_name}: {e}")
                continue

        # Sort by region name, then season
        scenarios.sort(key=lambda x: (x['region_name'], x['season_id']))

        return scenarios

    def load_historical_data(self, region_id, season_id):
        """
        Load historical weather and MODIS data for a specific scenario

        Args:
            region_id: 'yaounde_cameroun'
            season_id: 'spring_2024'

        Returns:
            dict: Complete historical data or None if not found
        """
        folder_name = f"{region_id}_{season_id}"
        folder_path = os.path.join(self.data_dir, folder_name)

        if not os.path.exists(folder_path):
            return None

        try:
            # Load metadata
            with open(os.path.join(folder_path, 'metadata.json'), 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            # Load weather data
            with open(os.path.join(folder_path, 'weather.json'), 'r', encoding='utf-8') as f:
                weather_data = json.load(f)

            # Load MODIS data (optional)
            modis_data = None
            modis_path = os.path.join(folder_path, 'modis_reference.json')
            if os.path.exists(modis_path):
                with open(modis_path, 'r', encoding='utf-8') as f:
                    modis_data = json.load(f)

            return {
                'metadata': metadata,
                'weather': weather_data,
                'modis': modis_data
            }

        except Exception as e:
            print(f"Error loading historical data for {region_id}_{season_id}: {e}")
            return None

    def find_closest_scenario(self, lat, lon, season_id=None):
        """
        Find closest available scenario to given coordinates

        Args:
            lat: Latitude
            lon: Longitude
            season_id: Optional season filter ('spring_2024' or 'summer_2024')

        Returns:
            dict: Closest scenario or None
        """
        scenarios = self.get_available_scenarios()

        if not scenarios:
            return None

        # Filter by season if specified
        if season_id:
            scenarios = [s for s in scenarios if s['season_id'] == season_id]

        if not scenarios:
            return None

        # Find closest
        min_distance = float('inf')
        closest = None

        for scenario in scenarios:
            distance = self._calculate_distance(
                lat, lon,
                scenario['lat'], scenario['lon']
            )

            if distance < min_distance:
                min_distance = distance
                closest = scenario
                closest['distance_km'] = round(distance, 1)

        return closest

    def _calculate_distance(self, lat1, lon1, lat2, lon2):
        """Calculate distance between two coordinates (km) using Haversine formula"""
        R = 6371  # Earth radius in km

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return R * c
