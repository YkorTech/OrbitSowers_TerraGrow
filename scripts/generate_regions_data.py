# -*- coding: utf-8 -*-
"""
Script pour générer les données des 15 régions populaires
À exécuter AVANT le hackathon pour préparer les données
"""

import requests
import json
import os
from datetime import datetime, timedelta
import time

# Configuration
REGIONS = {
    'yaounde_cameroun': {
        'name': 'Yaoundé, Cameroun',
        'lat': 3.87,
        'lon': 11.52,
        'climate': 'Tropical savane',
        'soil_type': 'clay'
    },
    'maroua_cameroun': {
        'name': 'Maroua, Cameroun',
        'lat': 10.6,
        'lon': 14.3,
        'climate': 'Sahel semi-aride',
        'soil_type': 'sandy'
    },
    'douala_cameroun': {
        'name': 'Douala, Cameroun',
        'lat': 4.05,
        'lon': 9.7,
        'climate': 'Tropical humide',
        'soil_type': 'clay'
    },
    'montreal_canada': {
        'name': 'Montréal, Canada',
        'lat': 45.5,
        'lon': -73.6,
        'climate': 'Continental humide',
        'soil_type': 'loam'
    },
    'nairobi_kenya': {
        'name': 'Nairobi, Kenya',
        'lat': -1.28,
        'lon': 36.82,
        'climate': 'Subtropical montagnard',
        'soil_type': 'loam'
    },
    'kano_nigeria': {
        'name': 'Kano, Nigeria',
        'lat': 12.0,
        'lon': 8.52,
        'climate': 'Sahel',
        'soil_type': 'sandy'
    },
    'addis_ethiopie': {
        'name': 'Addis-Abeba, Éthiopie',
        'lat': 9.03,
        'lon': 38.74,
        'climate': 'Subtropical montagnard',
        'soil_type': 'loam'
    },
    'punjab_inde': {
        'name': 'Punjab, Inde',
        'lat': 30.73,
        'lon': 76.78,
        'climate': 'Semi-aride chaud',
        'soil_type': 'loam'
    },
    'saopaulo_bresil': {
        'name': 'São Paulo, Brésil',
        'lat': -23.55,
        'lon': -46.63,
        'climate': 'Subtropical humide',
        'soil_type': 'clay'
    },
    'iowa_usa': {
        'name': 'Iowa, USA',
        'lat': 41.88,
        'lon': -93.1,
        'climate': 'Continental humide',
        'soil_type': 'loam'
    },
    'beauce_france': {
        'name': 'Beauce, France',
        'lat': 48.44,
        'lon': 1.48,
        'climate': 'Océanique tempéré',
        'soil_type': 'loam'
    },
    'dhaka_bangladesh': {
        'name': 'Dhaka, Bangladesh',
        'lat': 23.81,
        'lon': 90.41,
        'climate': 'Tropical mousson',
        'soil_type': 'clay'
    },
    'pampas_argentine': {
        'name': 'Pampas, Argentine',
        'lat': -34.6,
        'lon': -58.38,
        'climate': 'Subtropical humide',
        'soil_type': 'loam'
    },
    'prairies_canada': {
        'name': 'Prairies, Canada',
        'lat': 50.45,
        'lon': -104.62,
        'climate': 'Continental semi-aride',
        'soil_type': 'loam'
    },
    'garoua_cameroun': {
        'name': 'Garoua, Cameroun',
        'lat': 9.3,
        'lon': 13.4,
        'climate': 'Sahel',
        'soil_type': 'sandy'
    }
}


def get_nasa_power_data(lat, lon, days=90):
    """
    Récupère les données NASA POWER pour une localisation
    """
    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    # Date range (derniers 90 jours)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    params = {
        "parameters": "T2M,PRECTOTCORR,RH2M",
        "community": "AG",
        "longitude": lon,
        "latitude": lat,
        "start": start_date.strftime("%Y%m%d"),
        "end": end_date.strftime("%Y%m%d"),
        "format": "JSON"
    }

    print(f"  Appel NASA POWER API...")

    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()

        if 'properties' not in data or 'parameter' not in data['properties']:
            print(f"  [ERREUR] Structure invalide")
            return None

        return data['properties']['parameter']

    except Exception as e:
        print(f"  [ERREUR] {e}")
        return None


def aggregate_weekly(daily_data):
    """
    Agrège les données quotidiennes en données hebdomadaires
    """
    temps = daily_data.get('T2M', {})
    precip = daily_data.get('PRECTOTCORR', {})
    humidity = daily_data.get('RH2M', {})

    dates = sorted(temps.keys())

    weekly = []
    for i in range(0, len(dates), 7):
        week_dates = dates[i:i+7]

        if len(week_dates) < 7:
            continue

        avg_temp = sum(temps[d] for d in week_dates) / len(week_dates)
        total_rain = sum(precip[d] for d in week_dates)
        avg_humidity = sum(humidity[d] for d in week_dates) / len(week_dates)

        # Calculer ET simplifié
        et = 0.0023 * (avg_temp + 17.8) * (100 - avg_humidity) / 10 * 7

        weekly.append({
            'week': len(weekly) + 1,
            'temperature': round(avg_temp, 1),
            'precipitation': round(total_rain, 1),
            'humidity': round(avg_humidity, 1),
            'evapotranspiration': round(et, 1)
        })

    return weekly[:12]  # Limiter à 12 semaines


def generate_region_file(region_id, region_info):
    """
    Génère un fichier JSON pour une région
    """
    print(f"\n{'='*60}")
    print(f"Région: {region_info['name']}")
    print(f"Coordonnées: ({region_info['lat']}, {region_info['lon']})")
    print(f"{'='*60}")

    # Récupérer données NASA
    daily_data = get_nasa_power_data(region_info['lat'], region_info['lon'])

    if not daily_data:
        print(f"  [ÉCHEC] Impossible de récupérer les données")
        return False

    # Agréger en semaines
    weekly_data = aggregate_weekly(daily_data)

    print(f"  [OK] {len(weekly_data)} semaines de données générées")

    # Créer le fichier JSON
    output = {
        'name': region_info['name'],
        'lat': region_info['lat'],
        'lon': region_info['lon'],
        'climate': region_info['climate'],
        'soil_type': region_info['soil_type'],
        'weather_data': weekly_data,
        'generated_at': datetime.now().isoformat(),
        'source': 'NASA POWER API'
    }

    # Sauvegarder
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'regions')
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, f"{region_id}.json")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"  [SAUVEGARDE] {output_file}")

    return True


def main():
    """
    Génère les fichiers pour toutes les régions
    """
    print("\n" + "="*60)
    print("GENERATION DES DONNEES DES 15 REGIONS")
    print("="*60)

    total = len(REGIONS)
    success = 0

    for i, (region_id, region_info) in enumerate(REGIONS.items(), 1):
        print(f"\n[{i}/{total}] Traitement: {region_info['name']}")

        if generate_region_file(region_id, region_info):
            success += 1
            print(f"  [SUCCESS]")
        else:
            print(f"  [FAILED]")

        # Pause pour respecter les rate limits
        if i < total:
            print("  Pause 2 secondes...")
            time.sleep(2)

    # Résumé
    print("\n" + "="*60)
    print(f"TERMINE: {success}/{total} régions générées avec succès")
    print("="*60)

    if success == total:
        print("\nTOUTES LES DONNEES SONT PRETES !")
        print("Vous pouvez maintenant lancer le jeu.")
    else:
        print(f"\nATTENTION: {total - success} régions ont échoué")
        print("Le jeu utilisera l'API en temps réel pour ces régions.")


if __name__ == "__main__":
    main()
