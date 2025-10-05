# TerraGrow Academy - MVP v2.0
## Guide Pratique Hackathon 48h - Architecture Hybride
### NASA Space Apps Challenge 2025 - Montréal

---

## 1. Vision et Pitch

### 🌍 Qui sommes-nous : OrbitSowers Labs

**Équipe :** Camerounais 🇨🇲 basés à Montréal 🇨🇦  
**Mission :** Démocratiser l'agriculture de précision à l'échelle mondiale  
**Événement :** NASA Space Apps Challenge - Montréal

**Notre histoire :**
> "Nous sommes **OrbitSowers Labs**. Nos racines sont au Cameroun, où nos familles cultivent la terre. Aujourd'hui, nous vivons à Montréal. Entre ces deux mondes, nous avons découvert une vérité : la NASA offre des données satellites gratuites qui pourraient transformer l'agriculture mondiale, mais personne ne sait les utiliser.
> 
> **TerraGrow Academy**, c'est notre pont entre le ciel et la terre."

---

### 🎯 Concept en une phrase
**TerraGrow Academy** est un jeu éducatif à **portée mondiale** qui enseigne l'agriculture durable en utilisant de vraies données satellites NASA pour n'importe quelle région du monde.

---

### 🌍 Le problème
- **9 milliards d'humains en 2050** = besoin +70% production alimentaire
- **Agriculteurs africains, asiatiques, sud-américains** : 0 accès technologies spatiales
- **Gaspillage 40% eau** par manque de données
- **Changement climatique** frappe différemment chaque région
- **Technologies NASA existent** mais complexes et inaccessibles

---

### 💡 La solution : Architecture Hybride Mondiale

**Un jeu où VOUS choisissez OÙ cultiver :**

1. **Sélection localisation** 🗺️
   - Recherche : "Yaoundé, Cameroun" ou "Montréal, Québec"
   - Géolocalisation automatique
   - 15 régions mondiales pré-calculées (haute qualité)
   - API NASA pour n'importe où ailleurs

2. **Données réelles pour VOTRE région** 📡
   - Météo temps réel (NASA POWER API)
   - Humidité sol (SMAP - régions pré-calc)
   - Climat local automatiquement détecté

3. **Gameplay personnalisé** 🎮
   - 12 semaines gestion champ
   - Décisions : irrigation + fertilisation
   - Événements adaptés région (sécheresse Sahel vs gel Québec)

4. **Score et apprentissage** 📊
   - Rendement + durabilité
   - Conseils personnalisés
   - Comparaison avec moyenne région

---

### 🎮 Pourquoi "TerraGrow" ?
- **Terra** = La Terre + satellite Terra NASA + données terrestres
- **Grow** = Faire pousser cultures + grandir en connaissances
- **Academy** = Plateforme éducative mondiale

---

### 🎯 MVP = Minimum Viable Product

**CE QU'ON FAIT en 48h :**

✅ **Portée mondiale**
- Sélection localisation (recherche + géolocalisation)
- 15 régions mondiales pré-calculées
- API météo NASA pour couverture globale

✅ **Gameplay core**
- 1 champ, 12 semaines (1 saison)
- Choix 2-3 cultures selon région
- Irrigation + fertilisation

✅ **Architecture hybride**
- Données statiques (15 régions haute qualité)
- APIs temps réel (NASA POWER, Nominatim)
- Cache intelligent

✅ **Visualisations**
- Barre santé NDVI colorée
- Graphique évolution 12 semaines
- Carte localisation

✅ **Pédagogie**
- Tutoriel intégré
- Messages feedback
- Score rendement + durabilité

**CE QU'ON NE FAIT PAS (pour l'instant) :**
- ❌ Maladies/ravageurs (Niveau 1)
- ❌ Multi-champs (Niveau 1)
- ❌ Mode multijoueur (Niveau 2)
- ❌ Images satellites réelles (Niveau 2)
- ❌ Recommandations IA ML (Niveau 2)

---

### 📊 Pitch finale (5 minutes)

**Structure storytelling :**

**1. Qui sommes-nous (30s)**
> "OrbitSowers Labs. Camerounais à Montréal. Nos familles cultivent au Cameroun. Nous codons au Canada. Entre ces deux mondes, une mission : démocratiser l'agriculture spatiale."

**2. Problème (30s)**
> "Nos parents au Cameroun subissent sécheresses imprévisibles. Ici à Montréal, agriculteurs font face gels tardifs. La NASA a les données pour aider. Mais personne ne sait les utiliser."

**3. Solution (1min)**
> "TerraGrow : jeu éducatif mondial. Choisissez VOTRE région - Yaoundé, Montréal, Nairobi, n'importe où. Recevez données NASA RÉELLES pour votre climat. Apprenez à décider irrigation, fertilisation. Comprenez agriculture de précision en jouant."

**4. Démo live (2min)**
- Recherche "Yaoundé, Cameroun" → Climat détecté
- Jouer 2-3 semaines : irrigation, stress, pluie
- Changement région "Montréal" → Climat différent, mêmes outils
- Montrer graphique NDVI, score

**5. Données NASA (30s)**
> "NASA POWER : météo mondiale temps réel. SMAP : humidité sol. MODIS : santé végétation. GPM : précipitations. Toutes gratuites, toutes dans TerraGrow."

**6. Impact (30s)**
> "15 régions au MVP. 7 milliards à venir. De l'Afrique à l'Amérique, TerraGrow cultive l'avenir avec les yeux de la NASA dans le ciel."

---

## 2. User Stories MVP

### US1 - Sélection localisation mondiale
**En tant que** joueur  
**Je veux** choisir où je cultive dans le monde  
**Pour** jouer avec MON contexte climatique

**Critères d'acceptation :**
- [ ] Écran "Où cultivez-vous ?" au démarrage
- [ ] Bouton "📍 Détecter ma position" (géolocalisation)
- [ ] Barre recherche avec autocomplete (Nominatim API)
- [ ] Suggestions populaires affichées (Yaoundé, Montréal, Nairobi, etc.)
- [ ] Clic suggestion → Localisation sélectionnée
- [ ] Affichage : "📍 Yaoundé, Cameroun | 🌡️ Climat : Tropical savane"
- [ ] Bouton "Commencer" active partie

---

### US2 - Initialisation avec données région
**En tant que** joueur  
**Je veux** que le jeu charge les données de MA région  
**Pour** jouer avec conditions réalistes

**Critères d'acceptation :**
- [ ] Backend reçoit coordonnées (lat, lon)
- [ ] Si région populaire (15 pré-calc) → charge JSON haute qualité
- [ ] Sinon → appel NASA POWER API pour météo
- [ ] Affichage état initial :
  - Région : "Yaoundé, Cameroun"
  - Culture proposée : Maïs (adapté climat)
  - NDVI : 0.15, Humidité : 45%, Budget : $2000
  - Semaine 1/12
- [ ] Message bienvenue contextualisé : "Bienvenue à Yaoundé ! Saison des pluies débute. Gérez votre champ de maïs."

---

### US3 - Voir données satellites contextuelles
**En tant que** joueur  
**Je veux** voir l'état actuel spécifique à ma région  
**Pour** prendre décisions informées

**Critères d'acceptation :**
- [ ] Panel "Données satellites"
- [ ] Humidité sol actuelle (%)
- [ ] Précipitations prévues 7j (mm) - **temps réel NASA POWER**
- [ ] Température actuelle et prévue (°C)
- [ ] NDVI (barre colorée + valeur)
- [ ] Icônes claires (💧, ☀️, 🌱)
- [ ] Note source : "Données NASA en temps réel"

---

### US4 - Décider irrigation adaptée région
**En tant que** joueur  
**Je veux** irriguer selon disponibilité eau MA région  
**Pour** gérer stress hydrique réaliste

**Critères d'acceptation :**
- [ ] Slider irrigation : 0 / 10 / 20 / 30 mm
- [ ] Coût affiché en **USD** (ex: 20mm = $70)
- [ ] Eau disponible réservoir (adapté région : Yaoundé = 1500m³, Sahel = 500m³)
- [ ] Conseil contextualisé :
  - Région humide : "Humidité OK, irrigation optionnelle"
  - Région aride : "Humidité critique 18%, irrigation URGENTE"
- [ ] Tooltip : "💡 En région tropicale, sur-irrigation lessive nutriments"

---

### US5 - Décider fertilisation
**En tant que** joueur  
**Je veux** fertiliser pour booster croissance  
**Pour** optimiser rendement

**Critères d'acceptation :**
- [ ] Slider fertilisation : 0 / 50 / 100 kg N/ha
- [ ] Coût USD (ex: 50kg = $60)
- [ ] Impact visible semaine suivante (NDVI +0.05 à 0.10)
- [ ] Avertissement si sur-fertilisation : "⚠️ Risque lessivage"

---

### US6 - Appliquer décisions et simulation
**En tant que** joueur  
**Je veux** valider mes choix et voir conséquences  
**Pour** apprendre cause-effet

**Critères d'acceptation :**
- [ ] Bouton "✅ Valider semaine"
- [ ] Animation loading (1s) "Simulation en cours..."
- [ ] Backend :
  - Bilan hydrique : humidité_new = f(humidité, pluie_réelle, irrigation, ET)
  - Croissance NDVI : f(humidité, nutriments, température_réelle)
  - Événements aléatoires région (ex: canicule semaine 8 si Sahel)
- [ ] Mise à jour affichage :
  - NDVI nouvelle valeur
  - Barre couleur change (vert/jaune/rouge)
  - Humidité mise à jour
  - Budget déduit
  - Semaine +1
- [ ] Message feedback contextuel :
  - ✅ "Excellente irrigation ! Culture saine"
  - ⚠️ "Attention : stress hydrique léger"
  - 🚨 "Alerte : NDVI chute, stress sévère"

---

### US7 - Événements régionaux spécifiques
**En tant que** joueur  
**Je veux** affronter défis réels de MA région  
**Pour** comprendre diversité agriculture mondiale

**Critères d'acceptation :**
- [ ] Événements contextuels :
  - **Cameroun (Yaoundé)** : "☔ Pluies torrentielles ! Drainage limité, risque inondation"
  - **Québec (Montréal)** : "❄️ Alerte gel tardif ! Température 2°C, protection requise ?"
  - **Sahel (Maroua)** : "🌡️ Canicule extrême 42°C ! ET × 2, stress maximum"
- [ ] Événement apparaît aléatoirement selon climat région
- [ ] Choix joueur impacté : doit adapter stratégie
- [ ] Message pédagogique : "💡 En zone tropicale, drainage sol crucial saison pluies"

---

### US8 - Visualisation évolution NDVI
**En tant que** joueur  
**Je veux** voir graphiquement évolution santé culture  
**Pour** comprendre impact décisions long terme

**Critères d'acceptation :**
- [ ] Graphique ligne (Chart.js) : NDVI sur 12 semaines
- [ ] Axe X : Semaines 1-12
- [ ] Axe Y : NDVI 0-1
- [ ] Courbe mise à jour chaque semaine
- [ ] Zone colorée : Vert (optimal >0.6), Jaune (stress 0.4-0.6), Rouge (<0.4)
- [ ] Tooltip semaine : "Semaine 5 : NDVI 0.68 (sain), Pluie 25mm, Irrigation 15mm"

---

### US9 - Récolte et score contextualisé
**En tant que** joueur  
**Je veux** voir score comparé à moyenne MA région  
**Pour** évaluer performance relative

**Critères d'acceptation :**
- [ ] Semaine 12 : Bouton "🌾 Récolter"
- [ ] Calcul rendement (t/ha) selon NDVI intégré
- [ ] Comparaison :
  - "🏆 Votre rendement : 6.8 t/ha"
  - "📊 Moyenne Yaoundé : 5.2 t/ha (+30% !)"
  - "🌍 Moyenne mondiale maïs : 5.9 t/ha"
- [ ] Score durabilité (0-100) :
  - Efficacité eau : kg récolté / m³ eau utilisée
  - Lessivage azote (pénalité)
  - Note : "♻️ Durabilité : 78/100 (Bien)"
- [ ] Étoiles : ⭐⭐⭐⭐ (4/5)

---

### US10 - Conseils personnalisés région
**En tant que** joueur  
**Je veux** comprendre spécificités MA région  
**Pour** améliorer et apprendre

**Critères d'acceptation :**
- [ ] 2-3 messages personnalisés :
  - ✅ "Excellent : Adaptation pluies tropicales réussie !"
  - ⚠️ "Attention : Sur-irrigation semaines 7-9 → lessivage. En climat humide, vérifier humidité avant irriguer."
  - 💡 "Conseil Yaoundé : Saison sèche (déc-fév) nécessite irrigation régulière. Planifier réserves eau."
- [ ] Lien apprentissage : "📚 En savoir plus sur agriculture tropicale"
- [ ] Comparaison autre région : "🌍 Même culture au Québec nécessiterait 40% moins eau mais chauffage sol"

---

### US11 - Rejouer autre région
**En tant que** joueur  
**Je veux** essayer différentes régions  
**Pour** comprendre diversité agriculture mondiale

**Critères d'acceptation :**
- [ ] Bouton "🌍 Changer de région" écran final
- [ ] Retour sélection localisation
- [ ] Historique sauvegardé : "Régions jouées : Yaoundé (⭐⭐⭐⭐), Montréal (⭐⭐⭐)"
- [ ] Encouragement : "Essayez climat aride ! Maroua, Cameroun"

---

### US12 - Tutoriel contextuel première utilisation
**En tant que** nouveau joueur  
**Je veux** comprendre comment jouer  
**Pour** ne pas être perdu

**Critères d'acceptation :**
- [ ] Première partie : modal tutoriel (étapes 1-5)
- [ ] Étape 1 : "Bienvenue ! Choisissez votre région."
- [ ] Étape 2 : "Voici vos données satellites NASA. Humidité = santé racines."
- [ ] Étape 3 : "NDVI = santé feuilles. Vert = bon, jaune/rouge = stress."
- [ ] Étape 4 : "Décidez irrigation et fertilisation chaque semaine."
- [ ] Étape 5 : "Objectif : rendement élevé + durabilité. Bonne chance !"
- [ ] Checkbox "Ne plus afficher"
- [ ] Tooltips survol (💡) restent disponibles

---

## 3. WBS - Work Breakdown Structure

```
TerraGrow MVP v2.0 - Architecture Hybride (48h)
│
├── 0. PRÉ-HACKATHON (16-24h) - Toute équipe
│   ├── 0.1 Setup outils (2h)
│   │   ├── GitHub repo + branches
│   │   ├── Slack/Discord channels
│   │   └── Trello board
│   │
│   ├── 0.2 Préparation données (16-20h) - Data Scientist
│   │   ├── 0.2.1 Inscription NASA Earthdata (30 min)
│   │   ├── 0.2.2 Tests APIs NASA POWER (2h)
│   │   ├── 0.2.3 Préparation 15 régions statiques (12-16h)
│   │   │   ├── Cameroun : Yaoundé, Maroua, Douala
│   │   │   ├── Canada : Montréal, Prairies
│   │   │   ├── Kenya : Nairobi
│   │   │   ├── Nigeria : Kano
│   │   │   ├── Éthiopie : Addis-Abeba
│   │   │   ├── Inde : Punjab
│   │   │   ├── Brésil : São Paulo
│   │   │   ├── USA : Iowa
│   │   │   ├── France : Beauce
│   │   │   ├── Bangladesh : Dhaka
│   │   │   └── Argentine : Pampas
│   │   │   (Chaque région : SMAP, GPM, MODIS, climat, sol)
│   │   └── 0.2.4 Validation données (2h)
│   │
│   └── 0.3 Maquettes UI (2h) - Frontend + PM
│       ├── Wireframe sélection localisation
│       ├── Wireframe jeu principal
│       └── Palette couleurs
│
├── 1. DONNÉES & APIS (8h) - Data Scientist + Tech Lead
│   ├── 1.1 Services API (5h)
│   │   ├── 1.1.1 NASA POWER API wrapper (2h)
│   │   │   ├── Classe NASAPowerAPI
│   │   │   ├── get_weather(lat, lon, days)
│   │   │   └── Tests unitaires
│   │   │
│   │   ├── 1.1.2 Nominatim géocodage (1h)
│   │   │   ├── Classe GeocodingService
│   │   │   ├── search_location(query)
│   │   │   └── reverse_geocode(lat, lon)
│   │   │
│   │   ├── 1.1.3 DataProvider hybride (2h)
│   │   │   ├── Classe DataProvider
│   │   │   ├── get_game_data(lat, lon)
│   │   │   ├── Logique : cache → statique → API
│   │   │   └── find_closest_region()
│   │   │
│   │   └── 1.1.4 Tests intégration (bonus)
│   │
│   ├── 1.2 Structure données (2h)
│   │   ├── Format JSON standardisé
│   │   ├── Paramètres cultures (maïs, sorgho, blé)
│   │   └── Paramètres sols (loam, sandy, clay)
│   │
│   └── 1.3 Cache système (1h)
│       ├── Dict Python simple (MVP)
│       └── Logique TTL basique
│
├── 2. BACKEND (14h) - Tech Lead
│   ├── 2.1 Setup projet (1h)
│   │   ├── Structure dossiers (backend/, services/, models/)
│   │   ├── requirements.txt (Flask, requests, numpy, pandas)
│   │   └── Configuration (config.py)
│   │
│   ├── 2.2 Modèles (6h)
│   │   ├── 2.2.1 Classe Region (1h)
│   │   │   ├── Attributs : name, lat, lon, climate, soil_type
│   │   │   └── Méthode : load_parameters()
│   │   │
│   │   ├── 2.2.2 Classe Crop (2h)
│   │   │   ├── Attributs : type, ndvi, growth_rate, water_need
│   │   │   └── Méthode : calculate_growth(moisture, nutrients, temp)
│   │   │
│   │   ├── 2.2.3 Classe Soil (2h)
│   │   │   ├── Attributs : moisture, nitrogen, organic_matter
│   │   │   └── Méthode : update_moisture(rain, irrigation, et)
│   │   │
│   │   └── 2.2.4 Classe GameState (1h)
│   │       ├── Orchestration région + crop + sol
│   │       ├── Méthode : simulate_week()
│   │       └── Méthode : get_state()
│   │
│   ├── 2.3 Logique simulation (5h)
│   │   ├── 2.3.1 Bilan hydrique (2h)
│   │   │   ├── moisture_new = f(moisture, rain, irrig, et, drainage)
│   │   │   └── Paramètres adaptés type sol
│   │   │
│   │   ├── 2.3.2 Croissance NDVI (2h)
│   │   │   ├── Stress hydrique : f(moisture, optimal_moisture_region)
│   │   │   ├── Stress thermique : f(temp, optimal_temp_crop)
│   │   │   ├── Stress nutritionnel : f(nitrogen)
│   │   │   └── NDVI_new = NDVI + growth - stress
│   │   │
│   │   └── 2.3.3 Événements régionaux (1h)
│   │       ├── Probabilités selon climat
│   │       ├── Canicule, gel, pluie torrentielle
│   │       └── Impact paramétrable
│   │
│   └── 2.4 API Flask (2h)
│       ├── Route POST /api/init
│       │   ├── Reçoit : {lat, lon, crop_choice}
│       │   ├── Appelle : DataProvider.get_game_data()
│       │   └── Retourne : game_state initial
│       │
│       ├── Route POST /api/action
│       │   ├── Reçoit : {irrigation, fertilization}
│       │   ├── Appelle : GameState.simulate_week()
│       │   └── Retourne : new_state + feedback_messages
│       │
│       ├── Route GET /api/harvest
│       │   └── Retourne : scores + conseils
│       │
│       └── Route GET /api/search-location?q=query
│           └── Proxy Nominatim
│
├── 3. FRONTEND (12h) - Frontend Developer
│   ├── 3.1 Pages HTML (3h)
│   │   ├── 3.1.1 index.html - Sélection localisation (1.5h)
│   │   │   ├── Barre recherche + autocomplete
│   │   │   ├── Bouton géolocalisation
│   │   │   ├── Grid suggestions populaires
│   │   │   └── Carte mini (optionnel)
│   │   │
│   │   ├── 3.1.2 game.html - Jeu principal (1h)
│   │   │   ├── Header : Région, semaine, budget
│   │   │   ├── Main : 3 colonnes (données, champ, actions)
│   │   │   └── Footer : Messages
│   │   │
│   │   └── 3.1.3 results.html - Score final (30 min)
│   │       ├── Scores + comparaisons
│   │       └── Conseils personnalisés
│   │
│   ├── 3.2 Styles CSS (3h)
│   │   ├── Layout responsive (Grid CSS)
│   │   ├── Palette couleurs OrbitSowers
│   │   │   ├── Vert agriculture : #2ECC71
│   │   │   ├── Bleu eau : #3498DB
│   │   │   ├── Brun sol : #8B4513
│   │   │   └── Orange soleil : #F39C12
│   │   ├── Barre NDVI gradient (vert→jaune→rouge)
│   │   ├── Sliders stylisés
│   │   └── Animations transitions
│   │
│   ├── 3.3 JavaScript (5h)
│   │   ├── 3.3.1 location-selection.js (2h)
│   │   │   ├── Géolocalisation navigator.geolocation
│   │   │   ├── Fetch autocomplete Nominatim
│   │   │   ├── Sélection région → stockage lat/lon
│   │   │   └── Redirection vers jeu
│   │   │
│   │   ├── 3.3.2 api-client.js (1h)
│   │   │   ├── Classe TerraGrowAPI
│   │   │   ├── Méthodes : init(), action(), harvest()
│   │   │   └── Error handling
│   │   │
│   │   ├── 3.3.3 game.js (2h)
│   │   │   ├── État jeu (variables globales)
│   │   │   ├── Initialisation : appel API /init
│   │   │   ├── Event handlers sliders
│   │   │   ├── Validation semaine
│   │   │   ├── Mise à jour UI (NDVI, budget, semaine)
│   │   │   └── Messages feedback dynamiques
│   │   │
│   │   └── 3.3.4 charts.js (bonus si temps)
│   │       └── Chart.js graphique NDVI évolution
│   │
│   └── 3.4 Assets (1h)
│       ├── Icônes (FontAwesome ou Flaticon)
│       ├── Images régions (15 drapeaux/photos)
│       └── Logo OrbitSowers
│
├── 4. INTÉGRATION (8h) - Toute équipe
│   ├── 4.1 Connexion backend ↔ frontend (3h)
│   │   ├── Configuration CORS Flask
│   │   ├── Tests routes API
│   │   ├── Vérification flux données
│   │   └── Debugging erreurs
│   │
│   ├── 4.2 Tests end-to-end (3h)
│   │   ├── Scénario 1 : Yaoundé, maïs, saison normale
│   │   ├── Scénario 2 : Montréal, maïs, événement gel
│   │   ├── Scénario 3 : Région non pré-calc → API fallback
│   │   ├── Tests edge cases (humidité 0%, budget négatif)
│   │   └── Tests 3+ régions différentes
│   │
│   └── 4.3 Polissage (2h)
│       ├── Messages feedback améliorés
│       ├── Loading states (spinners API calls)
│       ├── Animations CSS
│       └── Responsive mobile (basique)
│
├── 5. PRÉSENTATION (6h) - PM + support équipe
│   ├── 5.1 Slides Google (2.5h)
│   │   ├── Diapo 1 : Titre + OrbitSowers Labs
│   │   ├── Diapo 2 : Qui sommes-nous (Cameroun → Montréal)
│   │   ├── Diapo 3 : Problème (agriculture + données NASA)
│   │   ├── Diapo 4 : Solution (TerraGrow portée mondiale)
│   │   ├── Diapo 5 : Architecture hybride (schéma)
│   │   ├── Diapo 6 : Démo screenshot (sélection région)
│   │   ├── Diapo 7 : Démo screenshot (gameplay)
│   │   ├── Diapo 8 : Données NASA (logos + sources)
│   │   ├── Diapo 9 : Impact (15 régions → mondial)
│   │   └── Diapo 10 : Roadmap + Call to action
│   │
│   ├── 5.2 Script pitch (1h)
│   │   ├── Répartition qui dit quoi
│   │   ├── Timing précis (5 min strict)
│   │   └── Transitions fluides
│   │
│   ├── 5.3 Répétitions (2h)
│   │   ├── Répétition 1 : Lecture script
│   │   ├── Répétition 2 : Avec slides
│   │   ├── Répétition 3 : Avec démo live
│   │   ├── Répétition 4 : Chronométré + feedback
│   │   └── Ajustements finaux
│   │
│   └── 5.4 Vidéo backup démo (30 min, optionnel)
│       └── Screencast 2 min au cas où démo plante
│
└── 6. DOCUMENTATION (2h) - Tech Lead
    ├── 6.1 README GitHub (1h)
    │   ├── Titre + description
    │   ├── Architecture (schéma)
    │   ├── Installation (étapes claires)
    │   ├── APIs utilisées + crédits
    │   ├── Régions supportées (liste 15)
    │   └── Licence MIT
    │
    └── 6.2 Commentaires code (1h)
        ├── Docstrings Python classes/fonctions
        └── Comments JavaScript fonctions clés
```

**Total estimé : 50h** (réparti 4 personnes × 12h/jour × 2j = 96h théoriques)  
**Marge : 46h** pour imprévus, pauses, debugging

---

## 4. Répartition des rôles

### 👥 Équipe OrbitSowers Labs (4 personnes)

#### Rôle 1 : Tech Lead / Backend Architect
**Nom :** _____________

**Responsabilités :**
- Architecture globale hybride
- Backend Python (Flask)
- Modèles simulation (bilan hydrique, NDVI)
- API REST endpoints
- Intégration services APIs

**Compétences requises :**
- Python avancé (OOP, async)
- Flask/FastAPI
- APIs REST
- Architecture microservices
- Git

**Livrables MVP :**
- [ ] Structure backend/ complète
- [ ] Classes Region, Crop, Soil, GameState
- [ ] Routes API fonctionnelles (/init, /action, /harvest)
- [ ] Intégration DataProvider hybride
- [ ] Tests unitaires basiques
- [ ] README technique

**Pré-hackathon (3h) :**
- Setup structure projet
- Tester NASA POWER API manuellement
- Prototyper DataProvider logique

---

#### Rôle 2 : Frontend Developer / UX
**Nom :** _____________

**Responsabilités :**
- Interface utilisateur (HTML/CSS/JS)
- Sélection localisation (recherche + géoloc)
- Gameplay interface
- Appels API backend
- Visualisations (graphiques)
- Expérience utilisateur fluide

**Compétences requises :**
- HTML5, CSS3 (Grid, Flexbox)
- JavaScript (ES6+, Fetch API)
- Chart.js ou équivalent
- Geolocation API
- UX design

**Livrables MVP :**
- [ ] Pages : location-select, game, results
- [ ] CSS responsive et stylisé
- [ ] JavaScript : api-client, game-logic, location-search
- [ ] Graphique NDVI évolution
- [ ] Loading states + error handling
- [ ] Assets (icônes, images régions)

**Pré-hackathon (2h) :**
- Maquettes Figma (wireframes)
- Tester Nominatim API autocomplete
- Setup Chart.js

---

#### Rôle 3 : Data Scientist / APIs Specialist
**Nom :** _____________

**Responsabilités :**
- Préparation 15 régions mondiales (JSON)
- Intégration APIs NASA (POWER)
- Services APIs (wrappers Python)
- Validation cohérence données
- Tests APIs
- Support modèles simulation

**Compétences requises :**
- Python (pandas, xarray, requests)
- APIs REST (NASA Earthdata)
- Analyse données géospatiales
- JSON manipulation
- Connaissance agronomie (bonus)

**Livrables MVP :**
- [ ] 15 fichiers JSON régions (data/regions/)
- [ ] Classe NASAPowerAPI fonctionnelle
- [ ] Classe GeocodingService (Nominatim)
- [ ] Classe DataProvider hybride (avec Tech Lead)
- [ ] Documentation sources données
- [ ] Tests API rate limits

**Pré-hackathon (16-20h) : CRITIQUE**
- Inscription NASA Earthdata
- Télécharger données 15 régions :
  - Cameroun : Yaoundé (3.87°N, 11.52°E), Maroua (10.6°N, 14.3°E)
  - Canada : Montréal (45.5°N, -73.6°W)
  - Kenya : Nairobi (-1.28°N, 36.82°E)
  - + 11 autres régions mondiales
- Formater JSON standardisé
- Valider cohérence (pas de NaN, valeurs réalistes)

---

#### Rôle 4 : Product Manager / Storyteller
**Nom :** _____________

**Responsabilités :**
- Vision produit (ce document)
- Coordination équipe
- User Stories validation
- Storytelling pitch OrbitSowers
- Présentation finale (slides + speech)
- Tests utilisateurs

**Compétences requises :**
- Communication excellente
- Storytelling émotionnel
- Organisation / gestion temps
- PowerPoint/Google Slides
- Compréhension technique (pas besoin coder)

**Livrables MVP :**
- [ ] Document vision (ce fichier !)
- [ ] User Stories détaillées
- [ ] Slides présentation (10 diapos)
- [ ] Script pitch 5 min (mémorisé)
- [ ] Coordination tests démo
- [ ] Feedback utilisateurs internes

**Pré-hackathon (3h) :**
- Finaliser ce document avec équipe
- Draft slides (template)
- Écrire script storytelling OrbitSowers
- Lister 15 régions avec Data Scientist

---

### 🔄 Collaboration transversale

**Binômes recommandés :**

**Tech Lead + Data Scientist** :
- Architecture hybride DataProvider
- Intégration NASA POWER API
- Modèles simulation (calibration paramètres)

**Frontend + PM** :
- UX sélection localisation
- Messages feedback utilisateur
- Tests gameplay fluide

**Toute équipe** :
- Stand-ups 2×/jour (9h, 14h)
- Tests intégration Jour 1 soir
- Debugging collectif
- Répétitions pitch

---

## 5. Organisation du temps - Méthode Hackathon

### ⏰ Planning 48h détaillé

#### **PRÉ-HACKATHON (J-7 à J-1)**

**1 semaine avant :**
- [ ] **Réunion kickoff équipe** (3h) - Tous
  - Lecture ce document v2.0 ensemble
  - Validation architecture hybride
  - Attribution rôles précis
  - Setup GitHub + Slack + Trello
  - Définir 15 régions mondiales liste

**5 jours avant :**
- [ ] **Data Scientist : START préparation données** (16-20h étalées)
  - Inscription NASA Earthdata
  - Tests APIs (POWER, Nominatim)
  - Début téléchargement 15 régions
  - Format JSON standardisé

**3 jours avant :**
- [ ] **Tech Lead : Setup structure projet** (3h)
  - Repo GitHub initialisé
  - Structure dossiers backend/
  - requirements.txt
  - Prototype DataProvider logique
  
- [ ] **Frontend : Maquettes** (2h)
  - Wireframes Figma (location select, game)
  - Palette couleurs OrbitSowers
  
- [ ] **PM : Draft slides** (2h)
  - Template Google Slides
  - Histoire OrbitSowers rédigée

**Veille hackathon (J-1) :**
- [ ] **Data Scientist : 15 régions 100% prêtes**
  - Validation finale données
  - Tests cohérence
  - Backup local (pas dépendre internet)

- [ ] **Check liste matériel**
  - Laptops chargés
  - Câbles HDMI/VGA
  - Chargeurs
  - Snacks, café ☕

- [ ] **Repos ! Sommeil 8h minimum** 😴

---

#### **JOUR 1 - Samedi (Architecture + Core)**

**08h30 - 09h00 : Arrivée, setup**
- ☕ Café, installation stations
- Test connexion internet
- Vérifier données locales chargées

**09h00 - 09h30 : Briefing équipe**
- Rappel vision TerraGrow
- Objectif Jour 1 : **Backend + Frontend basiques fonctionnels**
- Répartition tâches Sprint 1

---

**09h30 - 13h00 : SPRINT 1 - Fondations**

| Qui | Tâches (3h30) | Livrables |
|-----|---------------|-----------|
| **Tech Lead** | • Setup Flask app.py<br>• Classes Crop, Soil basiques<br>• Route /api/init (squelette) | Backend structure |
| **Frontend** | • HTML location-select.html<br>• CSS layout + couleurs<br>• JS recherche Nominatim (test) | Page sélection |
| **Data Scientist** | • NASAPowerAPI classe<br>• Tests API météo temps réel<br>• DataProvider logique hybride | Services APIs |
| **PM** | • User Stories validation tests<br>• Slides diapos 1-3 (identité)<br>• Préparation script storytelling | Présentation début |

**Checkpoint 13h :**
- ✅ Backend démarre sans erreur
- ✅ Frontend page localisation affiche
- ✅ API NASA POWER retourne données
- ✅ Slides identité OrbitSowers OK

---

**13h00 - 14h00 : Pause déjeuner 🍕**
- Manger ensemble, détente
- Discussions informelles projet
- PAS de travail (vraie coupure)

---

**14h00 - 18h00 : SPRINT 2 - Intégration Core**

| Qui | Tâches (4h) | Livrables |
|-----|-------------|-----------|
| **Tech Lead** | • Modèles complets (GameState)<br>• Bilan hydrique simulation<br>• Route /api/init complète<br>• Route /api/action (base) | API fonctionnelle |
| **Frontend** | • game.html structure<br>• CSS gameplay<br>• api-client.js<br>• Appel /api/init | Connexion backend |
| **Data Scientist** | • DataProvider find_closest_region()<br>• Cache dict implémentation<br>• Aide Tech Lead modèles NDVI | Hybride fonctionnel |
| **PM** | • Tests UX page localisation<br>• Feedback utilisateur interne<br>• Slides diapos 4-6 (solution) | UX validée |

**16h00 : Sync 15 min**
- Tour de table : Avancement, blocages
- Aide mutuelle si nécessaire

**Objectif 18h :**
- ✅ Sélection région fonctionne (recherche + suggestions)
- ✅ API /init retourne game state
- ✅ Frontend affiche données initiales
- ✅ 1 tour jouable (même sans calculs parfaits)

---

**18h00 - 19h00 : DÉMO INTERNE CRITIQUE**

**Scénario test complet :**
1. Lancer app
2. Rechercher "Yaoundé"
3. Démarrer jeu
4. Jouer 2-3 semaines (irrigation + fertilisation)
5. Voir NDVI évoluer

**Évaluation honnête :**
- ✅ **Fonctionne** → Continue Sprint 3 polissage
- ⚠️ **Bugs mineurs** → Liste priorités, fix rapide
- ❌ **Cassé** → Décision ruthless : simplifier scope

---

**19h00 - 22h00 : SPRINT 3 - Polissage Jour 1**

**Si MVP core fonctionne (cas idéal) :**

| Qui | Tâches | Livrables |
|-----|--------|-----------|
| **Tech Lead** | • Croissance NDVI optimisée<br>• Événements régionaux<br>• Route /api/harvest | Gameplay complet |
| **Frontend** | • Graphique NDVI (Chart.js)<br>• Messages feedback<br>• results.html | Visualisations |
| **Data Scientist** | • Calibration paramètres<br>• Tests 5+ régions<br>• Fallback API POWER si région inconnue | Robustesse |
| **PM** | • Slides diapos 7-10 (données, impact)<br>• Script pitch v1<br>• Tests gameplay narration | Présentation 80% |

**Si bugs critiques :**
- 🔥 **Toute équipe** sur debugging
- Prioriser : Backend simulation > Visualisations
- Simplifier si nécessaire (enlever graphique si bloque)

---

**22h00 : Checkpoint fin Jour 1**

**Checklist :**
- [ ] Sélection localisation fonctionne
- [ ] API backend stable (/init, /action)
- [ ] 12 semaines jouables début à fin
- [ ] Score final calculé (même basique)
- [ ] 0 erreurs console bloquantes

**Actions :**
- Git commit (tag v1.0-day1)
- Liste TODOs Jour 2 (post-it ou Trello)
- Plan bataille dimanche

**Coucher 23h MAX → Réveil 7h30 (8h30 sommeil)** 😴

---

#### **JOUR 2 - Dimanche (Polish + Présentation)**

**08h00 - 09h00 : Arrivée échelonnée**
- ☕ Café, réveil en douceur
- Test rapide : app marche encore ?
- Review code frais (bugs évidents ?)

**09h00 - 09h15 : Stand-up rapide**
- Chacun : "Fait hier / Fera aujourd'hui / Besoin aide sur..."
- Ajustements plan si nécessaire

---

**09h15 - 12h00 : SPRINT 4 - Features finales + Tests**

| Qui | Tâches (2h45) | Livrables |
|-----|---------------|-----------|
| **Tech Lead** | • Scoring durabilité détaillé<br>• Conseils personnalisés région<br>• Tests edge cases (budget 0, etc.) | Logique complète |
| **Frontend** | • Tutoriel modal première fois<br>• Tooltips explicatifs<br>• Animations CSS (transitions)<br>• Responsive mobile basique | UX polie |
| **Data Scientist** | • Tests 10+ régions différentes<br>• Validation cohérence scores<br>• Documentation API sources | Robustesse validée |
| **PM** | • Tests utilisateurs externes (inviter autre équipe)<br>• Noter feedback<br>• Ajustements UX rapides | UX optimisée |

**11h00 : Test utilisateur externe**
- Inviter 1-2 personnes autre équipe
- Observer jouer SANS aider
- Noter : Où bloquent ? Confusions ?
- Itérer rapidement

---

**12h00 - 13h00 : Pause déjeuner + Répétition pitch v1**

**Déjeuner (30 min)**

**Répétition 1 (30 min) :**
- PM présente pitch complet 5 min
- Équipe chronomètre strict
- Feedback : Trop long ? Pas clair ?
- Ajustements script

---

**13h00 - 15h30 : SPRINT 5 - Présentation finale**

| Qui | Tâches | Livrables |
|-----|--------|-----------|
| **PM** | • Slides finales (ajustements)<br>• Script pitch v2<br>• Répétitions ×3 | Pitch parfait |
| **Frontend** | • Mode démo (données pré-remplies)<br>• Vérifier aucun bug affichage<br>• Backup screenshots | Démo fluide |
| **Tech Lead** | • README GitHub complet<br>• Commentaires code<br>• Git commit final (tag v1.0-release) | Documentation |
| **Data Scientist** | • Documentation APIs + crédits<br>• Liste 15 régions README<br>• Tests finaux API fallback | Crédits NASA |

**14h00 : Répétition pitch complète #2**
- Toute équipe présente (répartir slides)
- Chronométrer (strict 5 min)
- Démo live 2 min intégrée
- Feedback + ajustements

**15h00 : Répétition pitch finale #3**
- Conditions réelles (debout, comme devant jury)
- Tester démo offline (au cas où internet fail)
- Vérifier transitions fluides
- Confiance ! 💪

---

**15h30 - 16h30 : Finalisation**

**Toute équipe :**
- [ ] Code nettoyé (supprimer debug prints, comments inutiles)
- [ ] README complet avec screenshots
- [ ] Slides finales (export PDF backup)
- [ ] Démo testée 5× (fonctionne offline)
- [ ] Vidéo screencast 2 min (optionnel backup)

**Checklist présentation :**
- [ ] Laptop chargé 100%
- [ ] Adaptateur HDMI/VGA testé
- [ ] Code en local (pas dépendre GitHub)
- [ ] Démo fonctionne sans internet
- [ ] Slides accessibles (Google + PDF local)
- [ ] Eau, mouchoirs (stress !)

---

**16h30 - 17h00 : Calme avant tempête**

- Respiration, méditation (5 min)
- Review mentale pitch (pas sur-répéter)
- Confiance en travail accompli
- "On a donné notre maximum, fierté quel que soit résultat"

---

**17h00 - 18h00 : PRÉSENTATION 🎉**

**Pitch 5 min :**
1. Identité OrbitSowers (30s)
2. Problème (30s)
3. Solution TerraGrow (1min)
4. **Démo live** (2min)
   - Recherche "Yaoundé" → Démarrage
   - Jouer 2 semaines rapide
   - Changer région "Montréal" → Différence
   - Montrer graphique NDVI
5. Données NASA (30s)
6. Impact mondial (30s)

**Q&A (5 min) :**
- Écouter vraiment questions
- Réponses concises et honnêtes
- Si ne sait pas : "Excellente question, c'est notre prochaine étape recherche"

**Après présentation :**
- Respirer ! 😮‍💨
- Fierté équipe 🎊
- Peu importe résultat : Vous avez LIVRÉ 🚀

---

## 6. Outils pour coordination

### 💻 Stack outils

#### **GitHub - Code & Versioning**
**URL :** github.com/orbitSowers/terragrow

**Structure branches :**
```
main (production)
├── dev (développement actif)
├── feature/location-select
├── feature/api-integration
├── feature/game-simulation
└── feature/frontend-ui
```

**Règles commits :**
- Fréquence : Toutes les 1-2h
- Messages clairs : "Add NASA POWER API integration" pas "update"
- Pull avant push (éviter conflits)

---

#### **Trello - Kanban**
**URL :** trello.com/b/terragrow-mvp

**Listes (colonnes) :**
1. **Backlog** : Toutes features possibles
2. **To Do Jour 1** : Samedi priorités
3. **To Do Jour 2** : Dimanche priorités
4. **In Progress** : Actuellement travaillé (limite 2 cards/personne)
5. **Review** : À tester
6. **Done** : ✅ Terminé

**Cartes exemples :**
- "US2 - Initialisation données région" | Assigné: Data Sci | Label: 🔴 P0 | Due: Sam 13h
- "Graphique NDVI Chart.js" | Assigné: Frontend | Label: 🟡 P1 | Due: Dim 12h

---

#### **Slack - Communication**
**Channels :**
- `#general` : Annonces, stand-ups
- `#backend` : Tech Lead + Data Scientist
- `#frontend` : Frontend Dev
- `#apis` : Discussions APIs NASA
- `#presentation` : PM + slides
- `#random` : Mèmes, motivation, photos équipe 📸

**Règles :**
- @channel = urgence uniquement
- Threads pour discussions (garder canal propre)
- Pas messages 23h-7h (respecter sommeil)
- Emojis reactions pour quick feedback (👍, ✅, 🚀)

---

#### **Google Drive - Documents**
**Structure :**
```
TerraGrow OrbitSowers/
├── 01_Vision/
│   └── MVP_Guide_v2.0.pdf (ce document)
├── 02_Presentations/
│   ├── Pitch_Slides.pptx
│   └── Demo_Video.mp4
├── 03_Ressources/
│   ├── APIs_Documentation.md
│   ├── 15_Regions_List.xlsx
│   └── Storytelling_Script.docx
└── 04_Assets/
    ├── Logo_OrbitSowers.png
    ├── Regions_Photos/ (15 images)
    └── Icons/
```

---

#### **Figma - Maquettes** (optionnel)
**URL :** figma.com/terragrow-mvp

**Frames :**
- Location Selection (desktop + mobile)
- Game Main (desktop)
- Results Screen

**Avantages :**
- Collaboration temps réel
- Feedback visuel rapide
- Export assets (PNG icons)

---

### 📊 Tableau suivi temps réel

**Google Sheets partagé :**

| Heure | Tech Lead | Frontend | Data Sci | PM | Notes |
|-------|-----------|----------|----------|----|-------|
| 09h30 | Setup Flask ⏳ | HTML location ✅ | NASA API test ⏳ | Slides draft ✅ | Bon démarrage |
| 11h00 | Models Crop ⏳ | CSS layout ⏳ | DataProvider ⏳ | US tests ⏳ | Sur la bonne voie |
| 13h00 | API /init ✅ | Search Nominatim ✅ | 15 régions OK ✅ | Slides 1-3 ✅ | **Checkpoint OK** |
| ... | ... | ... | ... | ... | ... |

**Légende :**
- ⏳ En cours
- ✅ Terminé
- ❌ Bloqué
- ⚠️ Besoin aide
- 🔥 Urgence

---

### 🚨 Gestion blocages

**Protocole si bloqué >30 min :**

1. **Signal** : Poster Slack #general
   ```
   🚨 @channel Bloqué sur intégration NASA API
   Erreur: 401 Unauthorized
   Besoin aide backend
   ```

2. **Mob programming** : Toute équipe stop 10 min
   - Brainstorm collectif
   - Partage écran
   - Debugging ensemble

3. **Décision rapide** (5 min max) :
   - ✅ Continuer avec solution trouvée
   - 🔄 Pivoter (approche différente)
   - ❌ Enlever feature (simplifier scope)

**Exemples blocages typiques :**

| Blocage | Solution rapide |
|---------|-----------------|
| CORS errors Flask | `CORS(app, origins='*')` dans app.py |
| API NASA rate limit | Utiliser données statiques fallback |
| Nominatim timeout | Hardcoder 15 suggestions sans autocomplete |
| Chart.js crash | Tableau simple HTML si pas temps debug |
| Calculs NDVI faux | Simplifier formule, valider cas test |

---

### 📱 Communication d'urgence

**Numéros téléphone équipe** (au cas où Slack down) :
- Tech Lead : _______________
- Frontend : _______________
- Data Sci : _______________
- PM : _______________

**Point de rencontre physique :** [Salle hackathon Space Apps Montréal]

---

## 📌 Résumé Ultra-Rapide (Mémo 1 page)

### 🎯 TerraGrow MVP v2.0 en 5 points

**1. VISION**
- Jeu éducatif agriculture mondiale
- Architecture hybride (statique + APIs)
- 15 régions pré-calc + NASA POWER API
- Storytelling OrbitSowers (Cameroun 🇨🇲 → Montréal 🇨🇦)

**2. GAMEPLAY**
- Sélection localisation (recherche/géoloc)
- 12 semaines gestion champ
- Irrigation + fertilisation
- Score rendement + durabilité

**3. DONNÉES**
- **Statique** : 15 régions JSON haute qualité
- **API** : NASA POWER (météo temps réel)
- **Géocodage** : Nominatim (recherche lieux)
- **Fallback** : Région proche si non pré-calc

**4. TECH STACK**
- **Backend** : Python + Flask
- **Frontend** : HTML + CSS + JavaScript vanilla
- **APIs** : NASA POWER, Nominatim
- **Cache** : Dict Python simple
- **Viz** : Chart.js (graphique NDVI)

**5. PRIORITÉS ABSOLUES**
- ✅ Sélection région fonctionne
- ✅ API backend stable
- ✅ 12 semaines jouables
- ✅ Score final calculé
- ✅ Pitch OrbitSowers mémorisé

---

### ⚡ Checklist Go/No-Go Jour 1 (18h)

**MUST HAVE (MVP minimum) :**
- [ ] Recherche localisation retourne résultats
- [ ] Backend /init retourne game_state
- [ ] Frontend affiche NDVI, humidité, budget
- [ ] Décision irrigation mise à jour backend
- [ ] Au moins 3 régions testées (Yaoundé, Montréal, +1)

**Si OUI aux 5 → Continue polissage**  
**Si NON → Simplifier ruthlessly**

---

### 🏆 Différenciateurs TerraGrow vs. autres équipes

| TerraGrow OrbitSowers | Équipes typiques |
|-----------------------|------------------|
| 🌍 Portée mondiale (15 régions) | 1-2 régions fixes |
| 🔌 Architecture APIs hybride | Data statique pure |
| 📡 Météo temps réel NASA | Données historiques |
| 🎭 Storytelling authentique (Cameroun→Canada) | Projet générique |
| 🌟 Vision scalable crédible | Prototype hackathon |

---

### 📞 Contacts urgence

**Mentors NASA Space Apps Montréal :** [À compléter sur place]  
**Support technique événement :** [À compléter]  
**Wifi backup :** Hotspot téléphone si internet fail

---

## 🚀 Message final équipe OrbitSowers

> **De Yaoundé à Montréal, de la terre au ciel, nous sommes OrbitSowers Labs.**
> 
> Ce weekend, nous ne construisons pas juste un jeu. Nous bâtissons un pont entre nos racines africaines et notre nouvelle maison canadienne. Entre les satellites de la NASA et les champs de nos parents. Entre la technologie spatiale et l'agriculture ancestrale.
> 
> **TerraGrow**, c'est notre histoire. C'est notre mission. C'est notre contribution au monde.
> 
> 48 heures. 4 personnes. 1 vision : **Cultiver l'avenir avec les yeux de la NASA**.
> 
> Allons-y. Semons. Cultivons. Récoltons. 🌍🌾🚀

**— OrbitSowers Labs, NASA Space Apps Challenge Montréal 2025**

---

**🎯 Validez-vous ce plan MVP v2.0 ?**

**Document créé par et pour OrbitSowers Labs**  
**TerraGrow Academy - MVP Architecture Hybride**  
**Version 2.0 - Octobre 2025**