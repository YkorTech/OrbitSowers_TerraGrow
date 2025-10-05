# 🌾 Système de Sélection de Culture

## 📋 Vue d'ensemble

Le nouveau système permet à l'utilisateur de **choisir la culture** qu'il souhaite cultiver, avec un **aperçu 3D en temps réel** du modèle.

---

## ✨ Fonctionnalités

### 1. **6 Cultures Disponibles**

| Culture | Modèle 3D | Climats recommandés |
|---------|-----------|---------------------|
| 🌾 **Blé** | wheat.glb (11 MB) | Continental, Tempéré |
| 🌽 **Maïs** | corn.glb (279 KB) | Tropical, Subtropical, Tempéré |
| 🍚 **Riz** | rice_plant.glb (152 KB) | Tropical, Subtropical |
| 🌻 **Tournesol** | sunflower.glb (4.5 MB) | Tempéré, Continental, Subtropical |
| 🍅 **Tomate** | tomato.glb (2.4 MB) | Subtropical, Tempéré, Tropical |
| 🥬 **Laitue** | lettuce.glb (84 KB) | Tempéré, Continental |

### 2. **Sélecteur avec Preview 3D**

- **Canvas 3D intégré** dans la RegionCard
- **Rotation automatique** du modèle (OrbitControls)
- **Changement en temps réel** quand l'utilisateur clique sur une culture
- **Recommandations climatiques** : Les cultures adaptées au climat de la région sont mises en avant

### 3. **Intégration Complète**

- ✅ **Store Zustand** : `selectedCrop` dans le state global
- ✅ **FieldScene** : Utilise `selectedCrop` au lieu de `crop.type` du backend
- ✅ **API Backend** : Passe le `cropId` choisi à l'initialisation
- ✅ **Configuration centralisée** : `src/config/crops.js`

---

## 🏗️ Architecture

### **Fichiers créés/modifiés**

```
src/
├── config/
│   └── crops.js                 ✅ NOUVEAU - Configuration des 6 cultures
│
├── components/
│   ├── UI/
│   │   ├── CropSelector.jsx     ✅ NOUVEAU - Composant sélecteur
│   │   ├── CropSelector.css     ✅ NOUVEAU - Styles
│   │   ├── RegionCard.jsx       🔧 MODIFIÉ - Intègre CropSelector
│   │   └── RegionCard.css       🔧 MODIFIÉ - Ajout scrollbar
│   │
│   └── Field/
│       └── FieldScene.jsx       🔧 MODIFIÉ - Utilise selectedCrop
│
├── stores/
│   └── gameStore.js             🔧 MODIFIÉ - Ajout selectedCrop
│
└── hooks/
    └── useNASAData.js           🔧 MODIFIÉ - Passe cropId au backend
```

---

## 📝 Configuration des Cultures (`crops.js`)

Chaque culture a :

```javascript
{
  id: 'wheat',              // Identifiant unique
  name: 'Blé',              // Nom français
  nameEn: 'Wheat',          // Nom anglais
  icon: '🌾',               // Emoji
  model: '/models/wheat.glb', // Chemin du modèle 3D
  scale: 1.0,               // Échelle du modèle
  yOffset: 0.5,             // Décalage vertical (pour aligner la base au sol)
  description: '...',       // Description
  climate: ['continental', 'temperate'], // Climats recommandés
  growthTime: '12 semaines',
  color: '#F4E4C1'          // Couleur (future utilisation)
}
```

---

## 🎮 Flux Utilisateur

### **Avant (Ancien système)**
1. Utilisateur clique sur une région
2. Backend choisit automatiquement la culture selon le climat
3. L'utilisateur voit la culture imposée

### **Maintenant (Nouveau système)**
1. Utilisateur clique sur une région
2. **Sélecteur de culture s'affiche** avec :
   - Preview 3D du modèle
   - Grille de 6 cultures cliquables
   - Recommandations selon le climat
3. Utilisateur **choisit sa culture** en cliquant
4. Le modèle 3D **tourne en temps réel**
5. Clic sur "Commencer à cultiver 🌾"
6. Le jeu démarre avec la **culture choisie**

---

## 🔧 Fonctions Utilitaires

### **`getCropById(cropId)`**
Récupère une culture par son ID.

```javascript
const wheat = getCropById('wheat')
```

### **`getRecommendedCrops(climate)`**
Filtre les cultures adaptées à un climat.

```javascript
const tropicalCrops = getRecommendedCrops('Tropical')
// Retourne : [corn, rice, tomato]
```

### **`getDefaultCrop(climate)`**
Retourne la première culture recommandée pour un climat.

```javascript
const defaultCrop = getDefaultCrop('Continental')
// Retourne : wheat
```

---

## 🎨 Styles & UX

### **Preview 3D**
- Fond gradient vert (#10b981)
- Rotation automatique à 2 deg/s
- Label avec icône + nom de la culture
- Canvas de 200px de hauteur

### **Grille de Sélection**
- 3 colonnes sur desktop, 2 sur mobile
- Effet hover : border verte + translation
- Sélection : fond gradient vert + glow
- Icônes 2rem, noms 0.85rem

### **Recommandations Climat**
- Badge vert clair en bas du sélecteur
- Affiche le climat de la région
- Visible seulement si des cultures sont recommandées

---

## 🔌 Intégration Backend

Le `cropId` choisi est passé au backend lors de l'initialisation :

```javascript
// Frontend
initializeGame(lat, lon, 'wheat')

// Backend Flask (doit gérer)
@app.route('/api/init', methods=['POST'])
def init():
    data = request.json
    crop_type = data.get('crop_type', 'maize')  # 'wheat', 'corn', 'rice', etc.
    # ...
```

**Note** : Le backend doit accepter le paramètre `crop_type` et l'utiliser au lieu de calculer automatiquement la culture selon le climat.

---

## 🚀 Améliorations Futures

- [ ] Ajouter plus de cultures (sorgho, riz basmati, soja, etc.)
- [ ] Statistiques par culture (rendement moyen, eau nécessaire, etc.)
- [ ] Animations de croissance différentes par culture
- [ ] Sons spécifiques par culture (vent dans le blé, etc.)
- [ ] Mode "défi" : culture non adaptée au climat = difficulté ++

---

## 🐛 Troubleshooting

### **Problème : Modèle 3D ne s'affiche pas**
- Vérifier que le fichier `.glb` existe dans `public/models/`
- Vérifier l'ID dans `crops.js` correspond au nom du fichier

### **Problème : Modèle traverse le sol**
- Ajuster le `yOffset` dans `crops.js`
- Valeurs typiques : 0 à 0.5

### **Problème : Modèle trop grand/petit**
- Ajuster le `scale` dans `crops.js`
- Valeurs typiques : 0.5 à 1.5

---

**🌾 TerraGrow Academy - Système de Sélection de Culture v1.0**
