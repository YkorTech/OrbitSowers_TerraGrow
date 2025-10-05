# 🌍 TerraGrow Academy - Interactive 3D WebGL Experience

> Jeu éducatif d'agriculture de précision avec données satellites NASA en 3D

**Par OrbitSowers Labs** 🇨🇲 → 🇨🇦
NASA Space Apps Challenge 2025 - Montréal

---

## ✨ Features

- 🌍 **Globe 3D interactif** - Cliquez sur les 15 régions pré-définies ou utilisez la géolocalisation
- 🛰️ **Satellite en orbite** - Animation réaliste avec modèle 3D
- 📡 **Données NASA en temps réel** - NASA POWER API (météo, température, précipitations)
- 🎮 **Gameplay immersif** - Simulation agricole 12 semaines avec irrigation/fertilisation
- 🌱 **6 cultures sélectionnables** - Blé, maïs, riz, tournesol, tomate, laitue avec preview 3D
- 🌾 **Scène 3D champ réaliste** - Modèles 3D GLB avec textures sol détaillées
- 📊 **Interface HUD moderne** - Stats en temps réel + contrôles intuitifs
- 🌤️ **Atmosphère immersive** - Ciel dynamique, brouillard, éclairage réaliste
- 🎯 **Écran de résultats détaillés** - Score, étoiles, rendement, durabilité

---

## 🚀 Installation & Démarrage

### Prérequis

- Node.js 18+ installé
- Backend Flask TerraGrow en cours d'exécution (`http://localhost:5000`)

### Étapes

```bash
# 1. Se placer dans le dossier
cd TerraGrow_3D

# 2. Installer les dépendances
npm install

# 3. IMPORTANT: Vérifier que les assets sont présents
# - public/textures/ doit contenir les textures Earth + sol
# - public/models/ doit contenir satellite.glb, wheat.glb, corn.glb

# 4. Démarrer le serveur de développement
npm run dev

# 5. Ouvrir http://localhost:3000 dans le navigateur
```

---

## 📦 Setup Assets (IMPORTANT)

### Assets requis dans `public/` :

**Textures Earth** (`public/textures/`) :
```
2k_earth_daymap.jpg      (463 KB) - Texture jour
2k_earth_nightmap.jpg    (255 KB) - Texture nuit
2k_earth_clouds.jpg      (965 KB) - Nuages
2k_stars.jpg             (223 KB) - Fond étoilé
```

**Textures Sol** (`public/textures/`) :
```
brown_mud_02_diff_1k.jpg       - Sol diffuse (Poly Haven)
brown_mud_02_nor_dx_1k.jpg     - Sol normal map
leafy_grass_diff_1k.jpg        - Herbe
```

**Modèles 3D** (`public/models/`) :
```
satellite.glb            (4.2 MB) - Satellite NASA
wheat.glb                        - Blé
corn.glb                         - Maïs
rice_plant.glb                   - Riz
sunflower.glb                    - Tournesol
tomato.glb                       - Tomate
lettuce.glb                      - Laitue
```

### Commande rapide (Windows PowerShell) :

```powershell
# Créer les dossiers
New-Item -ItemType Directory -Force -Path public/textures
New-Item -ItemType Directory -Force -Path public/models

# Copier textures
Copy-Item ../glb/2k_earth_daymap.jpg public/textures/
Copy-Item ../glb/2k_earth_nightmap.jpg public/textures/
Copy-Item ../glb/2k_earth_clouds.jpg public/textures/
Copy-Item ../glb/2k_stars.jpg public/textures/

# Copier modèle
Copy-Item ../glb/satellite.glb public/models/
```

### Commande rapide (Linux/Mac) :

```bash
mkdir -p public/{textures,models}

cp ../glb/2k_earth_daymap.jpg public/textures/
cp ../glb/2k_earth_nightmap.jpg public/textures/
cp ../glb/2k_earth_clouds.jpg public/textures/
cp ../glb/2k_stars.jpg public/textures/

cp ../glb/satellite.glb public/models/
```

---

## 🎮 Comment jouer

### 1. Vue Globe
- **15 régions cliquables** marquées par des sphères orange/vertes avec drapeaux
- **Bouton "📍 Ma position"** pour utiliser la géolocalisation
- Les régions tournent avec la Terre (rotation synchronisée)
- Hover sur une région → elle s'agrandit et devient verte

### 2. Sélection Région & Culture
- Affichage des données **NASA POWER** en temps réel :
  - Climat de la région (ex: Tropical, Continental, Subtropical)
  - Température moyenne
  - Précipitations prévues
- **Sélecteur de culture interactif** :
  - Aperçu 3D rotatif de la culture
  - 6 cultures disponibles : Blé, Maïs, Riz, Tournesol, Tomate, Laitue
  - Cultures recommandées ✨ selon le climat
  - Liberté de cultiver n'importe quelle culture
- Cliquez **"Commencer à cultiver 🌱"**

### 3. Vue Jeu (Champ 3D Réaliste)
- **Barre supérieure** : Stats en temps réel (Semaine, NDVI, Humidité, Azote, Budget)
- **Centre (plein écran)** : Scène 3D du champ
  - Sol texturé avec relief (brown mud + herbe)
  - 16 plants 3D (culture sélectionnée)
  - Croissance dynamique selon NDVI
  - Animation de vent (balancement des plants)
  - Ciel dynamique avec soleil
  - Brouillard et éclairage réaliste
- **Barre inférieure** : Contrôles de gestion
  - 💧 **Irrigation** : 0-50mm
  - 🌿 **Fertilisation** : 0-200 kg N/ha
  - Coût en temps réel
  - Bouton validation semaine

### 4. Dynamique visuelle selon NDVI
- **NDVI élevé** (>0.6) → Plants grands et verts (santé excellente)
- **NDVI moyen** (0.3-0.6) → Plants moyens et jaunâtres (stress modéré)
- **NDVI bas** (<0.3) → Plants petits et rougeâtres (stress sévère)
- **La culture ne change jamais** durant les 12 semaines

### 5. Fin de saison (12 semaines)
- **Écran de résultats détaillé** :
  - Étoiles (1-5 ⭐)
  - Rendement vs moyenne régionale (t/ha)
  - Score durabilité (0-100)
  - Efficacité eau & azote
  - Budget restant
  - Recommandations personnalisées par climat
  - Graphique évolution NDVI
- Bouton **"Nouvelle partie"** pour rejouer

---

## 🏗️ Architecture

### Structure du projet

```
TerraGrow_3D/
├── src/
│   ├── components/
│   │   ├── Scene/            # Composants 3D
│   │   │   ├── Scene.jsx
│   │   │   ├── EarthGlobe.jsx      ⭐ Globe avec rotation synchronisée
│   │   │   ├── Satellite.jsx       🛰️ Orbite satellite (GLB + lumière)
│   │   │   ├── CameraController.jsx 📷 Animations caméra (zoom 1.6)
│   │   │   ├── RegionMarkers.jsx   📍 15 régions cliquables + hover
│   │   │   └── Lights.jsx
│   │   │
│   │   ├── Field/            # Scène champ 3D réaliste
│   │   │   └── FieldScene.jsx      🌾 Sol texturé + 16 plants GLB
│   │   │                           🌤️ Ciel + fog + lumières
│   │   │
│   │   └── UI/               # Interface overlay
│   │       ├── Header.jsx
│   │       ├── RegionCard.jsx      📋 Fiche région
│   │       ├── CropSelector.jsx    🌱 Sélecteur cultures 3D
│   │       ├── GameInterface.jsx   🎮 HUD stats + contrôles
│   │       ├── ResultsScreen.jsx   🏆 Écran de résultats
│   │       ├── GlobeControls.jsx   📍 Bouton géolocalisation
│   │       └── LoadingScreen.jsx
│   │
│   ├── hooks/
│   │   └── useNASAData.js          📡 Hook API NASA
│   │
│   ├── utils/
│   │   ├── coordinates.js          🧮 Lat/lon ↔ 3D
│   │   └── apiClient.js            🌐 Wrapper Flask API
│   │
│   ├── stores/
│   │   └── gameStore.js            💾 Zustand state management
│   │
│   ├── styles/
│   │   └── global.css
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── public/
│   ├── models/
│   │   ├── satellite.glb           🛰️ Modèle 3D satellite
│   │   ├── wheat.glb               🌾 Blé
│   │   ├── corn.glb                🌽 Maïs
│   │   ├── rice_plant.glb          🍚 Riz
│   │   ├── sunflower.glb           🌻 Tournesol
│   │   ├── tomato.glb              🍅 Tomate
│   │   └── lettuce.glb             🥬 Laitue
│   │
│   └── textures/
│       ├── 2k_earth_daymap.jpg     🌍 Texture jour
│       ├── 2k_earth_nightmap.jpg   🌃 Texture nuit
│       ├── 2k_earth_clouds.jpg     ☁️ Nuages
│       ├── 2k_stars.jpg            ⭐ Fond étoilé
│       ├── brown_mud_02_diff_1k.jpg     🌱 Sol diffuse
│       ├── brown_mud_02_nor_dx_1k.jpg   🌱 Sol normal map
│       └── leafy_grass_diff_1k.jpg      🌿 Herbe
│
├── package.json
├── vite.config.js
└── README.md
```

### Stack technologique

- **React 18** - Framework UI
- **React Three Fiber (R3F)** - Abstraction React de Three.js
- **@react-three/drei** - Helpers R3F (OrbitControls, useGLTF, etc.)
- **@react-spring/three** - Animations caméra
- **Zustand** - State management global
- **Vite** - Build tool moderne
- **Chart.js** - Graphiques (si ajoutés)

---

## 🔌 Intégration Backend Flask

L'application se connecte au backend existant `OrbitSowers_TerraGrow/backend/` :

**API utilisées** :
- `POST /api/init` - Initialiser partie (lat/lon)
- `POST /api/action` - Valider semaine (irrigation/fertilisation)
- `GET /api/harvest` - Récolte finale
- `GET /api/search-location` - Recherche lieu (Nominatim proxy)
- `GET /api/popular-regions` - 15 régions pré-calculées

**Configuration** : `src/utils/apiClient.js`

```javascript
const API_BASE_URL = 'http://localhost:5000/api'
```

**Important** : Le backend Flask doit être **démarré** avant de lancer le frontend 3D.

```bash
# Terminal 1 : Backend
cd ../OrbitSowers_TerraGrow/backend
python app.py

# Terminal 2 : Frontend 3D
cd ../TerraGrow_3D
npm run dev
```

---

## 🎨 Customisation

### Modifier les couleurs du globe

`src/components/Scene/EarthGlobe.jsx` :
```javascript
<meshStandardMaterial
  map={dayMap}
  emissiveMap={nightMap}
  emissive={new THREE.Color(0x444444)}  // Couleur émissive (nuit)
  emissiveIntensity={0.2}               // Intensité
  roughness={0.7}                        // Rugosité
  metalness={0.1}                        // Metallic
/>
```

### Ajuster la vitesse du satellite

`src/components/Scene/Satellite.jsx` :
```javascript
const speed = 0.3  // Modifier cette valeur (plus bas = plus lent)
```

### Changer la distance de zoom caméra

`src/components/Scene/CameraController.jsx` :
```javascript
getCameraPositionForRegion(lat, lon, 1.8)  // Distance (1.8 = zoom proche)
```

---

## 🐛 Troubleshooting

### Erreur: "Cannot find module 'three'"

```bash
npm install
```

### Erreur: "Failed to load textures"

Vérifiez que les fichiers sont bien copiés dans `public/textures/` et `public/models/` :
```bash
ls public/textures/
ls public/models/
```

### Erreur: "API request failed"

- Vérifiez que le backend Flask tourne sur `http://localhost:5000`
- Testez manuellement : `curl http://localhost:5000/api/health`

### Erreur: "Cannot animate between AnimatedValue and AnimatedArray"

✅ **Corrigé** dans CameraController.jsx - conversion Vector3 → Array

### Globe ne s'affiche pas (écran noir)

1. Ouvrez la console navigateur (F12)
2. Cherchez erreurs Three.js
3. Vérifiez que WebGL est supporté : `https://get.webgl.org/`

### Cultures ne s'affichent pas complètement dans preview

✅ **Corrigé** - Caméra et échelle optimisées par culture

### Performance lente / WebGL Context Lost

- Rafraîchissez la page (F5)
- Réduire la résolution du globe si nécessaire
- Vérifiez GPU dans gestionnaire de tâches

---

## 📊 Performance

### Benchmarks

- **FPS cible** : 60 FPS (desktop), 30 FPS (mobile)
- **Polygones globe** : ~8k triangles
- **Textures** : 2k résolution (optimisé)
- **Draw calls** : ~10 par frame

### Optimisations futures

- [ ] LOD (Level of Detail) pour le globe
- [ ] Texture compression (basis format)
- [ ] Instanced rendering pour les markers
- [ ] Worker thread pour raycasting

---

## 🚀 Build Production

```bash
# Build optimisé
npm run build

# Preview du build
npm run preview

# Dossier de sortie : dist/
```

**Déploiement** :
- Vercel, Netlify, GitHub Pages compatibles
- Nécessite backend Flask séparé (pas static)

---

## 📝 TODO / Roadmap

### Phase 1 (MVP) - ✅ Complété
- [x] Globe 3D avec 15 régions cliquables
- [x] Rotation synchronisée (Terre + nuages + markers)
- [x] Satellite en orbite avec modèle GLB
- [x] Caméra animations (zoom fluide) - **Bug animation @react-spring corrigé**
- [x] Géolocalisation navigateur
- [x] Intégration API Flask complète
- [x] **6 cultures sélectionnables** avec preview 3D rotatif
- [x] Recommandations cultures selon climat
- [x] Scène champ 3D réaliste :
  - [x] Sol texturé (diffuse + normal map)
  - [x] 16 plants 3D (6 modèles GLB)
  - [x] Croissance dynamique selon NDVI
  - [x] Animation de vent
  - [x] Ciel dynamique + fog + lumières
- [x] HUD stats + contrôles irrigation/fertilisation
- [x] Écran de résultats détaillé avec graphique
- [x] **Affichage 3D cultures optimisé** (preview complet)

### Phase 2 (Améliorations) - En cours
- [ ] **Corriger NDVI history** (13 points → 12 points)
- [ ] **Résoudre WebGL Context Lost** (optimisation cleanup)
- [ ] **Indicateurs visuels** irrigation/fertilisation recommandée
- [ ] Graphique NDVI Chart.js (évolution 12 semaines)
- [ ] Particules irrigation (effet pluie 3D)
- [ ] Sons ambient (vent, pluie)
- [ ] Tutoriel interactif (tooltips)
- [ ] Mode mobile optimisé (touch controls)

### Phase 3 (Avancé) - Futur
- [ ] Optimisation performances (LOD, instancing)
- [ ] Plus de modèles cultures (patate, sorgho)
- [ ] Earth.glb modèle haute qualité
- [ ] Clouds shader animé (parallax)
- [ ] Postprocessing (bloom, SSAO)
- [ ] Mode multijoueur (comparaison scores)
- [ ] Leaderboard régional

---

## 🤝 Contribution

**Équipe OrbitSowers Labs**
- Camerounais 🇨🇲 basés à Montréal 🇨🇦
- NASA Space Apps Challenge 2025

---

## 📜 Licence

MIT License - Open Source

---

## 🙏 Crédits

- **Textures Earth** : [Solar System Scope](https://www.solarsystemscope.com/textures/)
- **Textures Sol** : [Poly Haven](https://polyhaven.com) - Brown Mud 02, Leafy Grass
- **Modèles 3D** : Sketchfab (satellite.glb, wheat.glb, corn.glb)
- **NASA POWER API** : NASA Langley Research Center
- **Nominatim API** : OpenStreetMap
- **Three.js** : Three.js contributors
- **React Three Fiber** : Poimandres team (@pmndrs/drei)

---

## 📧 Support

- **Issues** : GitHub Issues
- **Email** : contact@orbitsowers.com

---

**🌾 TerraGrow Academy - Cultiver l'avenir avec les yeux de la NASA**

*Hackathon NASA Space Apps Challenge 2025 - Montréal*
