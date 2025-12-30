import time
import random
import json
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "factory/lineA/sensors"

MACHINES = ["M01", "M02", "M03"]
SENSORS = [
    ("temp", "C", 60, 90),
    ("vibration", "mm_s", 0.1, 5.0),
    ("pressure", "bar", 2.0, 6.0),
]

def make_reading():
    machine = random.choice(MACHINES)
    sensor, unit, lo, hi = random.choice(SENSORS)
    value = round(random.uniform(lo, hi), 3)
    return {
        "ts": datetime.now(timezone.utc).isoformat(),
        "machine_id": machine,
        "sensor": sensor,
        "value": value,
        "unit": unit
    }

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER_HOST, BROKER_PORT, keepalive=30)
    client.loop_start()
    try:
        while True:
            msg = make_reading()
            client.publish(TOPIC, json.dumps(msg), qos=0, retain=False)
            time.sleep(0.3)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
