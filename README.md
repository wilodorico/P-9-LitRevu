# LITRevu - Application de critiques de livres et d’articles

## 📖 Présentation
LITRevu est une application web permettant aux utilisateurs de demander et publier des critiques de livres ou d’articles. Elle offre également la possibilité de rechercher des œuvres intéressantes à lire en se basant sur les critiques partagées par la communauté.

## 🚀 Fonctionnalités principales
- **Publication de critiques** : Les utilisateurs peuvent partager leurs avis sur des livres ou des articles.
- **Demande de critiques** : Créez un billet pour solliciter une critique sur une œuvre spécifique.
- **Recherche d'œuvres** : Découvrez des livres ou articles recommandés par la communauté.
- **Flux personnalisé** : Affichez les publications des utilisateurs suivis, vos propres billets et critiques, et les réponses à vos billets.
- **Système de suivi** : Suivez d'autres utilisateurs pour enrichir votre flux de contenus pertinents.
- **Gestion des billets et critiques** : Modifiez ou supprimez vos publications à tout moment.
- **Authentification** : Inscription, connexion

## 🛠️ Technologies utilisées
[![Django](https://img.shields.io/badge/Django-%23092E20.svg?logo=django&logoColor=white)](#)
[![HTML](https://img.shields.io/badge/HTML-%23E34F26.svg?logo=html5&logoColor=white)](#)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=000)](#)
[![HTMX](https://img.shields.io/badge/HTMX-36C?logo=htmx&logoColor=fff)](#)
[![TailwindCSS](https://img.shields.io/badge/Tailwind%20CSS-%2338B2AC.svg?logo=tailwind-css&logoColor=white)](#)
[![Flowbite](https://img.shields.io/badge/Flowbite-UIcomponents-%2338BDF8?logo=https://flowbite.com/images/logo.svg)](#)

## 🛠️ Prérequis
- Python 3.10+
- Django 4.2+
- Node.js (pour Tailwind css)
- pip

## 📦 Installation
1. **Cloner le dépôt GitHub**
```bash
git clone https://github.com/wilodorico/P-9-LitRevu.git
cd P-9-LitRevu
```

2. **Créer et activer l'environnement virtuel**
```bash
python -m venv venv
source venv/bin/activate # Sur macOS/Linux
venv\Scripts\activate # Sur Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Appliquer les migrations de la base de données**
```bash
python manage.py migrate
```

5. **Lancer le serveur local**
```bash
python manage.py runserver
```

L'application sera accessible à l'adresse : `http://localhost:8000`

## 🔑 Accès aux données de test
1. Admin (Pour accéder au site d'administration)
- **Nom d'utilisateur** : `admin`
- **Mot de passe** : `admin`
2. Marie
- **Nom d'utilisateur** : `marie`
- **Mot de passe** : `marie12345`
3. Jack
- **Nom d'utilisateur** : `jack`
- **Mot de passe** : `jack12345`
4. Joe
- **Nom d'utilisateur** : `joe`
- **Mot de passe** : `joe12345`

## 💡 Utilisation
- Accédez à la page d'accueil pour vous connecter ou vous inscrire.
- Explorez votre flux personnalisé.
- Publiez des billets et des critiques via les formulaires dédiés.
- Suivez d'autres utilisateurs pour enrichir votre flux.
