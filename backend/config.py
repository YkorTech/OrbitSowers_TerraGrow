"""
Configuration file for TerraGrow Academy
"""

import os

class Config:
    """Base configuration"""

    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'terragrow-dev-secret-key-2025'
    DEBUG = True

    # API endpoints
    NASA_POWER_API_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"
    NOMINATIM_API_URL = "https://nominatim.openstreetmap.org/search"

    # Cache settings
    CACHE_TTL = 3600  # 1 hour in seconds

    # Game settings
    INITIAL_BUDGET = 2000  # USD
    WEEKS_PER_SEASON = 12

    # Data paths
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
    REGIONS_DIR = os.path.join(DATA_DIR, 'regions')

    # Popular regions (pre-calculated)
    POPULAR_REGIONS = {
        'yaounde': {'name': 'Yaoundé, Cameroun', 'lat': 3.87, 'lon': 11.52, 'climate': 'Tropical savane'},
        'maroua': {'name': 'Maroua, Cameroun', 'lat': 10.6, 'lon': 14.3, 'climate': 'Sahel semi-aride'},
        'douala': {'name': 'Douala, Cameroun', 'lat': 4.05, 'lon': 9.7, 'climate': 'Tropical humide'},
        'montreal': {'name': 'Montréal, Canada', 'lat': 45.5, 'lon': -73.6, 'climate': 'Continental humide'},
        'nairobi': {'name': 'Nairobi, Kenya', 'lat': -1.28, 'lon': 36.82, 'climate': 'Subtropical montagnard'},
        'kano': {'name': 'Kano, Nigeria', 'lat': 12.0, 'lon': 8.52, 'climate': 'Sahel'},
        'addis': {'name': 'Addis-Abeba, Éthiopie', 'lat': 9.03, 'lon': 38.74, 'climate': 'Subtropical montagnard'},
        'punjab': {'name': 'Punjab, Inde', 'lat': 30.73, 'lon': 76.78, 'climate': 'Semi-aride chaud'},
        'saopaulo': {'name': 'São Paulo, Brésil', 'lat': -23.55, 'lon': -46.63, 'climate': 'Subtropical humide'},
        'iowa': {'name': 'Iowa, USA', 'lat': 41.88, 'lon': -93.1, 'climate': 'Continental humide'},
        'beauce': {'name': 'Beauce, France', 'lat': 48.44, 'lon': 1.48, 'climate': 'Océanique tempéré'},
        'dhaka': {'name': 'Dhaka, Bangladesh', 'lat': 23.81, 'lon': 90.41, 'climate': 'Tropical mousson'},
        'pampas': {'name': 'Pampas, Argentine', 'lat': -34.6, 'lon': -58.38, 'climate': 'Subtropical humide'},
        'prairies': {'name': 'Prairies, Canada', 'lat': 50.45, 'lon': -104.62, 'climate': 'Continental semi-aride'},
        'garoua': {'name': 'Garoua, Cameroun', 'lat': 9.3, 'lon': 13.4, 'climate': 'Sahel'},
    }

    # Crop parameters
    CROPS = {
        'maize': {
            'name': 'Maïs',
            'optimal_temp': 25,  # °C
            'optimal_moisture': 60,  # %
            'water_need': 500,  # mm per season
            'nitrogen_need': 150,  # kg/ha
            'growth_rate': 0.08,  # NDVI increase per week
            'initial_ndvi': 0.15,
            'max_ndvi': 0.85,
        },
        'sorghum': {
            'name': 'Sorgho',
            'optimal_temp': 28,
            'optimal_moisture': 50,
            'water_need': 400,
            'nitrogen_need': 100,
            'growth_rate': 0.07,
            'initial_ndvi': 0.12,
            'max_ndvi': 0.80,
        },
        'wheat': {
            'name': 'Blé',
            'optimal_temp': 18,
            'optimal_moisture': 55,
            'water_need': 450,
            'nitrogen_need': 120,
            'growth_rate': 0.075,
            'initial_ndvi': 0.14,
            'max_ndvi': 0.82,
        }
    }

    # Soil types
    SOIL_TYPES = {
        'loam': {
            'name': 'Limon (Loam)',
            'field_capacity': 70,  # %
            'wilting_point': 25,  # %
            'drainage_rate': 0.15,
            'nitrogen_retention': 0.85,
        },
        'sandy': {
            'name': 'Sableux (Sandy)',
            'field_capacity': 50,
            'wilting_point': 15,
            'drainage_rate': 0.30,
            'nitrogen_retention': 0.65,
        },
        'clay': {
            'name': 'Argileux (Clay)',
            'field_capacity': 85,
            'wilting_point': 35,
            'drainage_rate': 0.08,
            'nitrogen_retention': 0.95,
        }
    }

    # Costs (USD)
    IRRIGATION_COST_PER_MM = 3.5  # $ per mm
    FERTILIZER_COST_PER_KG = 1.2  # $ per kg N
