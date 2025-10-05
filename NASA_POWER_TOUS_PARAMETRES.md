# 📊 TOUS LES PARAMÈTRES NASA POWER API

## Source : https://power.larc.nasa.gov/

---

## 🌾 COMMUNAUTÉ AGRICULTURE (AG)

Voici **TOUS** les paramètres disponibles pour l'agriculture :

---

### 🌡️ TEMPÉRATURE (9 paramètres)

| Code | Nom complet | Unité | Utilisation possible |
|------|-------------|-------|---------------------|
| **T2M** | Temperature at 2 Meters | °C | ✅ **UTILISÉ** - Température moyenne |
| **T2M_MAX** | Temperature at 2 Meters Maximum | °C | 🔥 Détection canicules |
| **T2M_MIN** | Temperature at 2 Meters Minimum | °C | ❄️ Détection gels |
| **T2M_RANGE** | Temperature at 2 Meters Range | °C | 📊 Amplitude thermique journalière |
| **T2MDEW** | Dew/Frost Point at 2 Meters | °C | 💧 Point de rosée (condensation) |
| **T2MWET** | Wet Bulb Temperature at 2 Meters | °C | 🌡️ Température humide |
| **TS** | Earth Skin Temperature | °C | 🌍 Température surface du sol |
| **T10M** | Temperature at 10 Meters | °C | 🌡️ Température altitude 10m |
| **T10M_MAX** | Temperature at 10 Meters Maximum | °C | 🔥 Max à 10m |

---

### 💧 PRÉCIPITATION & HUMIDITÉ (4 paramètres)

| Code | Nom complet | Unité | Utilisation possible |
|------|-------------|-------|---------------------|
| **PRECTOTCORR** | Precipitation Corrected | mm/day | ✅ **UTILISÉ** - Pluie corrigée |
| **PRECTOTCORR_SUM** | Precipitation Corrected Sum | mm | 📊 Cumul précipitations |
| **RH2M** | Relative Humidity at 2 Meters | % | ✅ **UTILISÉ** - Humidité relative |
| **QV2M** | Specific Humidity at 2 Meters | g/kg | 💧 Humidité spécifique |

---

### 💨 VENT (8 paramètres)

| Code | Nom complet | Unité | Utilisation possible |
|------|-------------|-------|---------------------|
| **WS10M** | Wind Speed at 10 Meters | m/s | 💨 Vitesse vent (irrigation spray) |
| **WS10M_MAX** | Wind Speed at 10 Meters Maximum | m/s | 🌪️ Rafales maximum |
| **WS10M_MIN** | Wind Speed at 10 Meters Minimum | m/s | 🍃 Vent minimum |
| **WS10M_RANGE** | Wind Speed at 10 Meters Range | m/s | 📊 Variation vent |
| **WS50M** | Wind Speed at 50 Meters | m/s | 💨 Vent altitude 50m |
| **WS50M_MAX** | Wind Speed at 50 Meters Maximum | m/s | 🌪️ Rafales max 50m |
| **WS50M_MIN** | Wind Speed at 50 Meters Minimum | m/s | 🍃 Vent min 50m |
| **WS50M_RANGE** | Wind Speed at 50 Meters Range | m/s | 📊 Variation 50m |

---

### ☀️ RADIATION SOLAIRE (10 paramètres)

| Code | Nom complet | Unité | Utilisation possible |
|------|-------------|-------|---------------------|
| **ALLSKY_SFC_SW_DWN** | All Sky Surface Shortwave Downward Irradiance | MJ/m²/day | ☀️ Radiation solaire totale |
| **CLRSKY_SFC_SW_DWN** | Clear Sky Surface Shortwave Downward Irradiance | MJ/m²/day | ☀️ Radiation ciel clair |
| **ALLSKY_SFC_LW_DWN** | All Sky Surface Longwave Downward Irradiance | MJ/m²/day | 🌙 Radiation infrarouge |
| **ALLSKY_SFC_PAR_TOT** | All Sky Surface PAR Total | MJ/m²/day | 🌱 **PAR** - Photosynthèse active |
| **CLRSKY_SFC_PAR_TOT** | Clear Sky Surface PAR Total | MJ/m²/day | 🌱 PAR ciel clair |
| **ALLSKY_SRF_ALB** | All Sky Surface Albedo | - | 🔆 Réflectance surface |
| **TOA_SW_DWN** | Top-of-Atmosphere Shortwave Downward Irradiance | MJ/m²/day | 🛰️ Radiation haut atmosphère |
| **ALLSKY_KT** | All Sky Insolation Clearness Index | - | ☁️ Indice clarté |
| **CLRSKY_KT** | Clear Sky Insolation Clearness Index | - | ☀️ Clarté ciel clair |
| **ALLSKY_NKT** | Normalized Insolation Clearness Index | - | 📊 Indice normalisé |

---

### 🌍 PRESSION & AUTRES (3 paramètres)

| Code | Nom complet | Unité | Utilisation possible |
|------|-------------|-------|---------------------|
| **PS** | Surface Pressure | kPa | 🌍 Pression atmosphérique |
| **GWETTOP** | Surface Soil Wetness | % | 💧 **Humidité sol surface** |
| **GWETROOT** | Root Zone Soil Wetness | % | 🌱 **Humidité zone racinaire** |

---

## ⚡ AUTRES COMMUNAUTÉS

### 🔋 RENEWABLE ENERGY (RE)
Plus de **50 paramètres** pour énergie solaire et éolienne :
- Radiation directe/diffuse/réfléchie
- Vent à différentes altitudes
- Température pour performance panneaux
- Indice UV

### 🏢 SUSTAINABLE BUILDINGS (SB)
Paramètres pour bâtiments durables :
- Chauffage/refroidissement
- Température confort
- Humidité intérieure

---

## 🎯 PARAMÈTRES UTILES POUR TERRAGROW

### ✅ ACTUELLEMENT UTILISÉS (3)
```python
"T2M,PRECTOTCORR,RH2M"
```

### 🔥 TRÈS UTILES À AJOUTER (6)

| Paramètre | Pourquoi l'ajouter | Impact gameplay |
|-----------|-------------------|-----------------|
| **T2M_MAX** | Détection canicules | 🌡️ Événement "Canicule 42°C" |
| **T2M_MIN** | Détection gels | ❄️ Événement "Gel -2°C" |
| **ALLSKY_SFC_PAR_TOT** | Photosynthèse cultures | 🌱 Croissance NDVI plus réaliste |
| **WS10M** | Évaporation augmentée par vent | 💨 Ajuster ET selon vent |
| **GWETTOP** | Humidité sol NASA réelle | 💧 Remplacer simulation (si dispo) |
| **GWETROOT** | Humidité zone racinaire | 🌱 Stress hydrique précis |

### 🟡 UTILES MAIS SECONDAIRES (4)

| Paramètre | Utilisation | Priorité |
|-----------|-------------|----------|
| **T2MDEW** | Maladies fongiques (rosée) | Niveau 2 |
| **ALLSKY_SFC_SW_DWN** | Énergie solaire totale | Niveau 2 |
| **PS** | Altitude/pression | Niveau 2 |
| **WS10M_MAX** | Dommages cultures (rafales) | Niveau 2 |

---

## 💡 RECOMMANDATION POUR LE HACKATHON

### Option 1 : MINIMAL (actuel) ✅
```python
params = "T2M,PRECTOTCORR,RH2M"
```
**Avantage** : Simple, fonctionne, suffisant pour MVP

### Option 2 : AMÉLIORÉ 🔥 (recommandé)
```python
params = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_PAR_TOT,WS10M"
```
**Avantages** :
- Détection canicules/gels automatique
- Photosynthèse réaliste (PAR)
- Vent influence ET
- **Temps ajout** : 2-3h

### Option 3 : COMPLET 🚀
```python
params = "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,ALLSKY_SFC_PAR_TOT,WS10M,GWETTOP,GWETROOT"
```
**Avantages** :
- Humidité sol NASA réelle
- Toutes données pertinentes
- **Risque** : Complexité, temps (6-8h)

---

## 🔍 COMMENT TESTER UN NOUVEAU PARAMÈTRE

### Exemple : Ajouter T2M_MAX (température max)

**1. Modifier la requête API**
```python
params = {
    "parameters": "T2M,T2M_MAX,PRECTOTCORR,RH2M",  # Ajout T2M_MAX
    ...
}
```

**2. Extraire les données**
```python
temps_max = data['properties']['parameter']['T2M_MAX']
# {"20240101": 32.5, "20240102": 34.2, ...}
```

**3. Utiliser dans simulation**
```python
# Détecter canicule
if temp_max > 40:
    event = {
        'type': 'heatwave',
        'description': f'Canicule extrême {temp_max}°C !',
        'effect': 'ET × 1.5, stress thermique'
    }
```

**4. Test URL directe**
```
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,T2M_MAX&community=AG&longitude=11.52&latitude=3.87&start=20240101&end=20240107&format=JSON
```

---

## 📚 DOCUMENTATION COMPLÈTE

**Liste paramètres officielle** :
https://power.larc.nasa.gov/docs/services/api/application/parameters/

**Méthodologie (sources satellites)** :
https://power.larc.nasa.gov/docs/methodology/

**Exemples requêtes** :
https://power.larc.nasa.gov/docs/services/api/temporal/daily/

---

## ✅ CONCLUSION

### Ce qu'on utilise actuellement :
- **3 paramètres** : T2M, PRECTOTCORR, RH2M
- **Suffisant** pour MVP fonctionnel

### Ce qu'on pourrait ajouter facilement :
- **+4 paramètres** : T2M_MAX, T2M_MIN, ALLSKY_SFC_PAR_TOT, WS10M
- **Temps** : 2-3h
- **Impact** : Gameplay plus riche (canicules, gels, PAR)

### Ce qui existe mais complexe :
- **GWETTOP/GWETROOT** : Humidité sol NASA (si disponible pour la région)
- **50+ autres paramètres** : Pour versions futures

**Votre jeu utilise déjà les données essentielles. Tout le reste est bonus !** 🎉
