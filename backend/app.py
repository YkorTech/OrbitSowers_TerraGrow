"""
Flask API for TerraGrow Academy
Main application file with REST endpoints
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from config import Config
from models import Crop, Soil, Region, GameState
from services.nasa_power_api import NASAPowerAPI
from services.geocoding_service import GeocodingService
from services.data_provider import DataProvider

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Initialize services
nasa_api = NASAPowerAPI()
geocoding_service = GeocodingService()
data_provider = DataProvider()

# Store active game states (in production, use database)
game_sessions = {}


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'TerraGrow API is running'})


@app.route('/api/search-location', methods=['GET'])
def search_location():
    """
    Search for a location using Nominatim

    Query params:
        q (str): Search query
    """
    query = request.args.get('q', '')

    if not query:
        return jsonify({'error': 'Query parameter q is required'}), 400

    try:
        results = geocoding_service.search_location(query)
        return jsonify({'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/popular-regions', methods=['GET'])
def get_popular_regions():
    """Get list of popular pre-calculated regions"""
    regions = []
    for key, info in Config.POPULAR_REGIONS.items():
        regions.append({
            'id': key,
            'name': info['name'],
            'lat': info['lat'],
            'lon': info['lon'],
            'climate': info['climate']
        })

    return jsonify({'regions': regions})


@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """
    Get list of available historical scenarios (region + season combinations)

    Returns:
        JSON with list of scenarios including:
        - region_id, region_name
        - season_id, season_name
        - lat, lon, climate
        - difficulty, recommended_crops
        - has_modis (bool)
    """
    try:
        scenarios = data_provider.historical_loader.get_available_scenarios()
        return jsonify({
            'scenarios': scenarios,
            'total': len(scenarios)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/init', methods=['POST'])
def initialize_game():
    """
    Initialize a new game session

    Body:
        lat (float): Latitude
        lon (float): Longitude
        crop_type (str): Type of crop (optional, auto-selected)
        season_id (str): Season ID (optional, 'spring_2024' or 'summer_2024')
        region_id (str): Region ID (optional, e.g. 'yaounde_cameroun')
    """
    data = request.get_json()

    lat = data.get('lat')
    lon = data.get('lon')
    crop_type = data.get('crop_type')
    season_id = data.get('season_id')
    region_id = data.get('region_id')

    if lat is None or lon is None:
        return jsonify({'error': 'lat and lon are required'}), 400

    try:
        # Get region data (with optional historical scenario)
        region_data = data_provider.get_game_data(
            lat, lon,
            season_id=season_id,
            region_id=region_id
        )

        # Create region object
        region = Region(
            name=region_data['name'],
            lat=lat,
            lon=lon,
            climate=region_data['climate'],
            soil_type=region_data.get('soil_type', 'loam')
        )

        # Auto-select crop if not provided
        if not crop_type:
            recommended = region.get_recommended_crops()
            crop_type = recommended[0] if recommended else 'maize'

        # Validate crop type
        if crop_type not in Config.CROPS:
            return jsonify({'error': f'Invalid crop type: {crop_type}'}), 400

        # Create game state
        game_state = GameState(
            region=region,
            crop_type=crop_type,
            crop_params=Config.CROPS[crop_type],
            soil_params=Config.SOIL_TYPES[region_data.get('soil_type', 'loam')],
            initial_budget=Config.INITIAL_BUDGET
        )

        # Store weather data
        game_state.weather_data = region_data.get('weather_data', [])

        # Generate session ID
        session_id = f"{lat}_{lon}_{crop_type}"
        game_sessions[session_id] = game_state

        # Return initial state
        return jsonify({
            'session_id': session_id,
            'state': game_state.to_dict(),
            'recommended_crops': region.get_recommended_crops(),
            'weather_preview': game_state.weather_data[:4] if game_state.weather_data else []
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/action', methods=['POST'])
def perform_action():
    """
    Perform a weekly action

    Body:
        session_id (str): Game session ID
        irrigation (float): Irrigation amount (mm)
        fertilizer (float): Fertilizer amount (kg N/ha)
    """
    data = request.get_json()

    session_id = data.get('session_id')
    irrigation = data.get('irrigation', 0)
    fertilizer = data.get('fertilizer', 0)

    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400

    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session_id'}), 404

    try:
        game_state = game_sessions[session_id]

        # Check if game is complete
        if game_state.current_week > game_state.max_weeks:
            return jsonify({'error': 'Game already completed'}), 400

        # Get weather for current week
        week_index = game_state.current_week - 1
        if week_index < len(game_state.weather_data):
            weather = game_state.weather_data[week_index]
        else:
            # Fallback weather if not available
            weather = {
                'precipitation': 10,
                'temperature': 25,
                'evapotranspiration': 25
            }

        # Simulate week
        result = game_state.simulate_week(irrigation, fertilizer, weather)

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/harvest', methods=['GET'])
def harvest():
    """
    Harvest and get final score

    Query params:
        session_id (str): Game session ID
    """
    session_id = request.args.get('session_id')

    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400

    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session_id'}), 404

    try:
        game_state = game_sessions[session_id]

        if game_state.current_week <= game_state.max_weeks:
            return jsonify({'error': 'Game not yet complete'}), 400

        # Calculate final score
        scores = game_state.calculate_final_score()

        return jsonify(scores)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/state', methods=['GET'])
def get_state():
    """
    Get current game state

    Query params:
        session_id (str): Game session ID
    """
    session_id = request.args.get('session_id')

    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400

    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session_id'}), 404

    game_state = game_sessions[session_id]
    return jsonify(game_state.to_dict())


@app.route('/api/accept-loan', methods=['POST'])
def accept_loan():
    """
    Accept emergency loan offer

    Body:
        session_id (str): Game session ID
    """
    data = request.get_json()
    session_id = data.get('session_id')

    if not session_id:
        return jsonify({'error': 'session_id is required'}), 400

    if session_id not in game_sessions:
        return jsonify({'error': 'Invalid session_id'}), 404

    try:
        game_state = game_sessions[session_id]

        # Check if already taken
        if game_state.loan_taken:
            return jsonify({'error': 'Loan already taken'}), 400

        # Check if eligible (week >= 8)
        if game_state.current_week < 8:
            return jsonify({'error': 'Loan only available from week 8'}), 400

        # Grant loan
        loan_amount = 500
        game_state.loan_taken = True
        game_state.loan_amount = loan_amount
        game_state.loan_week = game_state.current_week
        game_state.budget += loan_amount

        return jsonify({
            'success': True,
            'loan_amount': loan_amount,
            'new_budget': game_state.budget,
            'repayment_due': loan_amount * 1.20,
            'message': f'Pret de ${loan_amount} accorde. Remboursement: ${loan_amount * 1.20:.0f} (interet 20%)'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("TerraGrow Academy API starting...")
    print(f"Popular regions loaded: {len(Config.POPULAR_REGIONS)}")
    app.run(debug=True, port=5000, host='0.0.0.0')
