# 🌍 TerraGrow Academy

## Jeu éducatif d'agriculture de précision avec données satellites NASA

![TerraGrow](https://img.shields.io/badge/NASA-Space%20Apps%20Challenge-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow)

---

## 📖 Description

**TerraGrow Academy** est un jeu éducatif qui enseigne l'agriculture de précision en utilisant de vraies données satellites de la NASA. Les joueurs cultivent des champs virtuels partout dans le monde en prenant des décisions d'irrigation et de fertilisation basées sur des données réelles.

### 🎯 Objectifs
- Apprendre l'agriculture de précision de manière ludique
- Comprendre l'utilisation des données satellites (NDVI, humidité du sol, météo)
- Optimiser le rendement tout en préservant les ressources (eau, azote)
- Découvrir les défis agricoles de différentes régions du monde

---

## 🌟 Fonctionnalités

✅ **Portée mondiale** : Jouez n'importe où dans le monde
✅ **Données NASA en temps réel** : Météo via NASA POWER API
✅ **15 régions pré-calculées** : Données haute qualité pour régions populaires
✅ **Simulation réaliste** : Bilan hydrique, croissance NDVI, stress cultures
✅ **Événements climatiques** : Sécheresses, canicules, gels selon région
✅ **Score durabilité** : Évaluation efficacité eau et azote
✅ **Visualisations** : Graphiques évolution NDVI sur 12 semaines

---

## 🛠️ Technologies utilisées

### Backend
- **Python 3.8+**
- **Flask** : API REST
- **Requests** : Appels APIs externes
- **NumPy** : Calculs scientifiques

### Frontend
- **HTML5 / CSS3**
- **JavaScript (Vanilla ES6+)**
- **Chart.js** : Visualisations graphiques

### APIs externes
- **NASA POWER** : Données météorologiques mondiales
- **Nominatim (OpenStreetMap)** : Géocodage et recherche de lieux

---

## 📦 Installation

### Prérequis
- Python 3.8 ou supérieur
- pip (gestionnaire de packages Python)
- Navigateur web moderne

### Étapes d'installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/OrbitSowers/TerraGrow.git
cd TerraGrow
```

2. **Installer les dépendances Python**
```bash
cd backend
pip install -r requirements.txt
```

3. **Lancer le serveur backend**
```bash
python app.py
```

Le serveur démarre sur `http://localhost:5000`

4. **Ouvrir le frontend**
```bash
cd ../frontend
# Ouvrir index.html dans votre navigateur
# OU utiliser un serveur local :
python -m http.server 8000
```

Puis ouvrir `http://localhost:8000` dans votre navigateur.

---

## 🎮 Comment jouer

### 1. Sélection de région
- Utilisez la géolocalisation automatique
- Recherchez une ville (ex: "Yaoundé", "Montréal")
- Choisissez parmi 15 régions pré-calculées

### 2. Gestion hebdomadaire
Chaque semaine, vous décidez :
- **💧 Irrigation** : 0-30 mm (coût : $3.5/mm)
- **🌿 Fertilisation** : 0-100 kg N/ha (coût : $1.2/kg)

### 3. Suivi de la culture
Surveillez :
- **NDVI** : Indice de végétation (0.15 → 0.85)
- **Humidité du sol** : % d'eau disponible
- **Météo** : Température, pluie prévue
- **Azote disponible** : Nutriments dans le sol

### 4. Événements climatiques
Affrontez des défis réels selon votre région :
- 🌵 **Sécheresse** (Sahel, zones arides)
- ☔ **Pluies torrentielles** (Tropiques)
- ❄️ **Gel tardif** (Régions tempérées)
- 🌡️ **Canicule** (Toutes régions)

### 5. Récolte et score
Après 12 semaines, obtenez :
- **Rendement** (t/ha) comparé à la moyenne régionale
- **Score durabilité** (efficacité eau et azote)
- **Étoiles** (1-5) selon performance globale
- **Conseils personnalisés** pour s'améliorer

---

## 📊 Régions pré-calculées

| Région | Pays | Climat | Cultures |
|--------|------|--------|----------|
| Yaoundé | 🇨🇲 Cameroun | Tropical savane | Maïs, Sorgho |
| Maroua | 🇨🇲 Cameroun | Sahel semi-aride | Sorgho |
| Douala | 🇨🇲 Cameroun | Tropical humide | Maïs |
| Montréal | 🇨🇦 Canada | Continental humide | Blé, Maïs |
| Nairobi | 🇰🇪 Kenya | Subtropical montagnard | Maïs |
| Kano | 🇳🇬 Nigeria | Sahel | Sorgho |
| Addis-Abeba | 🇪🇹 Éthiopie | Subtropical montagnard | Blé |
| Punjab | 🇮🇳 Inde | Semi-aride chaud | Blé |
| São Paulo | 🇧🇷 Brésil | Subtropical humide | Maïs |
| Iowa | 🇺🇸 USA | Continental humide | Maïs |
| Beauce | 🇫🇷 France | Océanique tempéré | Blé |
| Dhaka | 🇧🇩 Bangladesh | Tropical mousson | Maïs |
| Pampas | 🇦🇷 Argentine | Subtropical humide | Blé, Maïs |
| Prairies | 🇨🇦 Canada | Continental semi-aride | Blé |
| Garoua | 🇨🇲 Cameroun | Sahel | Sorgho |

---

## 🔬 Sources de données

### NASA POWER API
- **Température** (T2M) : Température à 2m du sol
- **Précipitations** (PRECTOTCORR) : Pluie corrigée
- **Humidité relative** (RH2M) : Humidité à 2m
- Documentation : https://power.larc.nasa.gov/

### OpenStreetMap Nominatim
- Géocodage et recherche de lieux
- API : https://nominatim.openstreetmap.org/

---

## 🏗️ Architecture

```
TerraGrow/
├── backend/
│   ├── app.py                 # API Flask principale
│   ├── config.py              # Configuration
│   ├── requirements.txt       # Dépendances Python
│   ├── models/                # Modèles de simulation
│   │   ├── crop.py           # Modèle culture (NDVI, croissance)
│   │   ├── soil.py           # Modèle sol (humidité, azote)
│   │   ├── region.py         # Modèle région (climat, paramètres)
│   │   └── game_state.py     # Orchestration jeu
│   └── services/              # Services APIs
│       ├── nasa_power_api.py # Wrapper NASA POWER
│       ├── geocoding_service.py # Nominatim
│       └── data_provider.py  # Données hybrides
│
├── frontend/
│   ├── index.html            # Sélection localisation
│   ├── game.html             # Jeu principal
│   ├── results.html          # Résultats finaux
│   ├── css/
│   │   └── styles.css        # Styles
│   └── js/
│       ├── api-client.js     # Client API
│       ├── location-selection.js
│       ├── game.js           # Logique jeu
│       └── results.js        # Affichage résultats
│
├── data/
│   └── regions/              # Données régions pré-calculées (JSON)
│
└── README.md
```

---

## 🤝 Équipe OrbitSowers Labs

**De Yaoundé 🇨🇲 à Montréal 🇨🇦**

Nous sommes une équipe passionnée par l'agriculture de précision et la démocratisation des technologies spatiales. Notre mission : rendre les données satellites NASA accessibles aux agriculteurs du monde entier.

### Vision
> "Cultiver l'avenir avec les yeux de la NASA"

---

## 📜 Licence

MIT License - Voir le fichier LICENSE pour plus de détails

---

## 🙏 Crédits

- **NASA POWER Project** : Données météorologiques
- **OpenStreetMap Nominatim** : Géocodage
- **Chart.js** : Bibliothèque de graphiques
- **NASA Space Apps Challenge** : Inspiration et plateforme

---

## 📧 Contact

Pour toute question ou contribution :
- GitHub Issues : https://github.com/OrbitSowers/TerraGrow/issues
- Email : contact@orbitsowers.com

---

**🌾 TerraGrow Academy - Apprendre l'agriculture de précision, une semaine à la fois**

*NASA Space Apps Challenge 2025 - Montréal* 
