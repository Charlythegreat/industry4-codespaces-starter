"""API FastAPI pour la détection d'anomalies sur les capteurs industriels."""
import os
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta, timezone

import numpy as np
import psycopg
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Connexion PostgreSQL/TimescaleDB
PG_CONN = os.getenv(
    "PG_CONN",
    "host=localhost port=5432 dbname=i40 user=i40 password=i40pass"
)

app = FastAPI(title="I4.0 Anomaly API", version="0.1.0")


# --- Modèles Pydantic ---
class PredictRequest(BaseModel):
    """Requête de prédiction d'anomalie."""
    machine_id: str = Field(..., description="Identifiant machine (ex: M01)")
    window_minutes: int = Field(
        15, ge=1, le=240, description="Fenêtre d'historique en minutes")
    sensors: Optional[List[str]] = Field(
        None, description="Liste de capteurs à considérer (par défaut: tous)")


class PredictResponse(BaseModel):
    """Réponse avec statistiques et score d'anomalie."""
    machine_id: str
    window_minutes: int
    n_points: int
    per_sensor: Dict[str, Dict[str, Any]]
    anomaly_score: float
    thresholds: Dict[str, float] = Field(
        default_factory=lambda: {"z_abs": 3.0})


# --- Endpoints ---
@app.get("/health")
def health():
    """Vérification de l'état de l'API."""
    return {"status": "ok", "ts": datetime.now(timezone.utc).isoformat()}


@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    """Analyse les données capteurs et détecte les anomalies (z-score > 3)."""
    since = datetime.now(timezone.utc) - timedelta(minutes=req.window_minutes)
    try:
        with psycopg.connect(PG_CONN) as conn:
            with conn.cursor() as cur:
                params = {"since": since, "machine_id": req.machine_id}
                sensor_filter = ""
                if req.sensors:
                    sensor_filter = "AND sensor = ANY(%(sensors)s)"
                    params["sensors"] = req.sensors

                cur.execute(
                    f"""
                    SELECT ts, sensor, value
                    FROM sensor_readings
                    WHERE machine_id = %(machine_id)s
                      AND ts >= %(since)s
                      {sensor_filter}
                    ORDER BY ts ASC
                    """,
                    params
                )
                rows = cur.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB error: {e}")

    if not rows:
        raise HTTPException(
            status_code=404, detail="Aucune donnée sur la fenêtre spécifiée")

    by_sensor: Dict[str, List[float]] = {}
    latest_by_sensor: Dict[str, float] = {}
    for ts, sensor, value in rows:
        by_sensor.setdefault(sensor, []).append(float(value))
        latest_by_sensor[sensor] = float(value)

    # Calcul des statistiques par capteur
    per_sensor_out: Dict[str, Dict[str, Any]] = {}
    anomalies = 0
    for sensor, values in by_sensor.items():
        arr = np.asarray(values, dtype=float)
        mu = float(np.mean(arr))      # Moyenne
        sigma = float(np.std(arr)) if len(arr) > 1 else 0.0  # Écart-type
        latest = latest_by_sensor[sensor]
        z = (latest - mu) / sigma if sigma > 1e-9 else 0.0   # Z-score
        is_anom = abs(z) >= 3.0       # Anomalie si |z| >= 3
        per_sensor_out[sensor] = {
            "latest": latest,
            "mean": mu,
            "std": sigma,
            "z_score_abs": abs(z),
            "is_anomaly": is_anom,
        }
        if is_anom:
            anomalies += 1

    anomaly_score = anomalies / max(len(by_sensor), 1)

    return PredictResponse(
        machine_id=req.machine_id,
        window_minutes=req.window_minutes,
        n_points=len(rows),
        per_sensor=per_sensor_out,
        anomaly_score=float(anomaly_score),
    )
