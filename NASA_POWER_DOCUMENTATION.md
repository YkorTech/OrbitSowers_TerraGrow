# 📡 Documentation NASA POWER API

## Source officielle

**URL** : https://power.larc.nasa.gov/

**Documentation API** : https://power.larc.nasa.gov/docs/services/api/

---

## Qu'est-ce que NASA POWER ?

**POWER** = **P**rediction **O**f **W**orldwide **E**nergy **R**esources

- Projet de la NASA Langley Research Center
- Données météorologiques et solaires mondiales
- **Gratuit et public** (pas de clé API)
- Données depuis 1981 jusqu'à temps réel
- Résolution : 0.5° × 0.5° (environ 50km × 50km)

---

## Paramètres utilisés dans TerraGrow

### T2M - Temperature at 2 Meters
- **Description** : Température de l'air à 2 mètres du sol
- **Unité** : °C (Celsius)
- **Source** : MERRA-2 (Modern-Era Retrospective analysis for Research and Applications)
- **Utilisation** : Calculer stress thermique des cultures

### PRECTOTCORR - Precipitation Corrected
- **Description** : Précipitations totales corrigées
- **Unité** : mm/jour
- **Source** : IMERG (Integrated Multi-satellitE Retrievals for GPM)
- **Utilisation** : Bilan hydrique du sol

### RH2M - Relative Humidity at 2 Meters
- **Description** : Humidité relative à 2 mètres
- **Unité** : %
- **Source** : MERRA-2
- **Utilisation** : Calculer évapotranspiration (ET)

---

## Endpoint utilisé

```
GET https://power.larc.nasa.gov/api/temporal/daily/point
```

### Paramètres de requête

| Paramètre | Valeur | Description |
|-----------|--------|-------------|
| `parameters` | `T2M,PRECTOTCORR,RH2M` | Paramètres demandés (séparés par virgules) |
| `community` | `AG` | Communauté Agriculture |
| `latitude` | `3.87` | Latitude (exemple Yaoundé) |
| `longitude` | `11.52` | Longitude (exemple Yaoundé) |
| `start` | `20240101` | Date début (YYYYMMDD) |
| `end` | `20241231` | Date fin (YYYYMMDD) |
| `format` | `JSON` | Format de réponse |

---

## Exemple de requête complète

### URL
```
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M,PRECTOTCORR,RH2M&community=AG&longitude=11.52&latitude=3.87&start=20240101&end=20240107&format=JSON
```

### Réponse JSON (structure)
```json
{
  "type": "Feature",
  "geometry": {
    "type": "Point",
    "coordinates": [11.52, 3.87, 588.63]
  },
  "header": {
    "title": "NASA/POWER Source Native Resolution Daily Data",
    "api_version": "v2.5.8",
    "fillValue": -999.0
  },
  "parameters": {
    "T2M": {
      "units": "C",
      "longname": "Temperature at 2 Meters"
    },
    "PRECTOTCORR": {
      "units": "mm/day",
      "longname": "Precipitation Corrected"
    },
    "RH2M": {
      "units": "%",
      "longname": "Relative Humidity at 2 Meters"
    }
  },
  "properties": {
    "parameter": {
      "T2M": {
        "20240101": 26.56,
        "20240102": 27.12,
        "20240103": 26.89,
        ...
      },
      "PRECTOTCORR": {
        "20240101": 0.0,
        "20240102": 12.34,
        "20240103": 5.67,
        ...
      },
      "RH2M": {
        "20240101": 66.29,
        "20240102": 78.45,
        "20240103": 72.11,
        ...
      }
    }
  }
}
```

---

## Validation des données

### 1. Source de données satellites

**MERRA-2** (NASA Global Modeling and Assimilation Office)
- Réanalyse atmosphérique
- Assimile observations satellites + stations météo
- Résolution temporelle : horaire → agrégé en quotidien
- Résolution spatiale : 0.5° × 0.625°

**IMERG** (GPM - Global Precipitation Measurement)
- Mission conjointe NASA/JAXA
- Constellation de satellites de précipitation
- Données depuis 2000
- Mises à jour quotidiennes

### 2. Couverture géographique

- **Globale** : -90° à +90° latitude, -180° à +180° longitude
- **Toute la Terre** : Océans + continents
- **Toutes altitudes** : Du niveau de mer à haute montagne

### 3. Période disponible

- **Historique** : 1981 - présent
- **Temps réel** : Mis à jour quotidiennement (délai ~2-3 jours)
- **Prévisions** : Non disponible (données historiques uniquement)

---

## Limites et considérations

### Résolution spatiale
- **0.5° × 0.5°** ≈ 50km × 50km à l'équateur
- Interpolation pour coordonnées précises
- Microclimat local non capturé

### Résolution temporelle
- Données **quotidiennes** (pas horaires)
- Moyenne/total journalier

### Délai
- Données temps réel avec **2-3 jours de retard**
- Données historiques finalisées après 6 mois

### Précision
- Température : ±2°C
- Précipitation : ±20% (varie selon région)
- Humidité : ±5%

---

## Utilisation dans TerraGrow

### Workflow
```
1. Utilisateur choisit région (lat, lon)
2. Backend appelle NASA POWER API
3. Récupère 90 jours de données (T2M, PRECTOTCORR, RH2M)
4. Agrège en 12 semaines
5. Calcule ET (évapotranspiration)
6. Stocke dans fichier JSON
7. Utilise pour simulation jeu
```

### Calculs dérivés

**Évapotranspiration (ET)**
```python
ET = 0.0023 × (T + 17.8) × (100 - RH) / 10
```
- Formule simplifiée de Hargreaves
- T = température (°C)
- RH = humidité relative (%)

---

## Crédits et citations

### Citation officielle NASA POWER
```
NASA POWER Project Data Sets (2024). NASA Langley Research Center (LaRC)
Prediction of Worldwide Energy Resources (POWER) Project.
https://power.larc.nasa.gov/
```

### Licence
- **Domaine public** (NASA)
- Données libres d'utilisation
- Attribution recommandée mais non obligatoire

---

## Ressources supplémentaires

- **Site officiel** : https://power.larc.nasa.gov/
- **Documentation API** : https://power.larc.nasa.gov/docs/services/api/
- **Méthodologie** : https://power.larc.nasa.gov/docs/methodology/
- **FAQ** : https://power.larc.nasa.gov/docs/faq/
- **Contact** : nasa-power@mail.nasa.gov

---

## Vérification manuelle

Pour tester l'API vous-même :

1. Ouvrez votre navigateur
2. Collez cette URL :
```
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=T2M&community=AG&longitude=11.52&latitude=3.87&start=20240101&end=20240107&format=JSON
```
3. Vous verrez les données JSON brutes NASA

**Aucune clé API, aucune inscription, 100% gratuit et public !**
