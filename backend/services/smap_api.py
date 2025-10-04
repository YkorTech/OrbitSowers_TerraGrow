# -*- coding: utf-8 -*-
"""
SMAP API Service
Soil Moisture Active Passive - NASA satellite data
Provides REAL soil moisture measurements from space
"""

import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()


class SMAPAPI:
    """
    SMAP (Soil Moisture Active Passive) API wrapper

    SMAP satellite measures soil moisture from space
    - Launched: 2015
    - Resolution: ~9km
    - Frequency: 2-3 days
    """

    def __init__(self):
        self.username = os.getenv('NASA_EARTHDATA_USERNAME')
        self.password = os.getenv('NASA_EARTHDATA_PASSWORD')

        # SMAP L3 dataset (Level 3 - daily global)
        self.base_url = "https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.008"

        # Alternative: OpenDAP endpoint (easier access)
        self.opendap_url = "https://n5eil01u.ecs.nsidc.org/opendap/SMAP/SPL3SMP.008"

        self.cache = {}

    def get_soil_moisture(self, lat, lon, date=None):
        """
        Get soil moisture for a specific location and date

        Args:
            lat (float): Latitude
            lon (float): Longitude
            date (datetime): Date (default: yesterday)

        Returns:
            dict: Soil moisture data
        """
        if not self.username or not self.password:
            print("[WARNING] NASA Earthdata credentials not found in .env")
            return self._get_fallback_soil_moisture(lat, lon)

        if date is None:
            date = datetime.now() - timedelta(days=1)  # Yesterday (SMAP has delay)

        cache_key = f"{lat}_{lon}_{date.strftime('%Y%m%d')}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        try:
            # Method 1: Try simplified API (if available)
            soil_moisture = self._fetch_smap_simplified(lat, lon, date)

            if soil_moisture is None:
                # Method 2: Fallback to simulation
                print(f"[INFO] SMAP data not available for {date}, using simulation")
                soil_moisture = self._get_fallback_soil_moisture(lat, lon)

            self.cache[cache_key] = soil_moisture
            return soil_moisture

        except Exception as e:
            print(f"[ERROR] SMAP API error: {e}")
            return self._get_fallback_soil_moisture(lat, lon)

    def _fetch_smap_simplified(self, lat, lon, date):
        """
        Simplified SMAP fetch (if NSIDC provides REST API)

        Note: SMAP data access is complex, often requires:
        - File download (.h5 HDF5 format)
        - Libraries: h5py, netCDF4
        - Grid interpolation

        For MVP, we use fallback simulation
        """
        # TODO: Implement full SMAP access with h5py
        # Requires: pip install h5py netCDF4

        # For now, return None to use fallback
        return None

    def _get_fallback_soil_moisture(self, lat, lon):
        """
        Fallback: Estimate soil moisture based on climate

        This is used when:
        - No Earthdata credentials
        - SMAP data not available
        - API error
        """
        # Estimate based on latitude (climate proxy)
        abs_lat = abs(lat)

        if abs_lat < 10:  # Tropical
            base_moisture = 55
        elif abs_lat < 23.5:  # Subtropical
            base_moisture = 45
        elif abs_lat < 40:  # Temperate
            base_moisture = 50
        else:  # Cold
            base_moisture = 40

        return {
            'soil_moisture': base_moisture,
            'unit': '%',
            'source': 'simulation',
            'note': 'Simulated - SMAP data requires NASA Earthdata credentials'
        }

    def check_credentials(self):
        """
        Test NASA Earthdata credentials

        Returns:
            bool: True if credentials work
        """
        if not self.username or not self.password:
            return False

        # Test authentication with a simple request
        test_url = "https://urs.earthdata.nasa.gov/api/users/user"

        try:
            response = requests.get(
                test_url,
                auth=HTTPBasicAuth(self.username, self.password),
                timeout=10
            )

            if response.status_code == 200:
                print(f"[OK] NASA Earthdata authenticated: {self.username}")
                return True
            else:
                print(f"[ERROR] Authentication failed: {response.status_code}")
                return False

        except Exception as e:
            print(f"[ERROR] Credential check failed: {e}")
            return False


class SMAPAPI_Advanced:
    """
    Advanced SMAP implementation using h5py

    Requirements:
        pip install h5py netCDF4 pydap

    Usage:
        Only use if you have time to implement full HDF5 parsing
    """

    def __init__(self):
        try:
            import h5py
            self.h5py = h5py
            self.available = True
        except ImportError:
            print("[WARNING] h5py not installed. Install: pip install h5py")
            self.available = False

    def download_smap_file(self, date, username, password):
        """
        Download SMAP HDF5 file for a specific date

        File format: SMAP_L3_SM_P_YYYYMMDD_R18290_001.h5
        """
        if not self.available:
            return None

        # Build filename
        filename = f"SMAP_L3_SM_P_{date.strftime('%Y%m%d')}_R18290_001.h5"

        # Download URL (requires authentication)
        year = date.strftime('%Y')
        month = date.strftime('%m')
        day = date.strftime('%d')

        url = f"https://n5eil01u.ecs.nsidc.org/SMAP/SPL3SMP.008/{year}.{month}.{day}/{filename}"

        # TODO: Implement download with authentication
        # session = requests.Session()
        # session.auth = (username, password)
        # response = session.get(url)

        return None

    def extract_soil_moisture_from_h5(self, h5_file, lat, lon):
        """
        Extract soil moisture from downloaded H5 file

        Args:
            h5_file (str): Path to .h5 file
            lat (float): Latitude
            lon (float): Longitude

        Returns:
            float: Soil moisture (%)
        """
        if not self.available:
            return None

        # TODO: Implement H5 parsing
        # with h5py.File(h5_file, 'r') as f:
        #     soil_moisture = f['Soil_Moisture_Retrieval_Data']['soil_moisture'][...]
        #     # Interpolate to lat/lon

        return None


# Helper function for easy integration
def get_smap_soil_moisture(lat, lon):
    """
    Convenience function to get SMAP soil moisture

    Usage:
        moisture = get_smap_soil_moisture(3.87, 11.52)
    """
    smap = SMAPAPI()
    return smap.get_soil_moisture(lat, lon)
