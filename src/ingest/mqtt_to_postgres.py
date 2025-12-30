"""Service d'ingestion - Consomme les messages MQTT et les stocke dans TimescaleDB."""
import os
import json
import psycopg
from psycopg.rows import dict_row
import paho.mqtt.client as mqtt

# Configuration via variables d'environnement
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "factory/lineA/sensors")

PG_CONN = os.getenv(
    "PG_CONN",
    "host=localhost port=5432 dbname=i40 user=i40 password=i40pass"
)


def upsert_reading(conn, reading):
    """Insère ou met à jour une lecture capteur dans la DB."""
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO sensor_readings (ts, machine_id, sensor, value, unit)
            VALUES (%(ts)s, %(machine_id)s, %(sensor)s, %(value)s, %(unit)s)
            ON CONFLICT (ts, machine_id, sensor) DO UPDATE
            SET value = EXCLUDED.value, unit = EXCLUDED.unit
            """,
            reading
        )


def on_message(conn):
    """Factory pour le callback de réception MQTT."""
    def _handler(client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode("utf-8"))
            upsert_reading(conn, data)
        except Exception as e:
            print(f"Ingest error: {e}")
    return _handler


def main():
    """Connexion DB + MQTT et écoute continue des messages."""
    with psycopg.connect(PG_CONN) as conn:
        conn.autocommit = True
        client = mqtt.Client()
        client.on_message = on_message(conn)
        client.connect(MQTT_HOST, MQTT_PORT, keepalive=30)
        client.subscribe(MQTT_TOPIC, qos=0)
        print(f"Listening MQTT {MQTT_HOST}:{MQTT_PORT} topic '{MQTT_TOPIC}'")
        client.loop_forever()


if __name__ == "__main__":
    main()
