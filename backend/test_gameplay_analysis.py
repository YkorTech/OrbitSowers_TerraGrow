"""
Analyse complete du gameplay
Test plusieurs scenarios pour identifier les problemes
"""

import requests
import sys

BASE_URL = "http://localhost:5000"

def test_scenario(region_name, lat, lon, season_id, region_id, crop_type):
    """Test un scenario complet"""
    print("\n" + "=" * 80)
    print(f"SCENARIO: {region_name} - {crop_type.upper()} - {season_id}")
    print("=" * 80)

    # Init
    init_data = {
        "lat": lat,
        "lon": lon,
        "crop_type": crop_type,
        "season_id": season_id,
        "region_id": region_id
    }

    response = requests.post(f"{BASE_URL}/api/init", json=init_data)
    game_data = response.json()
    session_id = game_data['session_id']

    initial_budget = game_data['state']['budget']
    soil_type = game_data['state']['soil']['name']

    print(f"\nInitial state:")
    print(f"  Region: {game_data['state']['region']['name']}")
    print(f"  Climate: {game_data['state']['region']['climate']}")
    print(f"  Soil: {soil_type}")
    print(f"  Budget: ${initial_budget}")
    print(f"  Crop: {game_data['state']['crop']['name']} (optimal moisture: {game_data['state']['crop']['name']})")

    # Preview weather
    print(f"\nWeather overview (12 weeks):")
    total_rain = 0
    total_et = 0
    for week in game_data['weather_preview']:
        total_rain += week['precipitation']
        total_et += week['evapotranspiration']

    print(f"  Total rain: {total_rain:.1f}mm")
    print(f"  Total ET: {total_et:.1f}mm")
    print(f"  Balance: {total_rain - total_et:+.1f}mm {'(DEFICIT)' if total_rain < total_et else '(EXCESS)'}")

    # Strategy
    print(f"\nStrategy:")

    # Determine strategy based on climate
    water_deficit = total_et - total_rain

    if water_deficit > 200:  # Arid region
        print(f"  ARID region detected (deficit {water_deficit:.0f}mm)")
        print(f"  -> Heavy irrigation required")
        irrigation_per_week = 30
        fertilizer_base = 15
    elif water_deficit > 0:  # Moderate deficit
        print(f"  MODERATE region (deficit {water_deficit:.0f}mm)")
        print(f"  -> Light irrigation needed")
        irrigation_per_week = 15
        fertilizer_base = 15
    else:  # Humid
        print(f"  HUMID region (excess {-water_deficit:.0f}mm)")
        print(f"  -> No irrigation, focus on fertilization")
        irrigation_per_week = 0
        fertilizer_base = 15

    # Simulate
    print(f"\nSimulating 12 weeks...")
    print("-" * 80)

    results = []
    budget_exhausted_week = None

    for week in range(1, 13):
        # Get current state
        state_response = requests.get(f"{BASE_URL}/api/state", params={"session_id": session_id})
        current_state = state_response.json()

        current_moisture = current_state['soil']['moisture']
        current_budget = current_state['budget']

        # Adaptive strategy
        if current_moisture < 35:
            irrigation = irrigation_per_week + 20  # Emergency irrigation
        elif current_moisture < 50:
            irrigation = irrigation_per_week + 10
        else:
            irrigation = irrigation_per_week

        # Phenological fertilization
        if week <= 3:
            fertilizer = fertilizer_base * 0.7
        elif week <= 7:
            fertilizer = fertilizer_base * 1.5  # Peak vegetative
        elif week <= 10:
            fertilizer = fertilizer_base * 1.0
        else:
            fertilizer = fertilizer_base * 0.5

        # Check if can afford
        estimated_cost = irrigation * 3.5 + fertilizer * 1.2

        if estimated_cost > current_budget:
            # Reduce actions to fit budget
            if current_budget < 20:
                # Critical budget
                irrigation = 0
                fertilizer = min(5, current_budget / 1.2)
                budget_exhausted_week = week
            else:
                # Scale down
                ratio = current_budget / estimated_cost * 0.9
                irrigation = irrigation * ratio
                fertilizer = fertilizer * ratio

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

        # Store results
        results.append({
            'week': week,
            'ndvi': result['crop']['ndvi'],
            'moisture': result['soil']['moisture'],
            'nitrogen': result['soil']['nitrogen'],
            'budget': result['budget'],
            'cost': result['costs']['total'],
            'rain': result['weather']['rain'],
            'temp': result['weather']['temperature'],
            'stage': result['crop'].get('stage', 'N/A')
        })

        status = "OK"
        if result['crop']['ndvi'] < 0.3:
            status = "CRITICAL"
        elif result['crop']['ndvi'] < 0.5:
            status = "STRESSED"

        print(f"Week {week:2d} [{result['crop'].get('stage', 'N/A'):<12s}]: " +
              f"NDVI={result['crop']['ndvi']:.3f} [{status:<8s}], " +
              f"Moisture={result['soil']['moisture']:5.1f}%, " +
              f"Budget=${result['budget']:7.2f}, " +
              f"Cost=${result['costs']['total']:5.2f}")

    # Harvest
    response = requests.get(f"{BASE_URL}/api/harvest", params={"session_id": session_id})
    harvest = response.json()

    # Analysis
    print("\n" + "=" * 80)
    print("RESULTS ANALYSIS")
    print("=" * 80)

    ndvi_trend = "INCREASING" if results[-1]['ndvi'] > results[0]['ndvi'] else "DECREASING"
    ndvi_max = max(r['ndvi'] for r in results)
    ndvi_min = min(r['ndvi'] for r in results)
    ndvi_final = results[-1]['ndvi']

    print(f"\nNDVI Evolution:")
    print(f"  Initial: {results[0]['ndvi']:.3f}")
    print(f"  Maximum: {ndvi_max:.3f}")
    print(f"  Final: {ndvi_final:.3f}")
    print(f"  Trend: {ndvi_trend}")

    if ndvi_final < 0.3:
        print(f"  STATUS: CROP FAILURE")
    elif ndvi_final < 0.5:
        print(f"  STATUS: POOR PERFORMANCE")
    elif ndvi_final < 0.7:
        print(f"  STATUS: MODERATE")
    else:
        print(f"  STATUS: GOOD")

    total_costs = initial_budget - results[-1]['budget']

    print(f"\nEconomics:")
    print(f"  Yield: {harvest['yield']:.2f} t/ha")
    print(f"  Revenue: ${harvest['revenue']:.2f}")
    print(f"  Total costs: ${total_costs:.2f}")
    print(f"  Profit: ${harvest['profit']:.2f}")
    print(f"  Budget remaining: ${results[-1]['budget']:.2f}")

    if budget_exhausted_week:
        print(f"  WARNING: Budget exhausted at week {budget_exhausted_week}")

    print(f"\nRating: {harvest['stars']}/5 stars")
    print(f"Sustainability: {harvest['sustainability_score']:.1f}/100")

    # Identify problems
    problems = []

    if ndvi_final < 0.4:
        problems.append("NDVI too low - crop failure")

    if ndvi_trend == "DECREASING" and ndvi_final < 0.5:
        problems.append("NDVI declining - chronic stress")

    if budget_exhausted_week and budget_exhausted_week < 10:
        problems.append(f"Budget exhausted too early (week {budget_exhausted_week})")

    if harvest['profit'] < 0:
        problems.append("Negative profit - economically unviable")

    if total_costs > initial_budget * 0.9:
        problems.append("Very high costs (>90% of budget)")

    if problems:
        print(f"\nPROBLEMS IDENTIFIED:")
        for i, problem in enumerate(problems, 1):
            print(f"  {i}. {problem}")
    else:
        print(f"\nNo major problems - scenario playable")

    return {
        'region': region_name,
        'crop': crop_type,
        'ndvi_final': ndvi_final,
        'ndvi_trend': ndvi_trend,
        'yield': harvest['yield'],
        'profit': harvest['profit'],
        'stars': harvest['stars'],
        'problems': problems,
        'budget_exhausted_week': budget_exhausted_week
    }


# Test scenarios
print("=" * 80)
print("GAMEPLAY ANALYSIS - TESTING MULTIPLE SCENARIOS")
print("=" * 80)

scenarios_to_test = [
    # Humid tropical (should work with Loam)
    ("Yaounde, Cameroun", 3.87, 11.52, "spring_2024", "yaounde_cameroun", "maize"),

    # Arid Sahel (high irrigation cost)
    ("Kano, Nigeria", 12.0, 8.52, "spring_2024", "kano_nigeria", "sorghum"),

    # Temperate
    ("Beauce, France", 48.44, 1.48, "spring_2024", "beauce_france", "wheat"),

    # Monsoon (rice should work)
    ("Dhaka, Bangladesh", 23.81, 90.41, "spring_2024", "dhaka_bangladesh", "rice"),
]

summary = []

for scenario in scenarios_to_test:
    try:
        result = test_scenario(*scenario)
        summary.append(result)
    except Exception as e:
        print(f"\nERROR testing scenario {scenario[0]}: {e}")
        summary.append({
            'region': scenario[0],
            'crop': scenario[5],
            'error': str(e)
        })

# Global summary
print("\n\n")
print("=" * 80)
print("GLOBAL SUMMARY - ALL SCENARIOS")
print("=" * 80)

print(f"\n{'Region':<25s} {'Crop':<10s} {'NDVI':<8s} {'Yield':<8s} {'Profit':<10s} {'Stars':<6s} {'Status'}")
print("-" * 80)

for s in summary:
    if 'error' in s:
        print(f"{s['region']:<25s} {s['crop']:<10s} ERROR: {s['error']}")
    else:
        status = "OK" if not s['problems'] else f"{len(s['problems'])} issues"
        print(f"{s['region']:<25s} {s['crop']:<10s} {s['ndvi_final']:<8.3f} {s['yield']:<8.2f} ${s['profit']:<9.2f} {s['stars']}/5   {status}")

# Count problems
playable = sum(1 for s in summary if 'error' not in s and not s['problems'])
problematic = sum(1 for s in summary if 'error' not in s and s['problems'])

print(f"\n\nPlayability: {playable}/{len(scenarios_to_test)} scenarios fully playable")
print(f"Problematic: {problematic}/{len(scenarios_to_test)} scenarios have issues")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
