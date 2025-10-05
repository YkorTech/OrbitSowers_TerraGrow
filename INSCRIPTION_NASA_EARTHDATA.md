# 📝 Guide d'inscription NASA Earthdata

## 🎯 Pourquoi s'inscrire ?

Pour accéder aux données satellites avancées :
- **SMAP** : Humidité du sol mesurée par satellite
- **MODIS** : NDVI réel observé depuis l'espace
- **GPM** : Précipitations haute résolution

---

## 📋 Étapes d'inscription (5 minutes)

### 1. Aller sur le site NASA Earthdata

**URL** : https://urs.earthdata.nasa.gov/users/new

### 2. Remplir le formulaire

**Informations requises** :

| Champ | Que mettre |
|-------|------------|
| **Username** | Votre choix (ex: `ykor_terragrow`) |
| **Email** | Votre email valide |
| **Password** | Mot de passe sécurisé |
| **Confirm Password** | Même mot de passe |
| **First Name** | Votre prénom |
| **Last Name** | Votre nom |
| **Country** | Cameroun ou Canada |
| **Affiliation** | `NASA Space Apps Challenge - OrbitSowers Labs` |
| **Study Area** | Agriculture, Remote Sensing |

**User Profile** :
- **User Type** : Research
- **How will you use NASA data?** :
  ```
  Educational game for precision agriculture using SMAP soil moisture
  and MODIS vegetation data. NASA Space Apps Challenge 2025 project.
  ```

### 3. Accepter les conditions

- [x] Accepter Terms of Use
- [x] Accepter Data Policy

### 4. Cliquer "Register for Earthdata Login"

### 5. Vérifier votre email

Un email de confirmation sera envoyé à votre adresse.
**Cliquer sur le lien** dans l'email pour activer le compte.

---

## ✅ Vérification

Une fois inscrit :

1. Se connecter sur : https://urs.earthdata.nasa.gov/
2. Aller dans **My Applications**
3. Approuver les applications suivantes :

**Applications à approuver** :
- [x] **NASA GESDISC DATA ARCHIVE** (pour SMAP)
- [x] **LP DAAC Data Pool** (pour MODIS)
- [x] **GES DISC** (pour GPM)

---

## 🔑 Sauvegarder vos identifiants

Une fois inscrit, NOTEZ :

```
Username: ___________________
Password: ___________________
```

**⚠️ IMPORTANT** : Ne partagez jamais ces identifiants publiquement !

---

## 📁 Créer fichier .env

Dans le dossier `backend/`, créer un fichier `.env` :

```bash
# Fichier: backend/.env
NASA_EARTHDATA_USERNAME=votre_username_ici
NASA_EARTHDATA_PASSWORD=votre_password_ici
```

**Ce fichier est dans .gitignore** (pas partagé sur GitHub)

---

## ⏱️ Temps estimé

- **Inscription** : 3 minutes
- **Vérification email** : 2 minutes
- **Approbation applications** : 2 minutes

**Total** : ~7 minutes

---

## 🆘 En cas de problème

### Problème : Email non reçu
**Solution** : Vérifier spam, attendre 10 min, ou utiliser autre email

### Problème : Compte déjà existant
**Solution** : Utiliser "Forgot Password" pour réinitialiser

### Problème : Accès données refusé
**Solution** : Vérifier applications approuvées dans "My Applications"

---

## ✅ Checklist finale

Avant de continuer :

- [ ] Compte créé et email vérifié
- [ ] Applications GESDISC et LP DAAC approuvées
- [ ] Fichier `.env` créé avec username/password
- [ ] Testé connexion sur https://urs.earthdata.nasa.gov/

**Une fois tout ✅ → Retour au code !**
