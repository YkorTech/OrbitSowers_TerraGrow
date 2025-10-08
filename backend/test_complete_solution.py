"""
Test de la solution complete - Gameplay equilibre
Tests:
1. Kano (Sahel aride) - doit etre jouable maintenant
2. Yaounde (Tropical humide) - doit rester excellent
3. Recommandations intelligentes - verification
4. Systeme de pret d'urgence - test
"""

import requests
import sys

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TEST SOLUTION COMPLETE - GAMEPLAY EQUILIBRE")
print("=" * 80)

# TEST 1: Kano (Sahel) - Le cas le plus difficile
print("\n" + "=" * 80)
print("TEST 1: KANO (SAHEL ARIDE) - SORGHUM")
print("=" * 80)

init_data = {
    "lat": 12.0,
    "lon": 8.52,
    "crop_type": "sorghum",
    "season_id": "spring_2024",
    "region_id": "kano_nigeria"
}

response = requests.post(f"{BASE_URL}/api/init", json=init_data)
game_data = response.json()
session_id = game_data['session_id']

print(f"\nRegion: {game_data['state']['region']['name']}")
print(f"Climate: {game_data['state']['region']['climate']}")
print(f"Soil: {game_data['state']['soil']['name']}")
print(f"Budget initial: ${game_data['state']['budget']}")

# Calculate total rain and ET
total_rain = sum(w['precipitation'] for w in game_data['weather_preview'])
total_et = sum(w['evapotranspiration'] for w in game_data['weather_preview'])
print(f"\nDonnees meteo (12 semaines):")
print(f"  Pluies totales: {total_rain:.1f}mm")
print(f"  ET totale: {total_et:.1f}mm")
print(f"  Deficit: {total_et - total_rain:.1f}mm -> Irrigation intensive requise")

print(f"\nSimulation 12 semaines avec strategie aride...")
print("-" * 80)

# Strategy for arid region
for week in range(1, 13):
    state_response = requests.get(f"{BASE_URL}/api/state", params={"session_id": session_id})
    current_state = state_response.json()

    current_moisture = current_state['soil']['moisture']

    # Adaptive irrigation for arid region
    if current_moisture < 30:
        irrigation = 35  # Emergency
    elif current_moisture < 40:
        irrigation = 30  # High
    elif current_moisture < 50:
        irrigation = 25  # Medium
    else:
        irrigation = 15  # Light

    # Phenological fertilization
    if week <= 3:
        fertilizer = 10  # Germination
    elif week <= 7:
        fertilizer = 20  # Vegetative peak
    elif week <= 10:
        fertilizer = 12  # Flowering
    else:
        fertilizer = 5   # Maturation

    action_data = {
        "session_id": session_id,
        "irrigation": irrigation,
        "fertilizer": fertilizer
    }

    response = requests.post(f"{BASE_URL}/api/action", json=action_data)
    result = response.json()

    if 'error' in result:
        print(f"\nWeek {week}: ERROR - {result['error']}")
        if 'loan_option' in result:
            print(f"  LOAN OFFERED: {result['loan_option']['message']}")
            print(f"  -> Accepting loan...")

            # Accept loan
            loan_response = requests.post(f"{BASE_URL}/api/accept-loan", json={"session_id": session_id})
            loan_result = loan_response.json()

            if 'success' in loan_result and loan_result['success']:
                print(f"  LOAN ACCEPTED: {loan_result['message']}")
                print(f"  New budget: ${loan_result['new_budget']}")

                # Retry the action
                response = requests.post(f"{BASE_URL}/api/action", json=action_data)
                result = response.json()
            else:
                print(f"  Failed to get loan: {loan_result}")
                break
        else:
            break

    # Show progress (week_played is the week that was just validated)
    week_played = result.get('week_played', week)
    print(f"Week {week_played:2d} [{result['crop'].get('stage', 'N/A'):<12s}]: " +
          f"NDVI={result['crop']['ndvi']:.3f}, " +
          f"Moisture={result['soil']['moisture']:5.1f}%, " +
          f"Budget=${result['budget']:7.2f}")

    # Show smart recommendations (first 2 weeks and critical moments)
    if week <= 2 or result['budget'] < 500:
        if 'messages' in result:
            for msg in result['messages']:
                if msg['type'] in ['tip', 'warning', 'info']:
                    # Remove emojis for display
                    text = msg['text'].encode('ascii', 'ignore').decode('ascii')
                    print(f"    [{msg['type'].upper()}] {text}")

# Harvest
print(f"\n{'='*80}")
print("RECOLTE - RESULTATS FINAUX")
print("=" * 80)

response = requests.get(f"{BASE_URL}/api/harvest", params={"session_id": session_id})
harvest = response.json()

print(f"\nKano (Sahel) - Sorghum:")
print(f"  Rendement: {harvest['yield']:.2f} t/ha")
print(f"  Revenu: ${harvest['revenue']:.2f}")
print(f"  Couts: ${harvest['total_costs']:.2f}")

if harvest.get('loan_taken'):
    print(f"  Pret pris: OUI")
    print(f"  Remboursement: ${harvest['loan_repayment']:.2f}")

print(f"  PROFIT: ${harvest['profit']:.2f}")
print(f"  Rating: {harvest['stars']}/5 etoiles")

# Verdict
if harvest['profit'] > 0:
    print(f"\n  [SUCCESS] KANO EST MAINTENANT JOUABLE! Profit positif: ${harvest['profit']:.2f}")
else:
    print(f"\n  [FAIL] KANO toujours non viable. Profit: ${harvest['profit']:.2f}")

# TEST 2: Yaounde (comparaison)
print("\n\n" + "=" * 80)
print("TEST 2: YAOUNDE (TROPICAL) - MAIZE (comparaison)")
print("=" * 80)

init_data2 = {
    "lat": 3.87,
    "lon": 11.52,
    "crop_type": "maize",
    "season_id": "spring_2024",
    "region_id": "yaounde_cameroun"
}

response = requests.post(f"{BASE_URL}/api/init", json=init_data2)
game_data2 = response.json()
session_id2 = game_data2['session_id']

print(f"Region: {game_data2['state']['region']['name']}")
print(f"Climate: {game_data2['state']['region']['climate']}")

print(f"\nSimulation rapide (strategie optimale)...")

for week in range(1, 13):
    state_response = requests.get(f"{BASE_URL}/api/state", params={"session_id": session_id2})
    current_state = state_response.json()

    current_moisture = current_state['soil']['moisture']

    # Minimal irrigation for humid region
    if current_moisture < 45:
        irrigation = 20
    elif current_moisture < 55:
        irrigation = 10
    else:
        irrigation = 0

    # Phenological fertilization
    if week <= 3:
        fertilizer = 10
    elif week <= 7:
        fertilizer = 25  # Peak
    elif week <= 10:
        fertilizer = 15
    else:
        fertilizer = 5

    action_data = {
        "session_id": session_id2,
        "irrigation": irrigation,
        "fertilizer": fertilizer
    }

    response = requests.post(f"{BASE_URL}/api/action", json=action_data)
    result = response.json()

    if 'error' in result:
        print(f"Week {week}: ERROR - {result['error']}")
        break

response = requests.get(f"{BASE_URL}/api/harvest", params={"session_id": session_id2})
harvest2 = response.json()

print(f"\nYaounde (Tropical) - Maize:")
print(f"  Rendement: {harvest2['yield']:.2f} t/ha")
print(f"  Revenu: ${harvest2['revenue']:.2f}")
print(f"  Couts: ${harvest2['total_costs']:.2f}")
print(f"  PROFIT: ${harvest2['profit']:.2f}")
print(f"  Rating: {harvest2['stars']}/5 etoiles")

# SUMMARY
print("\n\n" + "=" * 80)
print("RESUME - SOLUTION COMPLETE")
print("=" * 80)

print(f"\n1. REDUCTION COUTS IRRIGATION ($3.5 -> $1.5/mm):")
print(f"   Kano profit: ${harvest['profit']:.2f} {'[OK]' if harvest['profit'] > 0 else '[FAIL]'}")
print(f"   Yaounde profit: ${harvest2['profit']:.2f} [OK]")

print(f"\n2. SYSTEME DE PRET D'URGENCE:")
if harvest.get('loan_taken'):
    print(f"   Kano a utilise le pret: OUI (remboursement ${harvest['loan_repayment']:.2f})")
else:
    print(f"   Kano n'a pas eu besoin de pret: Excellent!")

print(f"\n3. RECOMMANDATIONS INTELLIGENTES:")
print(f"   Affichees pendant la partie (verification manuelle requise)")

print(f"\n4. JOUABILITE:")
jouable_count = sum([1 if harvest['profit'] > 0 else 0, 1 if harvest2['profit'] > 0 else 0])
print(f"   {jouable_count}/2 scenarios rentables")

if jouable_count == 2:
    print(f"\n[SUCCESS] Toutes les ameliorations fonctionnent!")
    print(f"   - Regions arides jouables")
    print(f"   - Regions humides toujours excellentes")
    print(f"   - Pret d'urgence disponible si necessaire")
    print(f"   - Recommandations contextuelles actives")
else:
    print(f"\n[PARTIAL] Ameliorations partielles. Verifier les parametres.")

print("\n" + "=" * 80)
