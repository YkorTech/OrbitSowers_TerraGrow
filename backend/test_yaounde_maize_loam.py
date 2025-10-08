"""
Test rapide : Mais a Yaounde avec sol Loam (drainage ameliore)
Compare avec les attentes du GAME_LOGIC_DESIGN.md
"""

import requests
import sys

BASE_URL = "http://localhost:5000"

print("=" * 70)
print("TEST MAIS A YAOUNDE - SOL LOAM (drainage ameliore)")
print("=" * 70)

# Initialize game
print("\n[1] Initialisation partie - Yaounde Spring 2024 - Mais")
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

print(f"  Region: {game_data['state']['region']['name']}")
print(f"  Crop: {game_data['state']['crop']['name']}")
print(f"  Soil: {game_data['state']['soil']['name']} [drainage={game_data['state']['soil']['type']}]")

# Strategy: Optimal fertilization according to phenological stages
fertilization = {
    1: 10, 2: 10, 3: 10,      # Germination: 20% total
    4: 25, 5: 30, 6: 25, 7: 20,  # Vegetative: 50% total (PIC)
    8: 15, 9: 15, 10: 10,     # Flowering: 25% total
    11: 5, 12: 5              # Maturation: 5% total
}

print("\n[2] Simulation 12 semaines avec fertilisation optimale")
print("-" * 70)

max_ndvi = 0
moisture_history = []

for week in range(1, 13):
    state_response = requests.get(f"{BASE_URL}/api/state", params={"session_id": session_id})
    current_state = state_response.json()

    current_moisture = current_state['soil']['moisture']

    # Adaptive irrigation
    if current_moisture < 40:
        irrigation = 30
    elif current_moisture < 55:
        irrigation = 15
    else:
        irrigation = 0

    fertilizer = fertilization[week]

    action_data = {
        "session_id": session_id,
        "irrigation": irrigation,
        "fertilizer": fertilizer
    }

    response = requests.post(f"{BASE_URL}/api/action", json=action_data)
    result = response.json()

    if 'error' in result:
        print(f"Week {week}: ERROR - {result['error']}")
        sys.exit(1)

    ndvi = result['crop']['ndvi']
    moisture = result['soil']['moisture']
    moisture_history.append(moisture)

    if ndvi > max_ndvi:
        max_ndvi = ndvi

    print(f"Week {week:2d} [{result['crop']['stage']:<12s}]: NDVI={ndvi:.3f}, Moisture={moisture:.1f}%, Rain={result['weather']['rain']:.1f}mm")

# Harvest
print("\n[3] Recolte - Resultats finaux")
print("=" * 70)

response = requests.get(f"{BASE_URL}/api/harvest", params={"session_id": session_id})
harvest = response.json()

print(f"\nRESULTATS:")
print(f"  NDVI max atteint: {max_ndvi:.3f}")
print(f"  NDVI final: {harvest['ndvi_history'][-1]:.3f}")
print(f"  Rendement: {harvest['yield']:.2f} t/ha")
print(f"  Revenu: ${harvest['revenue']:.2f}")
print(f"  Couts: ${harvest['total_costs']:.2f}")
print(f"  PROFIT: ${harvest['profit']:.2f}")
print(f"  Rating: {harvest['stars']}/5 etoiles")

# Check moisture saturation
saturated_weeks = sum(1 for m in moisture_history if m >= 95)
print(f"\n  Semaines saturees (>95%): {saturated_weeks}/12")

# Compare with expectations
print("\n[4] COMPARAISON AVEC GAME_LOGIC_DESIGN.md")
print("=" * 70)

expected_ndvi = 0.75
expected_yield = 7.5
expected_profit_min = 800

print(f"\nAttendu selon document:")
print(f"  NDVI cible: {expected_ndvi:.2f}")
print(f"  Rendement cible: {expected_yield} t/ha")
print(f"  Profit minimal: ${expected_profit_min}")

print(f"\nResultat obtenu:")
print(f"  NDVI max: {max_ndvi:.3f} [{('OK' if max_ndvi >= expected_ndvi else 'TROP BAS')}]")
print(f"  Rendement: {harvest['yield']:.2f} t/ha [{('OK' if harvest['yield'] >= expected_yield else 'TROP BAS')}]")
print(f"  Profit: ${harvest['profit']:.2f} [{('OK' if harvest['profit'] >= expected_profit_min else 'TROP BAS')}]")

# Verdict
if max_ndvi >= expected_ndvi and harvest['yield'] >= expected_yield:
    print("\n[SUCCESS] Objectifs atteints ! Sol Loam resout le probleme de drainage.")
elif max_ndvi >= 0.65:
    print("\n[PARTIAL] Amelioration significative mais pas encore optimal.")
    print("  Suggestion: Peut-etre augmenter drainage_rate de Loam a 0.70 ?")
else:
    print("\n[FAIL] Probleme de drainage persiste. Investiguer davantage.")

print("\n" + "=" * 70)
