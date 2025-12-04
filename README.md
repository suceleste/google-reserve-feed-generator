# 📍 Google Action Center | Feed Generator & Sync Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Google Maps](https://img.shields.io/badge/Google_Maps-Reserve-4285F4?style=for-the-badge&logo=googlemaps&logoColor=white)](https://www.google.com/maps)
[![JSON](https://img.shields.io/badge/Data-JSON_Schema-black?style=for-the-badge&logo=json)](https://json-schema.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

> **Solution d'ingénierie de données (ETL)** permettant l'intégration complète d'établissements physiques dans l'écosystème **Reserve with Google**.
> Ce projet automatise la génération, la validation et le déploiement des flux de données (Feeds) requis par Google pour activer le bouton "Réserver" sur Maps et Search.

---

## 🎯 Contexte & Enjeux Techniques

L'intégration au **Google Action Center** impose des contraintes techniques strictes pour garantir la fiabilité des réservations en temps réel :
1.  **Structure de données normée :** Respect des schémas JSON propriétaires `Entity`, `Service` et `Action`.
2.  **Fréquence de mise à jour :** Obligation d'upload quotidien (Keep-alive) pour maintenir le statut "Actif" du partenaire.
3.  **Validation Sandbox :** Nécessité de générer des jeux de données volumineux (Mocking/Dummy Data) pour satisfaire les quotas de validation de l'API Google.

Ce projet répond à ces problématiques via une architecture automatisée et sans maintenance.

---

## ⚙️ Fonctionnalités du Pipeline

### 1. Data Mapping & Transformation
Transformation des données brutes du catalogue client (90+ services, tarifs variables, durées, catégories) en format standardisé Google.
* **Conversion de types :** Gestion des prix en micro-montants (ex: 10€ = 10000000) et des durées en secondes.
* **Intégrité référentielle :** Garantie de la cohérence des IDs entre `Entity` (Lieu), `Service` (Offre) et `Action` (Deep Link).

### 2. Moteur de Synchronisation SFTP (`Upload_Google.py`)
Script Python robuste pour l'envoi sécurisé des données vers l'infrastructure Google (`partnerupload.google.com`).
* **Authentification Sécurisée :** Gestion de la connexion via clé privée SSH (`id_rsa`).
* **Rotation & Versionning :** Renommage automatique des fichiers avec **Timestamp UNIX** pour assurer l'unicité et le suivi des versions côté Google.
* **Génération des Descripteurs :** Création dynamique des fichiers `.filesetdesc.json` requis par l'ingestion Google.
* **Logging Avancé :** Traçabilité complète des opérations (Succès/Échec) dans `activity.log`.

---

## 📂 Architecture du Projet

```bash
.
├── action/                   # Flux définissant les liens de réservation (Deep links)
│   ├── action_template.json
│   └── reservewithgoogle.action.v2-xxxx.filesetdesc.json
├── entity/                   # Flux définissant les établissements (Metadata)
│   ├── entity_template.json
│   └── reservewithgoogle.entity-xxxx.filesetdesc.json
├── service/                  # Flux du catalogue complet (Offres & Tarifs)
│   ├── service_template.json
│   └── glam.service.v0-xxxx.filesetdesc.json
├── Upload_Google.py          # Script principal d'orchestration et d'upload (ETL)
├── id_rsa                    # Clé SSH (exclue du repo via .gitignore pour sécurité)
├── activity.log              # Logs d'exécution du pipeline
├── LICENSE                   # Licence MIT
└── README.md                 # Documentation technique
```
## 🚀 Installation & Déploiement

### Prérequis
* **Python 3.x** installé sur la machine.
* La clé SSH privée fournie par Google (format OpenSSH).

### 1. Installation des dépendances
Ce projet utilise `paramiko` pour gérer la connexion SFTP sécurisée.

```bash
pip install paramiko
```
### Configuration
Placez votre clé privée SSH fournie par Google dans la racine sous le nom id_rsa.

Configurez vos identifiants SFTP dans Upload_Google.py :

````Python
SFTP_HOST = "partnerupload.google.com"
SFTP_USER = "votre-username-google-partner"
````

### Exécution Automatisée
Le script est conçu pour être exécuté via une tâche planifiée (CRON sur Linux ou Task Scheduler sur Windows) afin d'assurer la fréquence quotidienne exigée par Google.

```Bash
python Upload_Google.py
```

Le script va scanner les dossiers, horodater les fichiers JSON, générer les fichiers de description et pousser le tout sur le serveur d'ingestion Google.

### 🛡️ Sécurité & Confidentialité
Ce repository contient une version anonymisée du code utilisé en production.

Les données sensibles (Clés SSH, Identifiants clients, Données réelles) sont exclues via .gitignore.

### 👤 Auteur
Sullyvan Descamps - Software Engineer & Backend Architect

Experts en intégrations API complexes et architectures de données.

### 👉 Engagez-moi sur Malt
[![Malt Profile](https://img.shields.io/badge/Disponible_sur-MALT-ff5c5c?style=for-the-badge&logo=malt)](https://www.malt.fr/profile/sullyvandescamps)
