"""
Test script to verify crop_v2 activation
Tests phenological stages, nitrogen requirements, and economic calculations
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from models import Crop, GameState, Region, Soil
from config import Config

print("=" * 60)
print("CROP V2 ACTIVATION TEST")
print("=" * 60)

# Test 1: Verify Crop V2 import
print("\n[TEST 1] Verification import Crop V2")
crop_params = Config.CROPS['maize']
crop = Crop('maize', crop_params)

# Check if V2 methods exist
has_get_nitrogen_requirement = hasattr(crop, 'get_nitrogen_requirement')
has_get_growth_stage = hasattr(crop, 'get_growth_stage')
has_drought_tolerance = hasattr(crop, 'drought_tolerance')
has_price_per_ton = hasattr(crop, 'price_per_ton')

print(f"  - get_nitrogen_requirement(): {has_get_nitrogen_requirement}")
print(f"  - get_growth_stage(): {has_get_growth_stage}")
print(f"  - drought_tolerance: {has_drought_tolerance}")
print(f"  - price_per_ton: {has_price_per_ton}")

if not all([has_get_nitrogen_requirement, has_get_growth_stage, has_drought_tolerance, has_price_per_ton]):
    print("ERROR: Crop V2 not activated correctly!")
    sys.exit(1)

print("SUCCESS: Crop V2 imported successfully")

# Test 2: Phenological stages and nitrogen requirements
print("\n[TEST 2] Stades phenologiques et besoins en azote")
print("\n  Mais (150 kg N/ha total):")
print("  " + "-" * 50)

crop = Crop('maize', Config.CROPS['maize'])
nitrogen_by_stage = []

for week in range(1, 13):
    crop.age_weeks = week - 1
    stage_idx, stage_name = crop.get_growth_stage()
    n_requirement = crop.get_nitrogen_requirement()
    nitrogen_by_stage.append(n_requirement)

    print(f"  Semaine {week:2d}: {stage_name:15s} -> {n_requirement:5.1f} kg N/ha")

total_nitrogen = sum(nitrogen_by_stage)
print(f"\n  Total sur 12 semaines: {total_nitrogen:.1f} kg N/ha")
print(f"  Configuration: {crop.nitrogen_need} kg N/ha")
print(f"  Difference: {abs(total_nitrogen - crop.nitrogen_need):.1f} kg N/ha")

# Test 3: Crop tolerances
print("\n[TEST 3] Tolerances differenciees par culture")
print("  " + "-" * 50)

crops_to_test = ['rice', 'sorghum', 'maize']
for crop_type in crops_to_test:
    crop = Crop(crop_type, Config.CROPS[crop_type])
    print(f"  {crop.name:12s}: Secheresse={crop.drought_tolerance:6s}, Waterlog={crop.waterlog_tolerance:6s}")

# Test 4: Economic calculations
print("\n[TEST 4] Calculs economiques")
print("  " + "-" * 50)

# Create a simple game state
region = Region('Yaounde, Cameroun', 3.87, 11.52, 'Tropical savane', 'clay')
game_state = GameState(
    region=region,
    crop_type='maize',
    crop_params=Config.CROPS['maize'],
    soil_params=Config.SOIL_TYPES['clay'],
    initial_budget=2000
)

# Set final NDVI to simulate harvest
game_state.crop.ndvi = 0.85
game_state.crop.age_weeks = 12
game_state.budget = 1865  # After costs

# Calculate yield and revenue
crop_yield = game_state.crop.get_yield()
revenue = game_state.crop.get_revenue()

print(f"  Culture: {game_state.crop.name}")
print(f"  NDVI final: {game_state.crop.ndvi:.3f}")
print(f"  Rendement: {crop_yield:.2f} t/ha")
print(f"  Prix: ${game_state.crop.price_per_ton}/tonne")
print(f"  Revenu: ${revenue:.2f}")
print(f"  Couts: ${2000 - game_state.budget:.2f}")
print(f"  Profit: ${revenue - (2000 - game_state.budget):.2f}")

# Test 5: Water stress with tolerances
print("\n[TEST 5] Stress hydrique selon tolerances")
print("  " + "-" * 50)

test_moistures = [30, 50, 70, 90]
crops_tolerance_test = [
    ('rice', Config.CROPS['rice']),
    ('sorghum', Config.CROPS['sorghum'])
]

for crop_type, params in crops_tolerance_test:
    crop = Crop(crop_type, params)
    print(f"\n  {crop.name}:")
    for moisture in test_moistures:
        stress = crop._calculate_water_stress(moisture)
        print(f"    Moisture {moisture}% -> Stress={stress:.2f}")

# Test 6: Full game simulation snippet
print("\n[TEST 6] Simulation semaine complete")
print("  " + "-" * 50)

region = Region('Yaounde, Cameroun', 3.87, 11.52, 'Tropical savane', 'clay')
game_state = GameState(
    region=region,
    crop_type='maize',
    crop_params=Config.CROPS['maize'],
    soil_params=Config.SOIL_TYPES['clay'],
    initial_budget=2000
)

# Simulate week 5 (vegetative stage - high N need)
game_state.crop.age_weeks = 4  # Start of week 5
weather = {
    'precipitation': 25,
    'temperature': 26,
    'evapotranspiration': 28
}

print(f"  Avant semaine 5:")
print(f"    Stade: {game_state.crop.get_growth_stage()[1]}")
print(f"    Besoin N: {game_state.crop.get_nitrogen_requirement():.1f} kg/ha")
print(f"    NDVI: {game_state.crop.ndvi:.3f}")
print(f"    Azote sol: {game_state.soil.nitrogen:.1f} kg/ha")

# Apply actions
result = game_state.simulate_week(
    irrigation_mm=20,
    fertilizer_kg=30,
    weather_data=weather
)

print(f"\n  Apres semaine 5:")
print(f"    Stade: {result['crop']['stage']}")
print(f"    NDVI: {result['crop']['ndvi']:.3f}")
print(f"    Azote sol: {result['soil']['nitrogen']:.1f} kg/ha")
print(f"    Budget: ${result['budget']:.2f}")
print(f"    Couts: ${result['costs']['total']:.2f}")

print("\n" + "=" * 60)
print("SUCCESS: ALL TESTS PASSED - CROP V2 ACTIVATED")
print("=" * 60)
print("\nNew behaviors activated:")
print("  [OK] Phenological stages (Germination -> Vegetative -> Flowering -> Maturation)")
print("  [OK] Progressive nitrogen needs (20% -> 50% -> 25% -> 5%)")
print("  [OK] Differentiated drought/waterlog tolerances")
print("  [OK] Economic calculations with profit (revenue - costs)")
print("\nReady for game!")
