# 🏭 Industry 4.0 IoT Pipeline Starter

[![GitHub Codespaces](https://img.shields.io/badge/GitHub-Codespaces-blue?logo=github)](https://github.com/features/codespaces)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-green?logo=fastapi)](https://fastapi.tiangolo.com)
[![TimescaleDB](https://img.shields.io/badge/TimescaleDB-Latest-orange?logo=postgresql)](https://timescale.com)
[![Grafana](https://img.shields.io/badge/Grafana-11.0-orange?logo=grafana)](https://grafana.com)

Pipeline complet de démonstration **IoT industriel** : de la collecte de données capteurs jusqu'à la visualisation en temps réel et l'API de prédiction d'anomalies.

---

## 📋 Table des matières

- [Présentation du projet](#-présentation-du-projet)
- [Pourquoi ce projet ?](#-pourquoi-ce-projet-)
- [Architecture technique](#-architecture-technique)
- [Technologies utilisées](#-technologies-utilisées)
- [Démarrage rapide](#-démarrage-rapide)
- [Accès aux services](#-accès-aux-services)
- [Structure du projet](#-structure-du-projet)
- [API Reference](#-api-reference)
- [Dashboard Grafana](#-dashboard-grafana)
- [Importance du projet](#-importance-du-projet)
- [Évolutions futures](#-évolutions-futures)
- [Contribuer](#-contribuer)
- [Licence](#-licence)

---

## 🎯 Présentation du projet

Ce projet est un **starter kit Industry 4.0** conçu pour démontrer une architecture IoT moderne de bout en bout. Il simule un environnement industriel avec des machines équipées de capteurs (température, vibration) et permet de :

- **Collecter** les données via protocole MQTT
- **Stocker** les séries temporelles dans TimescaleDB
- **Visualiser** en temps réel avec Grafana
- **Analyser** et détecter les anomalies via une API FastAPI

---

## 💡 Pourquoi ce projet ?

### Le contexte Industry 4.0

L'**Industrie 4.0** représente la quatrième révolution industrielle, caractérisée par :
- L'interconnexion des machines (IIoT - Industrial Internet of Things)
- L'analyse de données en temps réel
- La maintenance prédictive
- L'automatisation intelligente

### Les défis adressés

| Défi industriel | Solution apportée |
|-----------------|-------------------|
| Pannes imprévues coûteuses | Détection d'anomalies en temps réel |
| Données dispersées | Pipeline de données centralisé |
| Manque de visibilité | Dashboard temps réel |
| Temps de réaction lent | Alertes et API instantanées |

### Cas d'usage typiques

- 🔧 **Maintenance prédictive** : Anticiper les pannes avant qu'elles ne surviennent
- 📊 **Monitoring de production** : Suivre les KPIs en temps réel
- ⚠️ **Détection d'anomalies** : Identifier les comportements anormaux des machines
- 📈 **Optimisation énergétique** : Analyser la consommation et optimiser

---

## 🏗 Architecture technique

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         GitHub Codespaces                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐  │
│  │   Producer   │───▶│   Mosquitto  │───▶│   MQTT to PostgreSQL     │  │
│  │  (Simulator) │    │ (MQTT Broker)│    │      (Ingestion)         │  │
│  │   :Python    │    │    :1883     │    │       :Python            │  │
│  └──────────────┘    └──────────────┘    └───────────┬──────────────┘  │
│                                                       │                  │
│                                                       ▼                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────────────┐  │
│  │   FastAPI    │◀───│   Grafana    │◀───│     TimescaleDB          │  │
│  │  (REST API)  │    │ (Dashboard)  │    │   (Time-Series DB)       │  │
│  │    :8000     │    │    :3000     │    │       :5432              │  │
│  └──────────────┘    └──────────────┘    └──────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### Flux de données

1. **Simulation** → Le producer génère des données de capteurs (température, vibration) pour 3 machines
2. **Transport** → Les données sont publiées sur le broker MQTT Mosquitto
3. **Ingestion** → Le service d'ingestion consomme les messages et les stocke dans TimescaleDB
4. **Stockage** → TimescaleDB optimise le stockage et les requêtes sur les séries temporelles
5. **Visualisation** → Grafana affiche les données en temps réel
6. **Analyse** → L'API FastAPI permet de requêter et analyser les données

---

## 🛠 Technologies utilisées

### Pourquoi MQTT ?

**MQTT (Message Queuing Telemetry Transport)** est le protocole de référence pour l'IoT industriel :

| Avantage | Description |
|----------|-------------|
| **Léger** | Overhead minimal, idéal pour les capteurs à ressources limitées |
| **Fiable** | QoS configurable (0, 1, 2) pour garantir la livraison |
| **Scalable** | Architecture pub/sub permettant des millions de connexions |
| **Standard** | Protocole ouvert adopté par l'industrie (OASIS) |

### Pourquoi TimescaleDB ?

**TimescaleDB** est une extension PostgreSQL optimisée pour les séries temporelles :

| Avantage | Description |
|----------|-------------|
| **Performance** | Requêtes 10-100x plus rapides que PostgreSQL standard |
| **Compression** | Réduction de 90%+ de l'espace de stockage |
| **SQL natif** | Pas de nouvelle syntaxe à apprendre |
| **Hypertables** | Partitionnement automatique par temps |
| **Rétention** | Politiques de suppression automatique des anciennes données |

### Pourquoi Grafana ?

**Grafana** est la plateforme de visualisation leader pour le monitoring :

| Avantage | Description |
|----------|-------------|
| **Temps réel** | Rafraîchissement automatique des données |
| **Alertes** | Notifications configurables (email, Slack, etc.) |
| **Extensible** | +150 datasources supportées |
| **Open Source** | Communauté active et gratuit |

### Pourquoi FastAPI ?

**FastAPI** est le framework Python moderne pour les APIs :

| Avantage | Description |
|----------|-------------|
| **Performance** | Aussi rapide que Node.js et Go |
| **Typage** | Validation automatique avec Pydantic |
| **Documentation** | Swagger/OpenAPI généré automatiquement |
| **Async** | Support natif de l'asynchrone |

---

## 🚀 Démarrage rapide

### Prérequis

- Compte GitHub avec accès à Codespaces
- Navigateur web moderne

### Étape 1 : Lancer le Codespace

1. Cliquez sur le bouton **Code** → **Codespaces** → **Create codespace on main**
2. Attendez l'initialisation (~2-3 minutes)

### Étape 2 : Démarrer les services Docker

```bash
docker compose up -d
```

Vérifiez que tous les services sont en cours d'exécution :

```bash
docker compose ps
```

Résultat attendu :
```
NAME                                         STATUS
industry4-codespaces-starter-grafana-1       Up
industry4-codespaces-starter-mosquitto-1     Up
industry4-codespaces-starter-timescaledb-1   Up
```

### Étape 3 : Lancer la simulation

Dans un premier terminal, démarrez le simulateur de capteurs :

```bash
python -m src.simulate.producer
```

Dans un second terminal, démarrez l'ingestion des données :

```bash
python -m src.ingest.mqtt_to_postgres
```

### Étape 4 : Lancer l'API (optionnel)

```bash
uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
```

### Étape 5 : Vérifier les données

```bash
docker exec industry4-codespaces-starter-timescaledb-1 \
  psql -U i40 -d i40 -c "SELECT COUNT(*) FROM sensor_readings;"
```

> **NB** : Pour arrêter les services, et pour supprimer également les données saisissez la commande suivante dans le bash:
```bash
pkill -f uvicorn 2>/dev/null; pkill -f "python -m src" 2>/dev/null; docker compose down; echo "Tous les services arrêtés".
```

---

## 🌐 Accès aux services

| Service | Port | URL Codespaces | Credentials |
|---------|------|----------------|-------------|
| **Grafana** | 3000 | `https://<codespace>-3000.app.github.dev` | `admin` / `admin` |
| **FastAPI** | 8000 | `https://<codespace>-8000.app.github.dev` | - |
| **API Docs** | 8000 | `https://<codespace>-8000.app.github.dev/docs` | - |
| **MQTT** | 1883 | localhost:1883 | Anonymous |
| **PostgreSQL** | 5432 | localhost:5432 | `i40` / `i40pass` |

> 💡 **Astuce** : Cliquez sur l'onglet **PORTS** en bas de VS Code pour accéder directement aux URLs.

---

## 📁 Structure du projet

```
industry4-codespaces-starter/
├── .devcontainer/
│   └── devcontainer.json      # Configuration Codespaces + Docker
├── db/
│   └── init.sql               # Script d'initialisation TimescaleDB
├── grafana/
│   ├── dashboards/
│   │   └── sensors_timeseries.json  # Dashboard pré-configuré
│   └── provisioning/
│       ├── dashboards/
│       │   └── provider.yml   # Auto-provisioning dashboards
│       └── datasources/
│           └── datasource.yml # Connexion TimescaleDB
├── mosquitto/
│   ├── mosquitto.conf         # Configuration du broker MQTT
│   ├── data/                  # Données persistantes
│   └── log/                   # Logs du broker
├── src/
│   ├── api/
│   │   └── app.py             # API FastAPI (health + predict)
│   ├── ingest/
│   │   └── mqtt_to_postgres.py # Consumer MQTT → TimescaleDB
│   └── simulate/
│       └── producer.py        # Simulateur de capteurs
├── docker-compose.yml         # Orchestration des services
├── requirements.txt           # Dépendances Python
└── README.md                  # Ce fichier
```

---

## 📖 API Reference

### Health Check

```http
GET /health
```

**Réponse :**
```json
{
  "status": "ok",
  "ts": "2025-12-30T15:00:00.000000+00:00"
}
```

### Prédiction d'anomalies

```http
POST /predict
Content-Type: application/json

{
  "machine_id": "M01",
  "window_minutes": 15,
  "sensors": ["temp", "vibration", "pressure"]
}
```

**Réponse :**
```json
{
  "machine_id": "M01",
  "window_minutes": 15,
  "n_points": 150,
  "per_sensor": {
    "temp": {"mean": 80.5, "std": 2.1, "min": 75.2, "max": 86.8},
    "vibration": {"mean": 2.5, "std": 0.3, "min": 1.9, "max": 3.2},
    "pressure": {"mean": 4.0, "std": 0.5, "min": 2.1, "max": 5.8}
  },
  "anomaly_score": 0.12,
  "thresholds": {"z_abs": 3.0}
}
```

---

## 📊 Dashboard Grafana

### Accéder au dashboard

1. Ouvrez Grafana via le port **3000** (onglet PORTS de VS Code)
2. Connectez-vous avec `admin` / `admin`
3. Allez dans **Dashboards** → **I4.0 - Sensors Overview**

### Fonctionnalités du dashboard

- **Graphique temps réel** : Visualisation des valeurs de capteurs par machine
- **Filtres** : Sélection par machine et type de capteur
- **Rafraîchissement** : Mise à jour automatique toutes les 5 secondes
- **Plage temporelle** : Configurable (dernière heure, jour, semaine...)

### Capteurs simulés

| Capteur | Unité | Plage normale | Description |
|---------|-------|---------------|-------------|
| `temp` | °C | 60-90 | Température machine |
| `vibration` | mm/s | 0.1-5 | Vibration du moteur |
| `pressure` | bar | 2-6 | Pression hydraulique |

### Machines simulées

- **M01** : Machine de production principale
- **M02** : Machine secondaire
- **M03** : Machine auxiliaire

---

## 🏆 Importance du projet

### Valeur business

1. **Réduction des coûts de maintenance** : -25 à -30% grâce à la maintenance prédictive
2. **Diminution des temps d'arrêt** : Détection précoce des anomalies
3. **Optimisation des ressources** : Meilleure planification des interventions
4. **Amélioration de la qualité** : Corrélation entre paramètres machine et qualité produit

### Valeur technique

1. **Architecture moderne** : Stack reproductible et scalable
2. **Best practices** : Séparation des responsabilités, conteneurisation
3. **Documentation** : Code commenté et README détaillé
4. **Extensibilité** : Facile à adapter à d'autres cas d'usage

### Valeur pédagogique

1. **Apprentissage IoT** : Comprendre le flux de données industriel
2. **Pratique DevOps** : Docker, CI/CD, observabilité
3. **Data Engineering** : Pipeline de données temps réel
4. **Machine Learning** : Base pour implémenter des modèles prédictifs

---

## 🔮 Évolutions futures

### Court terme (v1.1)

- [ ] **Alertes Grafana** : Notifications en cas de dépassement de seuils
- [ ] **Plus de capteurs** : Pression, courant, vitesse
- [ ] **Authentification MQTT** : Sécurisation du broker
- [ ] **Tests unitaires** : Couverture de code

### Moyen terme (v2.0)

- [ ] **Machine Learning** : Modèles de détection d'anomalies (Isolation Forest, LSTM)
- [ ] **Edge Computing** : Traitement local avant envoi cloud
- [ ] **Multi-sites** : Gestion de plusieurs usines
- [ ] **Intégration ERP** : Connexion avec SAP, Oracle...

### Long terme (v3.0)

- [ ] **Digital Twin** : Représentation virtuelle des machines
- [ ] **IA générative** : Chatbot pour analyser les données
- [ ] **Réalité augmentée** : Visualisation overlay sur les machines
- [ ] **Blockchain** : Traçabilité et certification des données

---

## 🔒 Sécurité

### Environnement de démonstration

⚠️ **Ce projet est configuré pour la démonstration et l'apprentissage.** Pour un déploiement en production :

| Composant | Configuration démo | Production recommandée |
|-----------|-------------------|------------------------|
| MQTT | Anonymous | TLS + Authentification |
| PostgreSQL | Password simple | Secrets management |
| Grafana | admin/admin | SSO/LDAP |
| API | Pas d'auth | OAuth2/JWT |

### Recommandations

1. Changez tous les mots de passe par défaut
2. Activez TLS sur tous les endpoints
3. Utilisez des secrets managers (Vault, AWS Secrets Manager)
4. Implémentez le principe du moindre privilège
5. Activez les logs d'audit

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment participer :

1. **Fork** le repository
2. Créez une **branche** (`git checkout -b feature/ma-fonctionnalite`)
3. **Committez** vos changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrez une **Pull Request**

### Guidelines

- Suivez le style de code existant (Black, isort)
- Ajoutez des tests pour les nouvelles fonctionnalités
- Mettez à jour la documentation si nécessaire
- Décrivez clairement vos changements dans la PR

---

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- [TimescaleDB](https://timescale.com) pour leur excellente base de données time-series
- [Eclipse Mosquitto](https://mosquitto.org) pour le broker MQTT
- [Grafana Labs](https://grafana.com) pour la plateforme de visualisation
- [FastAPI](https://fastapi.tiangolo.com) pour le framework API Python
- La communauté open source pour tous les outils utilisés

---

<div align="center">

**⭐ Si ce projet vous a été utile, n'hésitez pas à lui donner une étoile !**

Made with ❤️ for Industry 4.0

</div>
