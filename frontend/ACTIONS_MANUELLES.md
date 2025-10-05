# ✅ Actions Manuelles - TerraGrow 3D

## 📋 Checklist complète des étapes à faire MAINTENANT

---

## 1. ✅ Installation des dépendances Node.js

### Commande à exécuter :

```bash
cd "/c/Users/YkorT/OneDrive/YKOR/Space/NASA Space Apps Challenge/TerraGrow_3D"
npm install
```

**Temps estimé :** 2-3 minutes

**Dépendances installées :**
- React 18.3.1
- React Three Fiber 8.16.0
- @react-three/drei 9.105.0
- @react-spring/three 9.7.3
- Three.js 0.163.0
- Zustand 4.5.2
- Vite 5.2.8

**Vérification :**
```bash
ls node_modules
# Doit afficher un dossier rempli de packages
```

---

## 2. ✅ Assets déjà copiés automatiquement

Les assets ont été copiés avec succès par le script `copy-assets.bat` :

**Vérification :**
```bash
ls public/textures
# Doit afficher :
# - 2k_earth_daymap.jpg
# - 2k_earth_nightmap.jpg
# - 2k_earth_clouds.jpg
# - 2k_stars.jpg

ls public/models
# Doit afficher :
# - satellite.glb
```

✅ **Rien à faire ici, déjà copié !**

---

## 3. 🔧 Démarrer le Backend Flask (IMPORTANT)

### Terminal 1 : Backend Flask

```bash
cd "/c/Users/YkorT/OneDrive/YKOR/Space/NASA Space Apps Challenge/OrbitSowers_TerraGrow/backend"
python app.py
```

**Vérification :**
- Console doit afficher : `TerraGrow Academy API starting...`
- Ouvrir navigateur : `http://localhost:5000/api/health`
- Doit afficher : `{"status":"ok","message":"TerraGrow API is running"}`

⚠️ **GARDEZ CE TERMINAL OUVERT pendant toute la session**

---

## 4. 🚀 Lancer le Frontend 3D

### Terminal 2 : Frontend React

```bash
cd "/c/Users/YkorT/OneDrive/YKOR/Space/NASA Space Apps Challenge/TerraGrow_3D"
npm run dev
```

**Ce qui va se passer :**
1. Vite compile le projet (5-10 secondes)
2. Serveur démarre sur `http://localhost:3000`
3. Navigateur s'ouvre automatiquement
4. Globe 3D s'affiche avec satellite en orbite

**Vérification :**
- URL dans navigateur : `http://localhost:3000`
- Globe terrestre 3D visible
- Satellite en orbite autour de la Terre
- Console navigateur (F12) : Aucune erreur rouge

---

## 5. 🎮 Tester le jeu

### Scénario de test complet :

1. **Cliquer sur le globe** (n'importe où, ex: Cameroun)
2. Attendre 2-3 secondes (chargement données NASA)
3. **Carte région s'affiche** en bas avec :
   - Nom région (via Nominatim)
   - Température
   - Précipitations
   - Culture recommandée
4. Cliquer **"🌱 Commencer à cultiver"**
5. **Vue jeu 3D** s'affiche :
   - Panneau gauche : Données (NDVI, humidité, azote)
   - Centre : Champ 3D avec 12 plants
   - Panneau droit : Sliders irrigation/fertilisation
6. Ajuster sliders :
   - Irrigation : 20mm
   - Fertilisation : 50 kg N/ha
7. Cliquer **"✅ Valider la semaine"**
8. Vérifier :
   - NDVI augmente
   - Semaine passe à 2/12
   - Budget diminue
9. Répéter 11 fois (jusqu'à semaine 12)
10. **Récolte automatique** s'affiche

---

## 6. 🐛 Debugging si problèmes

### Problème : Écran noir (pas de globe)

**Console navigateur (F12) :**
```
Erreur possible : "Failed to load texture"
```

**Solution :**
```bash
ls public/textures
# Vérifier que les fichiers .jpg sont là

# Si manquants, recopier :
./copy-assets.bat
```

---

### Problème : "API request failed"

**Console navigateur (F12) :**
```
Error: Failed to fetch
```

**Solution :**
1. Vérifier backend Flask :
   ```bash
   curl http://localhost:5000/api/health
   ```
2. Si erreur → Redémarrer backend :
   ```bash
   cd ../OrbitSowers_TerraGrow/backend
   python app.py
   ```

---

### Problème : Globe cliquable mais rien ne se passe

**Vérifier console navigateur :**
```javascript
"Clicked: 3.87°, 11.52°"  // Doit s'afficher
```

**Si pas affiché :**
- Raycaster ne fonctionne pas
- Vérifier Three.js chargé : Onglet Network → three.js (200 OK)

---

### Problème : Satellite ne bouge pas

**Vérifier :**
1. Modèle chargé ?
   ```bash
   ls public/models/satellite.glb
   ```
2. Console erreur :
   ```
   "GLTFLoader: Unable to load"
   ```

**Solution :**
- Satellite.glb trop gros/corrompu ?
- Essayer sans satellite (commenter `<Satellite />` dans `Scene.jsx`)

---

## 7. 📊 Performance monitoring

### FPS attendu :
- **Desktop** : 60 FPS
- **Laptop** : 45-60 FPS
- **Mobile** : 30 FPS (non optimisé pour l'instant)

### Vérifier FPS :
1. Console navigateur (F12)
2. Onglet "Performance"
3. Enregistrer 5 secondes
4. Analyser "Frames per second"

**Si FPS < 30 :**
- Réduire résolution globe : `sphereGeometry args={[1, 32, 32]}`
- Désactiver satellite temporairement

---

## 8. ✨ Fonctionnalités implémentées

### Scène 3D ✅
- [x] Globe terrestre texturé (jour + nuit + nuages)
- [x] Satellite en orbite animée
- [x] Raycasting détection clics
- [x] Conversion lat/lon ↔ position 3D
- [x] Markers 15 régions populaires
- [x] Caméra animations (zoom smooth)
- [x] OrbitControls rotation souris
- [x] Mini-scène champ 3D (12 plants)
- [x] Lighting réaliste (directional + ambient + hemisphere)
- [x] Background étoilé

### UI Overlay ✅
- [x] Header avec logo + stats
- [x] Carte région (données NASA)
- [x] Interface jeu (panneaux gauche/droite)
- [x] Sliders irrigation/fertilisation
- [x] Barre NDVI colorée
- [x] Loading screen animé
- [x] Responsive design (desktop)

### Intégration API ✅
- [x] Hook useNASAData (fetch données)
- [x] Hook useGameActions (submit action)
- [x] Zustand state global
- [x] Wrapper apiClient Flask
- [x] Géocodage Nominatim

### Navigation ✅
- [x] 3 vues : globe → game → results
- [x] Transitions animées caméra
- [x] Bouton "Retour au globe"
- [x] État persisté (Zustand)

---

## 9. 🔄 Workflow développement

### Modifier le code :

**Exemple : Changer couleur globe**
1. Ouvrir `src/components/Scene/EarthGlobe.jsx`
2. Ligne 50 :
   ```javascript
   emissive={new THREE.Color(0xff0000)}  // Rouge au lieu de bleu
   ```
3. Sauvegarder (Ctrl+S)
4. **Vite recharge automatiquement** (Hot Module Replacement)
5. Globe change de couleur dans navigateur

**Exemple : Ajouter un message**
1. Ouvrir `src/components/UI/RegionCard.jsx`
2. Ajouter :
   ```jsx
   <p>Bienvenue en {region.name} !</p>
   ```
3. Sauvegarder
4. Message apparaît immédiatement

---

## 10. 📦 Build production (optionnel)

### Si vous voulez tester le build final :

```bash
npm run build
```

**Sortie :** `dist/` (dossier optimisé)

**Preview du build :**
```bash
npm run preview
```

**Déploiement :**
- Vercel : `vercel deploy`
- Netlify : Drag & drop `dist/`
- GitHub Pages : `gh-pages -d dist`

⚠️ **Backend Flask doit être déployé séparément** (pas static)

---

## ✅ Checklist finale

Avant de considérer le projet terminé :

- [ ] `npm install` terminé sans erreur
- [ ] Backend Flask tourne sur `http://localhost:5000`
- [ ] Frontend 3D accessible sur `http://localhost:3000`
- [ ] Globe s'affiche correctement (textures visibles)
- [ ] Satellite orbite autour de la Terre
- [ ] Clic sur globe détecte lat/lon (console log)
- [ ] Carte région s'affiche avec données NASA
- [ ] Bouton "Commencer à cultiver" fonctionne
- [ ] Vue jeu affiche champ 3D + panneaux
- [ ] Sliders ajustent irrigation/fertilisation
- [ ] Bouton "Valider semaine" fonctionne
- [ ] NDVI augmente/diminue selon décisions
- [ ] Budget se déduit correctement
- [ ] 12 semaines jouables sans crash
- [ ] Récolte finale s'affiche (ou view results)
- [ ] Bouton "Retour au globe" fonctionne
- [ ] Console navigateur : 0 erreur rouge

---

## 🎉 Résultat attendu

Après avoir suivi toutes les étapes, vous devriez avoir :

**Une expérience 3D immersive complète** :
- Globe terrestre interactif
- Satellite NASA en orbite
- Données satellites réelles (NASA POWER)
- Gameplay agriculture 12 semaines
- Interface moderne et fluide
- Intégration backend/frontend fonctionnelle

**Temps total estimé :**
- Installation : 3 minutes
- Premier lancement : 2 minutes
- Test complet : 10 minutes
- **Total : ~15 minutes** 🚀

---

**Bonne chance ! 🌍🛰️🌾**

*TerraGrow Academy - OrbitSowers Labs*
*NASA Space Apps Challenge 2025 - Montréal*
