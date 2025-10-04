"""
Geocoding Service
Handles location search using Nominatim API
"""

import requests
import time


class GeocodingService:
    """Wrapper for Nominatim geocoding API"""

    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.cache = {}
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Nominatim requires 1 request per second max

    def search_location(self, query):
        """
        Search for a location by name

        Args:
            query (str): Search query (e.g., "Yaoundé, Cameroun")

        Returns:
            list: Search results with lat, lon, name
        """
        # Check cache
        cache_key = query.lower()
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Rate limiting
        self._rate_limit()

        params = {
            'q': query,
            'format': 'json',
            'limit': 5,
            'addressdetails': 1
        }

        headers = {
            'User-Agent': 'TerraGrow-Academy/1.0 (NASA Space Apps Challenge)'
        }

        try:
            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            results = []
            for item in data:
                result = {
                    'name': item.get('display_name', ''),
                    'lat': float(item.get('lat', 0)),
                    'lon': float(item.get('lon', 0)),
                    'type': item.get('type', ''),
                    'importance': item.get('importance', 0)
                }
                results.append(result)

            # Cache results
            self.cache[cache_key] = results

            return results

        except requests.exceptions.RequestException as e:
            print(f"Geocoding error: {e}")
            return []

    def reverse_geocode(self, lat, lon):
        """
        Get location name from coordinates

        Args:
            lat (float): Latitude
            lon (float): Longitude

        Returns:
            dict: Location information
        """
        cache_key = f"{lat}_{lon}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        self._rate_limit()

        params = {
            'lat': lat,
            'lon': lon,
            'format': 'json',
            'addressdetails': 1
        }

        headers = {
            'User-Agent': 'TerraGrow-Academy/1.0 (NASA Space Apps Challenge)'
        }

        try:
            response = requests.get(
                f"{self.base_url}/reverse",
                params=params,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            result = {
                'name': data.get('display_name', 'Unknown Location'),
                'city': data.get('address', {}).get('city', ''),
                'country': data.get('address', {}).get('country', ''),
                'lat': lat,
                'lon': lon
            }

            self.cache[cache_key] = result

            return result

        except requests.exceptions.RequestException as e:
            print(f"Reverse geocoding error: {e}")
            return {
                'name': f'Location ({lat}, {lon})',
                'city': '',
                'country': '',
                'lat': lat,
                'lon': lon
            }

    def _rate_limit(self):
        """Ensure we respect Nominatim rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time

        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)

        self.last_request_time = time.time()
