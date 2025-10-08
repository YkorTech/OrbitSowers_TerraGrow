"""
Test du flux des semaines - Verification que week 12 fonctionne correctement
"""

import requests

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("TEST DU FLUX DES SEMAINES")
print("=" * 80)

# Initialize game
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

print(f"\nRegion: {game_data['state']['region']['name']}")
print(f"Initial state: week = {game_data['state']['week']}")
print(f"Expected: week = 1 (next week to play)\n")

print("Simulating 12 weeks...\n")

for week in range(1, 13):
    # Minimal strategy (just to test week flow)
    irrigation = 10
    fertilizer = 15

    action_data = {
        "session_id": session_id,
        "irrigation": irrigation,
        "fertilizer": fertilizer
    }

    response = requests.post(f"{BASE_URL}/api/action", json=action_data)
    result = response.json()

    if 'error' in result:
        print(f"\n❌ ERROR at week {week}: {result['error']}")
        break

    week_played = result.get('week_played', 'N/A')
    next_week = result.get('week', 'N/A')
    is_complete = result.get('is_complete', False)

    print(f"Validated week {week_played:2d} → Next week: {next_week:2d} | is_complete: {is_complete}")

    # Verify logic
    if week_played != week:
        print(f"   ⚠️  WARNING: Expected week_played={week}, got {week_played}")

    if week < 12:
        if is_complete:
            print(f"   ❌ ERROR: is_complete should be False before week 12!")
        if next_week != week + 1:
            print(f"   ⚠️  WARNING: Expected next_week={week+1}, got {next_week}")
    else:  # week == 12
        if not is_complete:
            print(f"   ❌ ERROR: is_complete should be True after week 12!")
        if next_week != 13:
            print(f"   ⚠️  WARNING: Expected next_week=13 after week 12, got {next_week}")

print("\n" + "=" * 80)
print("VERIFICATION FINALE")
print("=" * 80)

# Try to harvest
response = requests.get(f"{BASE_URL}/api/harvest", params={"session_id": session_id})
harvest = response.json()

if 'error' in harvest:
    print(f"❌ Harvest ERROR: {harvest['error']}")
else:
    print(f"✅ Harvest successful!")
    print(f"   Yield: {harvest['yield']:.2f} t/ha")
    print(f"   Profit: ${harvest['profit']:.2f}")

# Try to validate week 13 (should fail)
print(f"\nTrying to validate week 13 (should fail)...")
action_data = {
    "session_id": session_id,
    "irrigation": 10,
    "fertilizer": 15
}
response = requests.post(f"{BASE_URL}/api/action", json=action_data)
result = response.json()

if 'error' in result:
    if 'already completed' in result['error']:
        print(f"✅ Correctly blocked: {result['error']}")
    else:
        print(f"❌ Unexpected error: {result['error']}")
else:
    print(f"❌ ERROR: Should not allow validation after week 12!")

print("\n" + "=" * 80)
print("TEST TERMINÉ")
print("=" * 80)
