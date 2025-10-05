# -*- coding: utf-8 -*-
import requests
import json

# Test simple - Meteo Yaounde
print("=" * 60)
print("Test connexion NASA POWER API")
print("=" * 60)

url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "T2M,PRECTOTCORR,RH2M",
    "community": "AG",
    "longitude": 11.52,
    "latitude": 3.87,
    "start": "20240101",
    "end": "20240107",  # Juste 1 semaine pour test
    "format": "JSON"
}

print("\n[1] Appel API NASA POWER...")
print(f"URL: {url}")
print(f"Localisation: Yaounde (3.87N, 11.52E)")

# Envoi de la requête
response = requests.get(url, params=params)

# Vérification
if response.status_code == 200:
    data = response.json()
    print("\n[OK] Requete reussie !")
    print(f"Status: {response.status_code}")

    # Afficher les données
    if 'properties' in data and 'parameter' in data['properties']:
        params_data = data['properties']['parameter']
        print("\n[2] Donnees recues:")
        print(f"  - Temperature (T2M): {len(params_data.get('T2M', {}))} jours")
        print(f"  - Precipitation (PRECTOTCORR): {len(params_data.get('PRECTOTCORR', {}))} jours")
        print(f"  - Humidite (RH2M): {len(params_data.get('RH2M', {}))} jours")

        # Exemple de données
        print("\n[3] Exemple (1er jour):")
        temps = params_data.get('T2M', {})
        if temps:
            first_date = list(temps.keys())[0]
            print(f"  Date: {first_date}")
            print(f"  Temperature: {temps[first_date]} C")
            print(f"  Precipitation: {params_data['PRECTOTCORR'][first_date]} mm")
            print(f"  Humidite: {params_data['RH2M'][first_date]} %")

    print("\n" + "=" * 60)
    print("SUCCESS - L'API NASA fonctionne !")
    print("=" * 60)
else:
    print(f"\n[ERREUR] Status: {response.status_code}")
    print(f"Reponse: {response.text[:200]}")
