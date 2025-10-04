# 🧪 Guide de Test - TerraGrow Academy

## 📋 Checklist de test

### ✅ Étape 1 : Lancer le backend

1. Ouvrir un terminal
2. Naviguer vers le dossier backend
3. Lancer :
```bash
cd backend
python app.py
```

**Vérifications** :
- ✅ Message "TerraGrow Academy API starting..."
- ✅ "Popular regions loaded: 15"
- ✅ "Running on http://127.0.0.1:5000"

---

### ✅ Étape 2 : Lancer le frontend

1. Ouvrir un NOUVEAU terminal
2. Naviguer vers le dossier frontend
3. Lancer :
```bash
cd frontend
python -m http.server 8000
```

**Vérifications** :
- ✅ "Serving HTTP on :: port 8000"

---

### ✅ Étape 3 : Ouvrir dans le navigateur

Ouvrir : **http://localhost:8000**

---

## 🎮 Scénarios de test

### Test 1 : Sélection région (index.html)

#### Actions :
1. La page se charge
2. Voir les 15 régions populaires affichées en grille
3. Cliquer sur "Yaoundé, Cameroun"
4. La région apparaît sélectionnée
5. Cliquer "Commencer à cultiver"

#### Résultats attendus :
- ✅ Grille de 15 régions visible
- ✅ Clic fonctionne (région surlignée)
- ✅ Redirection vers game.html

#### Bugs possibles :
- ❌ Régions ne s'affichent pas → Vérifier backend tourne
- ❌ Clic ne fonctionne pas → Ouvrir console (F12) voir erreurs

---

### Test 2 : Initialisation jeu (game.html)

#### Vérifications automatiques :
Dès l'arrivée sur game.html :

- ✅ Header affiche "Yaoundé, Cameroun"
- ✅ Semaine : 1 / 12
- ✅ Budget : $2000
- ✅ NDVI : 0.15 (barre verte à ~18%)
- ✅ Humidité sol : ~50%
- ✅ Azote : ~80 kg/ha
- ✅ Graphique NDVI affiché (1 point)
- ✅ Culture : "Maïs" affichée

#### Bugs connus corrigés :
- ✅ Graphique s'étend à l'infini → **CORRIGÉ** (hauteur fixe 300px)
- ✅ Écran blanc flash → **CORRIGÉ** (gestion erreurs ajoutée)

---

### Test 3 : Jouer semaine 1

#### Actions :
1. Slider irrigation : Mettre à 15mm
2. Slider fertilisation : Mettre à 50kg
3. Vérifier coûts :
   - Irrigation : 15 × 3.5 = $52.50
   - Fertilisation : 50 × 1.2 = $60.00
   - Total : $112.50
4. Cliquer "Valider la semaine"

#### Résultats attendus :
- ✅ Loading "Simulation en cours..." (1 sec)
- ✅ Semaine passe à 2
- ✅ Budget : 2000 - 112.5 = $1887.50
- ✅ NDVI augmente (ex: 0.15 → 0.23)
- ✅ Barre NDVI se remplit
- ✅ Graphique ajoute un point
- ✅ Message feedback : "Culture saine" (vert)

#### Bugs possibles :
- ❌ Rien ne se passe → Console (F12), vérifier erreur API
- ❌ NDVI ne bouge pas → Backend calcul problème
- ❌ Graphique plante → Vérifier Chart.js chargé

---

### Test 4 : Jouer 12 semaines complètes

#### Actions :
Répéter 12 fois :
1. Ajuster irrigation selon humidité
2. Ajuster fertilisation
3. Valider semaine

#### Scénarios à tester :

**Scénario A : Bon joueur** (irrigation équilibrée)
- Irrigation : 10-20mm selon pluie
- Fertilisation : 40-60kg
- **Résultat attendu** : NDVI → 0.70+, rendement >6 t/ha, ⭐⭐⭐⭐

**Scénario B : Sur-irrigation**
- Irrigation : 30mm chaque semaine
- Fertilisation : 100kg
- **Résultat attendu** : Lessivage azote, budget épuisé, durabilité faible

**Scénario C : Sous-irrigation**
- Irrigation : 0mm toujours
- Fertilisation : 0kg
- **Résultat attendu** : NDVI chute, stress hydrique, rendement <3 t/ha

---

### Test 5 : Événements aléatoires

#### Probabilité :
15% par semaine → 1-2 événements sur 12 semaines

#### Types possibles (Yaoundé - Tropical) :
- ☔ "Pluies torrentielles ! Drainage limité"
- 🌡️ "Canicule {temp}°C ! Stress extrême"
- 🌵 "Sécheresse ! Pas de pluie prévue"

#### Vérification :
- ✅ Message event apparaît (fond violet)
- ✅ Icône emoji visible
- ✅ Description claire

---

### Test 6 : Récolte (results.html)

#### Après semaine 12 :
1. Automatiquement redirigé vers results.html (2 sec)
2. Vérifier affichage :

**Scores** :
- ✅ Rendement : X.X t/ha
- ✅ Moyenne régionale : 5.2 t/ha (Yaoundé)
- ✅ Différence : +X% ou -X%
- ✅ Durabilité : X/100
- ✅ Étoiles : ⭐⭐⭐ (1-5)

**Graphique NDVI** :
- ✅ 12 points affichés
- ✅ Courbe colorée (vert/jaune/rouge)
- ✅ Hauteur fixe (pas à l'infini) → **CORRIGÉ**

**Conseils** :
- ✅ 2-3 recommandations personnalisées
- ✅ Conseil spécifique région (Yaoundé)

---

### Test 7 : Rejouer

#### Actions :
1. Cliquer "Rejouer cette région"
2. Ou "Changer de région"

#### Résultats :
- ✅ Retour à index.html
- ✅ Session nettoyée
- ✅ Peut recommencer

---

## 🐛 Bugs corrigés aujourd'hui

### Bug 1 : Graphique NDVI s'étend à l'infini ✅
**Cause** : Pas de hauteur fixe sur `.chart-container`
**Solution** : Ajout `height: 300px` et `canvas max-height: 250px`

### Bug 2 : Écran blanc flash ✅
**Cause** : Erreurs JavaScript non gérées
**Solution** : Ajout try/catch et vérifications `?.` (optional chaining)

### Bug 3 : Emojis cassent backend ✅
**Cause** : Encodage Windows (cp1252)
**Solution** : Suppression emojis dans print()

---

## 🔍 Console de débogage

### Ouvrir la console (F12)

**Messages normaux attendus** :
```
Loading game state...
Game state loaded: {region: {...}, crop: {...}, ...}
Irrigation: 15mm, Fertilizer: 50kg
Week validated, new state: {...}
```

**Erreurs à surveiller** :
```
❌ Failed to fetch → Backend pas lancé
❌ 404 Not Found → Route API incorrecte
❌ CORS error → Problème Flask CORS
❌ Undefined reading 'ndvi' → Données manquantes
```

---

## 📊 Données de test

### Vérifier données NASA chargées :

**Dans console backend** (après démarrage) :
```
Popular regions loaded: 15
```

**Vérifier fichiers JSON** :
```bash
ls data/regions/
# Doit afficher 15 fichiers .json
```

**Tester API directement** :
```bash
curl http://localhost:5000/api/health
# {"status":"ok","message":"TerraGrow API is running"}
```

---

## ✅ Checklist finale avant démo

Avant le hackathon, vérifier :

- [ ] Backend démarre sans erreur
- [ ] Frontend se charge (index.html)
- [ ] 15 régions affichées
- [ ] Peut jouer 12 semaines complètes
- [ ] Graphiques fonctionnent (pas d'infini)
- [ ] Pas d'écran blanc
- [ ] Récolte affiche scores
- [ ] Peut rejouer

**Si tout ✅ → JEU PRÊT POUR DÉMO !** 🎉
