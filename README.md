# Industry 4.0 Starter (Codespaces)

Pipeline démo IoT (MQTT) → TimeSeries (TimescaleDB) → Dashboards (Grafana) → API ML (FastAPI).

## Démarrage rapide

1. Crée un Codespace sur ce repo (bouton Code → Create codespace).
2. Attends l'initialisation (Docker compose démarre Mosquitto, TimescaleDB, Grafana).
3. Lance la simulation et l’ingestion:
   ```bash
   python -m src.simulate.producer
   ```
   ```bash
   python -m src.ingest.mqtt_to_postgres
   ```
4. Lance l’API FastAPI:
   ```bash
   uvicorn src.api.app:app --reload --host 0.0.0.0 --port 8000
   ```
   - Health: `GET /8000/health`
   - Prédiction: `POST /8000/predict` avec:
     ```json
     { "machine_id": "M01", "window_minutes": 15 }
     ```
5. Ouvre Grafana (port 3000, `admin/admin`):
   - Datasource Postgres et dashboard “I4.0 - Sensors Overview” sont auto‑provisionnés.

## Notes
- Si Docker est restreint sur Codespaces org, bascule sur services managés (Timescale Cloud, Mosquitto/Aiven).
- Secrets: configure `PG_CONN` si tu veux pointer vers une DB externe.
- Sécurité: Mosquitto en anonyme pour démo → protège en prod (utilisateurs/ACL/TLS).
