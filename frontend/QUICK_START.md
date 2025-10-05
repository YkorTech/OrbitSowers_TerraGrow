# 🚀 TerraGrow 3D - Guide de démarrage rapide

## ⚡ 3 Étapes pour lancer

### 1️⃣ Installer les dépendances (première fois uniquement)

```bash
npm install
```

**Temps estimé :** 2-3 minutes

---

### 2️⃣ Copier les assets (déjà fait ✅)

Les assets ont déjà été copiés automatiquement depuis `../glb/` :
- ✅ Textures Earth (daymap, nightmap, clouds)
- ✅ Modèle satellite .glb

**Si vous devez les recopier :**
```bash
./copy-assets.bat
```

---

### 3️⃣ Démarrer le projet

```bash
npm run dev
```

L'application s'ouvrira automatiquement sur `http://localhost:3000`

---

## 🔧 Prérequis IMPORTANT

### Backend Flask doit être démarré

Dans un **terminal séparé** :

```bash
cd ../OrbitSowers_TerraGrow/backend
python app.py
```

Le backend doit tourner sur `http://localhost:5000`

---

## 🎮 Utilisation

### Vue Globe (page d'accueil)
1. **Cliquez** sur n'importe quel point du globe
2. Une carte s'affiche avec les données NASA de la région
3. Cliquez **"Commencer à cultiver"**

### Vue Jeu
1. **Panneau gauche** : Voir les données satellites (NDVI, humidité, température)
2. **Centre** : Votre champ 3D avec 12 plants
3. **Panneau droit** : Ajuster irrigation et fertilisation
4. Cliquez **"Valider la semaine"**
5. Répéter 12 fois (12 semaines)

---

## 🐛 En cas de problème

### Le globe ne s'affiche pas
- Vérifiez la console du navigateur (F12)
- Vérifiez que les textures sont bien copiées :
  ```bash
  ls public/textures
  ```

### Erreur "API request failed"
- Vérifiez que le backend Flask tourne sur http://localhost:5000
- Testez : `curl http://localhost:5000/api/health`

### Erreur "Cannot find module"
```bash
rm -rf node_modules package-lock.json
npm install
```

---

## 📚 Ressources

- **README complet** : Voir `README.md`
- **Architecture** : Diagramme dans README
- **API Backend** : `../OrbitSowers_TerraGrow/backend/app.py`

---

## ✨ Features principales

- 🌍 Globe 3D cliquable (raycasting)
- 🛰️ Satellite en orbite réaliste
- 📡 Données NASA POWER en temps réel
- 🌾 Scène 3D champ agricole
- 📊 Interface moderne avec animations

---

**Prêt ? Lancez `npm run dev` !** 🚀
