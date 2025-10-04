"""
NASA POWER API Service
Handles weather data retrieval from NASA POWER API
"""

import requests
from datetime import datetime, timedelta


class NASAPowerAPI:
    """Wrapper for NASA POWER API"""

    def __init__(self):
        self.base_url = "https://power.larc.nasa.gov/api/temporal/daily/point"
        self.cache = {}

    def get_weather_data(self, lat, lon, days=90):
        """
        Get weather data for a location

        Args:
            lat (float): Latitude
            lon (float): Longitude
            days (int): Number of days of data

        Returns:
            list: Weather data for each day
        """
        # Check cache
        cache_key = f"{lat}_{lon}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Calculate date range (last 90 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        params = {
            "parameters": "T2M,PRECTOTCORR,RH2M",  # Temp, Precipitation, Humidity
            "community": "AG",  # Agriculture community
            "longitude": lon,
            "latitude": lat,
            "start": start_date.strftime("%Y%m%d"),
            "end": end_date.strftime("%Y%m%d"),
            "format": "JSON"
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            # Extract parameters
            if 'properties' not in data or 'parameter' not in data['properties']:
                raise ValueError("Invalid API response structure")

            parameters = data['properties']['parameter']
            temps = parameters.get('T2M', {})
            precip = parameters.get('PRECTOTCORR', {})
            humidity = parameters.get('RH2M', {})

            # Convert to list of daily data
            weather_data = []
            for date_key in sorted(temps.keys()):
                weather_data.append({
                    'date': date_key,
                    'temperature': temps.get(date_key, 25),
                    'precipitation': precip.get(date_key, 0),
                    'humidity': humidity.get(date_key, 50),
                    'evapotranspiration': self._estimate_et(temps.get(date_key, 25), humidity.get(date_key, 50))
                })

            # Cache the result
            self.cache[cache_key] = weather_data

            return weather_data

        except requests.exceptions.RequestException as e:
            print(f"NASA POWER API error: {e}")
            # Return fallback data
            return self._get_fallback_data(lat, days)

    def get_weekly_aggregates(self, lat, lon, weeks=12):
        """
        Get weather data aggregated by week

        Args:
            lat (float): Latitude
            lon (float): Longitude
            weeks (int): Number of weeks

        Returns:
            list: Weekly aggregated weather data
        """
        daily_data = self.get_weather_data(lat, lon, weeks * 7)

        if not daily_data:
            return self._get_fallback_weekly_data(weeks)

        # Aggregate by week
        weekly_data = []
        for i in range(0, min(len(daily_data), weeks * 7), 7):
            week_slice = daily_data[i:i+7]

            if not week_slice:
                continue

            avg_temp = sum(d['temperature'] for d in week_slice) / len(week_slice)
            total_precip = sum(d['precipitation'] for d in week_slice)
            avg_humidity = sum(d['humidity'] for d in week_slice) / len(week_slice)
            total_et = sum(d['evapotranspiration'] for d in week_slice)

            weekly_data.append({
                'week': len(weekly_data) + 1,
                'temperature': round(avg_temp, 1),
                'precipitation': round(total_precip, 1),
                'humidity': round(avg_humidity, 1),
                'evapotranspiration': round(total_et, 1)
            })

        return weekly_data[:weeks]

    def _estimate_et(self, temperature, humidity):
        """
        Estimate daily evapotranspiration using simplified formula

        Args:
            temperature (float): Temperature in °C
            humidity (float): Relative humidity %

        Returns:
            float: ET in mm/day
        """
        # Simplified Hargreaves equation approximation
        et = 0.0023 * (temperature + 17.8) * (100 - humidity) / 10
        return max(0, et)

    def _get_fallback_data(self, lat, days):
        """Generate fallback weather data if API fails"""
        import random

        # Determine climate based on latitude
        if abs(lat) < 23:  # Tropical
            base_temp = 28
            base_rain = 5
        elif abs(lat) < 40:  # Subtropical
            base_temp = 22
            base_rain = 3
        else:  # Temperate
            base_temp = 15
            base_rain = 2

        fallback = []
        for i in range(days):
            temp = base_temp + random.uniform(-3, 3)
            rain = max(0, base_rain + random.uniform(-2, 8))

            fallback.append({
                'date': f"day_{i+1}",
                'temperature': round(temp, 1),
                'precipitation': round(rain, 1),
                'humidity': 50 + random.uniform(-15, 15),
                'evapotranspiration': round(self._estimate_et(temp, 50), 1)
            })

        return fallback

    def _get_fallback_weekly_data(self, weeks):
        """Generate fallback weekly data"""
        daily = self._get_fallback_data(0, weeks * 7)
        return self.get_weekly_aggregates_from_daily(daily, weeks)

    def get_weekly_aggregates_from_daily(self, daily_data, weeks):
        """Aggregate daily data into weekly"""
        weekly = []
        for i in range(0, min(len(daily_data), weeks * 7), 7):
            week_slice = daily_data[i:i+7]
            if not week_slice:
                continue

            weekly.append({
                'week': len(weekly) + 1,
                'temperature': round(sum(d['temperature'] for d in week_slice) / len(week_slice), 1),
                'precipitation': round(sum(d['precipitation'] for d in week_slice), 1),
                'humidity': round(sum(d['humidity'] for d in week_slice) / len(week_slice), 1),
                'evapotranspiration': round(sum(d['evapotranspiration'] for d in week_slice), 1)
            })

        return weekly[:weeks]
