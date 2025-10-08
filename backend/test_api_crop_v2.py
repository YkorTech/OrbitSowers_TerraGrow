"""
Test API Flask avec crop_v2
Teste tous les endpoints avec la nouvelle logique
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("TEST API FLASK - CROP V2 INTEGRATION")
print("=" * 70)

# Test 1: Health check
print("\n[TEST 1] Health Check")
print("-" * 70)
try:
    response = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    if response.status_code != 200:
        print("ERROR: API not responding")
        exit(1)
    print("SUCCESS: API is running")
except Exception as e:
    print(f"ERROR: Cannot connect to API - {e}")
    print("Make sure Flask server is running: python app.py")
    exit(1)

# Test 2: Get scenarios
print("\n[TEST 2] Get Available Scenarios")
print("-" * 70)
response = requests.get(f"{BASE_URL}/api/scenarios")
scenarios = response.json()
print(f"Total scenarios available: {scenarios['total']}")
print(f"\nFirst 3 scenarios:")
for scenario in scenarios['scenarios'][:3]:
    print(f"  - {scenario['region_name']} ({scenario['season_name']})")
    print(f"    Climate: {scenario['climate']}")
    print(f"    MODIS data: {'Yes' if scenario['has_modis'] else 'No'}")

# Test 3: Initialize game (Yaounde Spring 2024 - Maize)
print("\n[TEST 3] Initialize Game - Yaounde Spring 2024 - Maize")
print("-" * 70)
init_data = {
    "lat": 3.87,
    "lon": 11.52,
    "crop_type": "maize",
    "season_id": "spring_2024",
    "region_id": "yaounde_cameroun"
}

response = requests.post(f"{BASE_URL}/api/init", json=init_data)
game_data = response.json()
session_id = game_data['session_id']

print(f"Session ID: {session_id}")
print(f"\nInitial State:")
print(f"  Region: {game_data['state']['region']['name']}")
print(f"  Climate: {game_data['state']['region']['climate']}")
print(f"  Crop: {game_data['state']['crop']['name']}")
print(f"  Initial NDVI: {game_data['state']['crop']['ndvi']}")
print(f"  Budget: ${game_data['state']['budget']}")
print(f"  Soil type: {game_data['state']['soil']['name']}")
print(f"  Initial moisture: {game_data['state']['soil']['moisture']}%")
print(f"  Initial nitrogen: {game_data['state']['soil']['nitrogen']} kg/ha")

# Check V2 fields
if 'stage' in game_data['state']['crop']:
    print(f"  Growth stage: {game_data['state']['crop']['stage']} [V2 OK]")
else:
    print("  WARNING: No 'stage' field - V2 not working?")

if 'nitrogen_requirement' in game_data['state']['crop']:
    print(f"  N requirement: {game_data['state']['crop']['nitrogen_requirement']} kg/ha [V2 OK]")
else:
    print("  WARNING: No 'nitrogen_requirement' field - V2 not working?")

print(f"\nWeather preview (first 4 weeks):")
for week in game_data['weather_preview']:
    print(f"  Week {week['week_num']}: {week['temperature']:.1f}C, {week['precipitation']:.1f}mm rain, {week['evapotranspiration']:.1f}mm ET")

# Test 4: Simulate multiple weeks
print("\n[TEST 4] Simulate 12 Weeks - Optimal Fertilization Strategy")
print("-" * 70)

# Strategy: Heavy fertilization during vegetative stage (weeks 4-7)
fertilization_strategy = {
    1: 10,   # Germination: low N
    2: 10,
    3: 10,
    4: 25,   # Vegetative: HIGH N
    5: 30,
    6: 25,
    7: 20,
    8: 15,   # Flowering: medium N
    9: 15,
    10: 10,
    11: 5,   # Maturation: low N
    12: 5
}

irrigation_strategy = {
    # Adapt irrigation based on rainfall
}

results_summary = []

for week in range(1, 13):
    # Get state first to see weather
    state_response = requests.get(f"{BASE_URL}/api/state", params={"session_id": session_id})
    current_state = state_response.json()

    # Determine irrigation based on moisture
    current_moisture = current_state['soil']['moisture']
    if current_moisture < 40:
        irrigation = 30  # Heavy irrigation if dry
    elif current_moisture < 55:
        irrigation = 15  # Light irrigation
    else:
        irrigation = 0   # No irrigation if wet

    fertilizer = fertilization_strategy.get(week, 10)

    # Perform action
    action_data = {
        "session_id": session_id,
        "irrigation": irrigation,
        "fertilizer": fertilizer
    }

    response = requests.post(f"{BASE_URL}/api/action", json=action_data)
    result = response.json()

    if 'error' in result:
        print(f"Week {week}: ERROR - {result['error']}")
        break

    # Store summary
    results_summary.append({
        'week': week,
        'stage': result['crop'].get('stage', 'N/A'),
        'ndvi': result['crop']['ndvi'],
        'moisture': result['soil']['moisture'],
        'nitrogen_soil': result['soil']['nitrogen'],
        'n_requirement': result['crop'].get('nitrogen_requirement', 'N/A'),
        'irrigation': irrigation,
        'fertilizer': fertilizer,
        'cost': result['costs']['total'],
        'budget': result['budget'],
        'rain': result['weather']['rain'],
        'temp': result['weather']['temperature']
    })

    print(f"\nWeek {week}: {result['crop'].get('stage', 'N/A')}")
    print(f"  Actions: Irrigation={irrigation}mm, Fertilizer={fertilizer}kg N/ha")
    print(f"  Weather: {result['weather']['rain']:.1f}mm rain, {result['weather']['temperature']:.1f}C, {result['weather']['et']:.1f}mm ET")
    print(f"  Crop: NDVI={result['crop']['ndvi']:.3f}, N need={result['crop'].get('nitrogen_requirement', 'N/A')} kg/ha")
    print(f"  Soil: Moisture={result['soil']['moisture']:.1f}%, N={result['soil']['nitrogen']:.1f} kg/ha")
    print(f"  Economics: Cost=${result['costs']['total']:.2f}, Budget=${result['budget']:.2f}")

    # Show messages (skip to avoid emoji encoding issues)
    if 'messages' in result and result['messages']:
        print(f"  Messages: {len(result['messages'])} feedback(s)")

# Test 5: Harvest and final score
print("\n[TEST 5] Harvest - Final Score")
print("-" * 70)

response = requests.get(f"{BASE_URL}/api/harvest", params={"session_id": session_id})
harvest = response.json()

print("\nFINAL RESULTS:")
print("=" * 70)
print(f"Yield: {harvest['yield']} {harvest['yield_unit']}")
print(f"Regional average: {harvest['regional_avg']} t/ha")
print(f"Your difference: {harvest['yield_diff']:+.1f}%")
print(f"\nECONOMICS [NEW V2 FIELDS]:")
if 'revenue' in harvest:
    print(f"  Revenue: ${harvest['revenue']:.2f}")
    print(f"  Total costs: ${harvest['total_costs']:.2f}")
    print(f"  PROFIT: ${harvest['profit']:.2f} {'[POSITIVE]' if harvest['profit'] > 0 else '[NEGATIVE]'}")
    print("  [V2 OK] Economic fields present")
else:
    print("  WARNING: No economic fields (revenue, costs, profit) - V2 not working?")

print(f"\nSUSTAINABILITY:")
print(f"  Overall score: {harvest['sustainability_score']:.1f}/100")
print(f"  Water efficiency: {harvest['water_efficiency']:.2f} kg/m3")
print(f"  Nitrogen efficiency: {harvest['nitrogen_efficiency']:.1f}%")
print(f"\nRATING: {harvest['stars']}/5 stars")
print(f"Budget remaining: ${harvest['budget_remaining']:.2f}")

print(f"\nRECOMMENDATIONS: {len(harvest['recommendations'])} tips")

# Test 6: Summary table
print("\n[TEST 6] Growth Summary - NDVI Evolution by Stage")
print("-" * 70)
print(f"{'Week':<6} {'Stage':<15} {'NDVI':<8} {'N Need':<10} {'N Soil':<10} {'Moisture':<10}")
print("-" * 70)
for r in results_summary:
    print(f"{r['week']:<6} {r['stage']:<15} {r['ndvi']:<8.3f} {r['n_requirement']:<10} {r['nitrogen_soil']:<10.1f} {r['moisture']:<10.1f}%")

# Final verification
print("\n" + "=" * 70)
print("VERIFICATION CROP V2")
print("=" * 70)

v2_features = {
    "Phenological stages present": any('stage' in r for r in results_summary),
    "Dynamic N requirements": any('n_requirement' in r and r['n_requirement'] != 'N/A' for r in results_summary),
    "Economic calculations (profit)": 'profit' in harvest,
    "NDVI varies by stage": len(set(r['ndvi'] for r in results_summary)) > 5
}

all_ok = all(v2_features.values())

for feature, status in v2_features.items():
    status_symbol = "[OK]" if status else "[MISSING]"
    print(f"  {status_symbol} {feature}")

if all_ok:
    print("\n[SUCCESS] All Crop V2 features working in API!")
else:
    print("\n[WARNING] Some V2 features missing")

print("\nTest complete!")
