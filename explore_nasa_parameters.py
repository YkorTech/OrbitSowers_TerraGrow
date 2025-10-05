# -*- coding: utf-8 -*-
"""
Exploration complète des paramètres NASA POWER API
Affiche TOUS les paramètres disponibles
"""

import requests
import json

print("="*70)
print("EXPLORATION NASA POWER API - TOUS LES PARAMETRES DISPONIBLES")
print("="*70)

# NASA POWER met à disposition la liste complète des paramètres
# Documentation: https://power.larc.nasa.gov/docs/services/api/

print("\n[INFO] NASA POWER propose 3 communautés de données:")
print("  - AG  : Agriculture (notre cas)")
print("  - RE  : Renewable Energy (énergie solaire/éolienne)")
print("  - SB  : Sustainable Buildings (bâtiments)")

print("\n" + "="*70)
print("PARAMETRES AGRICULTURE (Community: AG)")
print("="*70)

# Faire un appel test pour voir la structure
url = "https://power.larc.nasa.gov/api/temporal/daily/point"

# Appel avec TOUS les paramètres agriculture possibles
all_ag_params = "T2M,T2M_MAX,T2M_MIN,T2MDEW,T2MWET,TS,T2M_RANGE,RH2M,PRECTOTCORR,PS,WS10M,WS10M_MAX,WS10M_MIN,WS50M,WS50M_MAX,WS50M_MIN,ALLSKY_SFC_SW_DWN,ALLSKY_SFC_LW_DWN,ALLSKY_SFC_PAR_TOT,CLRSKY_SFC_SW_DWN"

params = {
    "parameters": all_ag_params,
    "community": "AG",
    "longitude": 11.52,
    "latitude": 3.87,
    "start": "20240101",
    "end": "20240101",  # Un seul jour pour test
    "format": "JSON"
}

print("\n[1] Appel API avec TOUS les paramètres AG...")

try:
    response = requests.get(url, params=params, timeout=30)

    if response.status_code == 200:
        data = response.json()

        print("\n[OK] Réponse reçue !")

        if 'parameters' in data:
            params_info = data['parameters']

            print(f"\n{'='*70}")
            print(f"TOTAL: {len(params_info)} paramètres disponibles")
            print(f"{'='*70}\n")

            # Catégoriser les paramètres
            temperature_params = {}
            precipitation_params = {}
            wind_params = {}
            radiation_params = {}
            humidity_params = {}
            pressure_params = {}
            other_params = {}

            for param_code, param_info in params_info.items():
                longname = param_info.get('longname', 'N/A')
                units = param_info.get('units', 'N/A')

                if 'Temperature' in longname or 'T2M' in param_code:
                    temperature_params[param_code] = param_info
                elif 'Precipitation' in longname or 'PREC' in param_code:
                    precipitation_params[param_code] = param_info
                elif 'Wind' in longname or 'WS' in param_code:
                    wind_params[param_code] = param_info
                elif 'Radiation' in longname or 'SW' in param_code or 'LW' in param_code or 'PAR' in param_code:
                    radiation_params[param_code] = param_info
                elif 'Humidity' in longname or 'RH' in param_code or 'DEW' in param_code:
                    humidity_params[param_code] = param_info
                elif 'Pressure' in longname or 'PS' in param_code:
                    pressure_params[param_code] = param_info
                else:
                    other_params[param_code] = param_info

            # Afficher par catégorie
            print("🌡️  TEMPERATURE (" + str(len(temperature_params)) + " paramètres)")
            print("-"*70)
            for code, info in temperature_params.items():
                print(f"  {code:20} | {info['longname']}")
                print(f"  {'':20} | Unité: {info['units']}")
                print()

            print("\n💧 PRECIPITATION & HUMIDITE (" + str(len(precipitation_params) + len(humidity_params)) + " paramètres)")
            print("-"*70)
            for code, info in {**precipitation_params, **humidity_params}.items():
                print(f"  {code:20} | {info['longname']}")
                print(f"  {'':20} | Unité: {info['units']}")
                print()

            print("\n💨 VENT (" + str(len(wind_params)) + " paramètres)")
            print("-"*70)
            for code, info in wind_params.items():
                print(f"  {code:20} | {info['longname']}")
                print(f"  {'':20} | Unité: {info['units']}")
                print()

            print("\n☀️  RADIATION SOLAIRE (" + str(len(radiation_params)) + " paramètres)")
            print("-"*70)
            for code, info in radiation_params.items():
                print(f"  {code:20} | {info['longname']}")
                print(f"  {'':20} | Unité: {info['units']}")
                print()

            print("\n🌍 PRESSION & AUTRES (" + str(len(pressure_params) + len(other_params)) + " paramètres)")
            print("-"*70)
            for code, info in {**pressure_params, **other_params}.items():
                print(f"  {code:20} | {info['longname']}")
                print(f"  {'':20} | Unité: {info['units']}")
                print()

            # Obtenir les valeurs pour voir des exemples
            if 'properties' in data and 'parameter' in data['properties']:
                param_data = data['properties']['parameter']

                print("\n" + "="*70)
                print("EXEMPLE DE DONNEES (Yaoundé, 01/01/2024)")
                print("="*70 + "\n")

                for param_code in sorted(param_data.keys()):
                    if '20240101' in param_data[param_code]:
                        value = param_data[param_code]['20240101']
                        info = params_info[param_code]
                        print(f"{param_code:20} : {value:8.2f} {info['units']:10} | {info['longname']}")

        # Sauvegarder dans un fichier
        print("\n" + "="*70)
        print("SAUVEGARDE")
        print("="*70)

        with open('nasa_power_all_parameters.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print("\n[OK] Tous les paramètres sauvegardés dans:")
        print("     nasa_power_all_parameters.json")

    else:
        print(f"\n[ERREUR] Status: {response.status_code}")

        # Essayer avec moins de paramètres
        print("\n[2] Essai avec paramètres de base uniquement...")
        params['parameters'] = "T2M,PRECTOTCORR,RH2M"
        response2 = requests.get(url, params=params, timeout=30)

        if response2.status_code == 200:
            data2 = response2.json()
            if 'parameters' in data2:
                print(f"\n[OK] {len(data2['parameters'])} paramètres de base disponibles:")
                for code, info in data2['parameters'].items():
                    print(f"  - {code}: {info['longname']} ({info['units']})")

except Exception as e:
    print(f"\n[ERREUR] {e}")

print("\n" + "="*70)
print("DOCUMENTATION COMPLETE")
print("="*70)
print("\nPour plus de détails:")
print("  https://power.larc.nasa.gov/docs/services/api/application/parameters/")
