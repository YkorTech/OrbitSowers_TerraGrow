# 🛰️ Guide AppEEARS - TerraGrow Academy

## 📋 Actions manuelles à faire MAINTENANT

---

## ✅ **ÉTAPE 1 : Vérifier autorisation SEDAC** (1 min)

Vous avez déjà fait ça normalement, mais vérifions :

1. Aller sur : https://urs.earthdata.nasa.gov/
2. Se connecter avec vos identifiants
3. Cliquer **"My Applications"**
4. Vérifier que **"SEDAC Website"** est autorisé (checkmark ✓)

**Si pas autorisé** → Cliquer "Authorize"

---

## 🧪 **ÉTAPE 2 : Tester AppEEARS API** (5-10 min)

### Lancer le script de test :

```bash
python test_appeears.py
```

### Vous allez voir :

```
====================================================
🧪 TEST AppEEARS API - TerraGrow
====================================================

📝 ÉTAPE 1/5 : Login NASA Earthdata
------------------------------------------------------------
Entrez votre username NASA Earthdata: [VOTRE_USERNAME]
Entrez votre password NASA Earthdata: [VOTRE_PASSWORD]

✅ AppEEARS login successful! Token expires: 2025-10-06T...
```

### Ce qui va se passer :

1. **Login** → Token généré (valide 48h)
2. **Recherche produits** → Liste des NDVI/SMAP disponibles
3. **Soumission tâche** → Extraction NDVI Yaoundé (12 mois)
4. **Attente** → Processing 1-5 minutes (affiche progression)
5. **Téléchargement** → Fichiers CSV dans `data/appeears/`

---

## 📊 **ÉTAPE 3 : Examiner les résultats** (2 min)

### Après le test, vérifiez :

**Fichiers créés** :
```
data/appeears/
├── terragrow_yaounde_cameroun-MOD13Q1-061-results.csv  ← DONNÉES NDVI
├── terragrow_yaounde_cameroun-request.json
└── terragrow_yaounde_cameroun-metadata.xml
```

### Ouvrir le CSV :

Le fichier contient les colonnes :
- `Date` - Date d'observation
- `MOD13Q1_061__250m_16_days_NDVI` - Valeur NDVI (× 10000)
- `MOD13Q1_061__250m_16_days_EVI` - Valeur EVI
- `Category`, `ID`, `Latitude`, `Longitude`

**Exemple** :
```csv
Date,MOD13Q1_061__250m_16_days_NDVI,MOD13Q1_061__250m_16_days_EVI,...
2024-01-01,6500,4200,...
2024-01-17,7200,4800,...
...
```

**Conversion NDVI** : Diviser par 10000
- 6500 → 0.65 (santé moyenne)
- 7200 → 0.72 (bonne santé)

---

## ⚠️ **Problèmes possibles**

### ❌ Login échoué
```
❌ AppEEARS login failed: 401 Unauthorized
```

**Solution** :
- Vérifier username/password NASA Earthdata
- Vérifier email confirmé
- Réinitialiser mot de passe si nécessaire

---

### ❌ Task failed
```
❌ Task failed: No data available for specified parameters
```

**Causes possibles** :
- Dates trop anciennes (MODIS depuis 2000)
- Coordonnées invalides (océan, pôles)
- Produit non disponible pour la région

**Solution** :
- Changer dates (utiliser 2023-2024)
- Vérifier coordonnées (terre ferme)

---

### ⏰ Timeout
```
⏰ Timeout waiting for task
```

**Solution** :
- Augmenter `max_wait_minutes=15` dans le script
- Vérifier status manuellement sur : https://appeears.earthdatacloud.nasa.gov/

---

## 🔍 **ÉTAPE 4 : Rechercher produits SMAP** (optionnel)

Si vous voulez tester SMAP (humidité sol) :

### Modifier `test_appeears.py` ligne 100 :

```python
layers = [
    {
        'product': 'MOD13Q1.061',  # MODIS NDVI
        'layer': '_250m_16_days_NDVI'
    },
    {
        'product': 'SPL4SMGP.007',  # SMAP Soil Moisture (si dispo)
        'layer': 'sm_surface'
    }
]
```

**Note** : SMAP peut ne PAS être disponible via AppEEARS Point.
Si erreur → Garder uniquement NDVI pour l'instant.

---

## 📝 **ÉTAPE 5 : Me dire les résultats** (1 min)

Une fois le test terminé, dites-moi :

### ✅ Si succès :
- "✅ AppEEARS fonctionne ! J'ai le CSV avec les données NDVI de Yaoundé"
- Coller les 5 premières lignes du CSV

### ❌ Si erreur :
- Coller le message d'erreur complet
- Je vous aiderai à débugger

---

## 🚀 **PROCHAINES ÉTAPES** (après test réussi)

1. **Script extraction 15 régions** → J'automatise pour toutes les régions
2. **Parser CSV** → Convertir en format JSON TerraGrow
3. **Intégrer au jeu** → Remplacer NDVI simulé par NDVI réel
4. **Tester gameplay** → Vérifier que tout fonctionne

---

## 📚 **Ressources AppEEARS**

- **Interface web** : https://appeears.earthdatacloud.nasa.gov/
- **Documentation** : https://appeears.earthdatacloud.nasa.gov/api/
- **Produits disponibles** : https://appeears.earthdatacloud.nasa.gov/products

---

## 🎯 **Résumé : Ce que vous devez faire**

1. ✅ Vérifier SEDAC autorisé (déjà fait normalement)
2. 🧪 Lancer `python test_appeears.py`
3. 📝 Entrer vos identifiants NASA Earthdata
4. ⏳ Attendre 2-5 minutes (processing + download)
5. 📊 Vérifier fichier CSV créé
6. 💬 Me dire si ça marche ou quelle erreur vous avez

---

**C'EST PARTI ! Lancez le test maintenant** 🚀
