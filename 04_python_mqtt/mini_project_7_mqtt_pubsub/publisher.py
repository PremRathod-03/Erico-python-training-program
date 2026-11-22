"""
Mini-Project 7 - Publisher

Publishes random message data with paho-mqtt to topic `mini_project/messages`.
Each message is JSON: id, device, random metrics, a random status text and a timestamp.

    python publisher.py                       # every 1 s until Ctrl+C
    python publisher.py --count 10 --interval 0.5
Run subscriber.py in another terminal to display the messages.
"""
import argparse
import json
import os
import random
import time
import uuid
from datetime import datetime

import paho.mqtt.client as mqtt

TOPIC = "mini_project/messages"
DEVICES = ["sensor-alpha", "sensor-beta", "sensor-gamma"]
STATUSES = ["OK", "OK", "OK", "WARN", "MAINTENANCE"]
WORDS = ["temperature stable", "door opened", "motion detected", "battery check", "heartbeat"]


def random_message(seq: int, rng: random.Random = random) -> dict:
    return {
        "id": seq,
        "device": rng.choice(DEVICES),
        "temperature": round(rng.uniform(18, 35), 2),
        "humidity": round(rng.uniform(30, 80), 1),
        "battery": rng.randint(5, 100),
        "status": rng.choice(STATUSES),
        "note": rng.choice(WORDS),
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default=os.environ.get("MQTT_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("MQTT_PORT", 1883)))
    parser.add_argument("--count", type=int, default=0, help="messages to send (0 = until Ctrl+C)")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--qos", type=int, choices=[0, 1, 2], default=1)
    args = parser.parse_args()

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"mp7-pub-{uuid.uuid4().hex[:6]}")
    client.on_connect = lambda c, u, f, rc, p: print(f"Publisher connected to {args.host}:{args.port} ({rc})")
    client.connect(args.host, args.port)
    client.loop_start()

    seq = 0
    try:
        while args.count == 0 or seq < args.count:
            seq += 1
            msg = random_message(seq)
            result = client.publish(TOPIC, json.dumps(msg), qos=args.qos)
            result.wait_for_publish()
            print(f"→ #{seq} {msg['device']}: {msg['temperature']}°C, {msg['humidity']}%, "
                  f"battery {msg['battery']}%, {msg['status']}")
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nPublisher stopped")
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
