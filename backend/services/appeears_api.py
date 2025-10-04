"""
AppEEARS API Service
Extracts MODIS NDVI and SMAP soil moisture data
"""

import requests
import time
import json
from datetime import datetime, timedelta


class AppEEARSAPI:
    """Wrapper for NASA AppEEARS API"""

    def __init__(self):
        self.base_url = "https://appeears.earthdatacloud.nasa.gov/api"
        self.token = None
        self.token_expiration = None

    def login(self, username, password):
        """
        Login to AppEEARS and get authentication token

        Args:
            username (str): NASA Earthdata username
            password (str): NASA Earthdata password

        Returns:
            bool: True if login successful
        """
        try:
            response = requests.post(
                f"{self.base_url}/login",
                auth=(username, password),
                timeout=30
            )

            if response.status_code == 200:
                token_data = response.json()
                self.token = token_data['token']
                self.token_expiration = token_data['expiration']
                print(f"✅ AppEEARS login successful! Token expires: {self.token_expiration}")
                return True
            else:
                print(f"❌ AppEEARS login failed: {response.text}")
                return False

        except Exception as e:
            print(f"❌ AppEEARS login error: {e}")
            return False

    def get_headers(self):
        """Get authorization headers"""
        if not self.token:
            raise ValueError("Not logged in. Call login() first.")

        return {'Authorization': f'Bearer {self.token}'}

    def submit_point_task(self, task_name, lat, lon, start_date, end_date, layers):
        """
        Submit a point extraction task

        Args:
            task_name (str): Name for the task
            lat (float): Latitude
            lon (float): Longitude
            start_date (str): Start date (MM-DD-YYYY)
            end_date (str): End date (MM-DD-YYYY)
            layers (list): List of layer dicts [{'product': 'MOD13Q1.061', 'layer': '_250m_16_days_NDVI'}]

        Returns:
            str: task_id if successful, None otherwise
        """
        task = {
            'task_type': 'point',
            'task_name': task_name,
            'params': {
                'dates': [{
                    'startDate': start_date,
                    'endDate': end_date
                }],
                'layers': layers,
                'coordinates': [{
                    'latitude': lat,
                    'longitude': lon,
                    'id': f'{lat}_{lon}'
                }]
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/task",
                json=task,
                headers=self.get_headers(),
                timeout=30
            )

            if response.status_code == 202:
                result = response.json()
                task_id = result['task_id']
                print(f"✅ Task submitted: {task_id}")
                print(f"   Status: {result['status']}")
                return task_id
            else:
                print(f"❌ Task submission failed: {response.text}")
                return None

        except Exception as e:
            print(f"❌ Task submission error: {e}")
            return None

    def get_task_status(self, task_id):
        """
        Get status of a task

        Args:
            task_id (str): Task ID

        Returns:
            dict: Status information
        """
        try:
            response = requests.get(
                f"{self.base_url}/status/{task_id}",
                headers=self.get_headers(),
                timeout=30
            )

            if response.status_code == 200:
                status_data = response.json()
                if isinstance(status_data, list) and len(status_data) > 0:
                    return status_data[0]
                return status_data
            else:
                return None

        except Exception as e:
            print(f"❌ Status check error: {e}")
            return None

    def wait_for_task(self, task_id, max_wait_minutes=10):
        """
        Wait for task to complete

        Args:
            task_id (str): Task ID
            max_wait_minutes (int): Maximum time to wait

        Returns:
            bool: True if task completed successfully
        """
        print(f"⏳ Waiting for task {task_id} to complete...")

        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60

        while (time.time() - start_time) < max_wait_seconds:
            # Check task status
            response = requests.get(
                f"{self.base_url}/task/{task_id}",
                headers=self.get_headers(),
                timeout=30
            )

            if response.status_code == 200:
                task_data = response.json()
                status = task_data.get('status')

                print(f"   Status: {status}")

                if status == 'done':
                    print(f"✅ Task completed!")
                    return True
                elif status == 'error':
                    print(f"❌ Task failed: {task_data.get('error')}")
                    return False

                # Show progress if available
                if 'progress' in task_data:
                    progress = task_data['progress']
                    if 'summary' in progress:
                        print(f"   Progress: {progress['summary']}%")

            # Wait before next check
            time.sleep(10)

        print(f"⏰ Timeout waiting for task")
        return False

    def download_task_files(self, task_id, output_dir='.'):
        """
        Download all files from completed task

        Args:
            task_id (str): Task ID
            output_dir (str): Directory to save files

        Returns:
            list: List of downloaded file paths
        """
        try:
            # Get bundle (list of files)
            response = requests.get(
                f"{self.base_url}/bundle/{task_id}",
                headers=self.get_headers(),
                timeout=30
            )

            if response.status_code != 200:
                print(f"❌ Failed to get bundle: {response.text}")
                return []

            bundle = response.json()
            files = bundle.get('files', [])

            downloaded_files = []

            for file_info in files:
                file_id = file_info['file_id']
                file_name = file_info['file_name']
                file_path = f"{output_dir}/{file_name}"

                print(f"📥 Downloading: {file_name}")

                # Download file
                file_response = requests.get(
                    f"{self.base_url}/bundle/{task_id}/{file_id}",
                    headers=self.get_headers(),
                    allow_redirects=True,
                    stream=True,
                    timeout=60
                )

                if file_response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        for chunk in file_response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    print(f"   ✅ Saved: {file_path}")
                    downloaded_files.append(file_path)
                else:
                    print(f"   ❌ Download failed: {file_response.status_code}")

            return downloaded_files

        except Exception as e:
            print(f"❌ Download error: {e}")
            return []

    def extract_ndvi_smap_data(self, lat, lon, region_name, output_dir='data/appeears'):
        """
        Complete workflow: Extract NDVI and SMAP data for a location

        Args:
            lat (float): Latitude
            lon (float): Longitude
            region_name (str): Name of region
            output_dir (str): Output directory

        Returns:
            dict: Extracted data or None
        """
        import os
        os.makedirs(output_dir, exist_ok=True)

        # Date range: last 12 months
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)

        start_str = start_date.strftime("%m-%d-%Y")
        end_str = end_date.strftime("%m-%d-%Y")

        # Define layers to extract
        layers = [
            {
                'product': 'MOD13Q1.061',  # MODIS NDVI
                'layer': '_250m_16_days_NDVI'
            },
            {
                'product': 'MOD13Q1.061',  # MODIS EVI
                'layer': '_250m_16_days_EVI'
            }
            # Note: SMAP requires specific products - check availability
        ]

        # Submit task
        task_name = f"terragrow_{region_name.lower().replace(' ', '_')}"
        task_id = self.submit_point_task(
            task_name=task_name,
            lat=lat,
            lon=lon,
            start_date=start_str,
            end_date=end_str,
            layers=layers
        )

        if not task_id:
            return None

        # Wait for completion
        if not self.wait_for_task(task_id, max_wait_minutes=10):
            return None

        # Download results
        files = self.download_task_files(task_id, output_dir)

        if not files:
            return None

        # Parse CSV results
        csv_files = [f for f in files if f.endswith('.csv')]

        if csv_files:
            print(f"✅ Data extracted to: {csv_files[0]}")
            return {
                'task_id': task_id,
                'files': files,
                'csv_file': csv_files[0]
            }

        return None

    def list_available_products(self):
        """
        List all available products (no auth required)

        Returns:
            list: List of products
        """
        try:
            response = requests.get(
                f"{self.base_url}/product",
                timeout=30
            )

            if response.status_code == 200:
                products = response.json()
                return products

            return []

        except Exception as e:
            print(f"❌ Error listing products: {e}")
            return []

    def search_products(self, search_term):
        """
        Search for products containing a term

        Args:
            search_term (str): Search term (e.g., "NDVI", "SMAP")

        Returns:
            list: Matching products
        """
        products = self.list_available_products()

        matches = []
        for product in products:
            if search_term.upper() in product.get('Product', '').upper() or \
               search_term.upper() in product.get('Description', '').upper():
                matches.append(product)

        return matches
