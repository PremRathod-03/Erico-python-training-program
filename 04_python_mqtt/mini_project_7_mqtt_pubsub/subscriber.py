"""
Mini-Project 7 - Subscriber

Subscribes to `mini_project/messages` and displays each message as a formatted table row,
with a running count per device. Malformed messages are reported instead of crashing.

    python subscriber.py                 # until Ctrl+C
    python subscriber.py --duration 15
"""
import argparse
import json
import os
import time
import uuid
from collections import Counter

import paho.mqtt.client as mqtt

TOPIC = "mini_project/messages"
HEADER = f"{'#':>4}  {'time':<19}  {'device':<13} {'temp °C':>8} {'hum %':>6} {'batt':>5}  {'status':<11} note"


def format_row(msg: dict) -> str:
    warn = " ⚠" if msg.get("status") != "OK" or msg.get("battery", 100) < 20 else ""
    return (f"{msg['id']:>4}  {msg['timestamp']:<19}  {msg['device']:<13} {msg['temperature']:>8.2f} "
            f"{msg['humidity']:>6.1f} {msg['battery']:>4}%  {msg['status']:<11} {msg['note']}{warn}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default=os.environ.get("MQTT_HOST", "localhost"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("MQTT_PORT", 1883)))
    parser.add_argument("--duration", type=float, default=0)
    args = parser.parse_args()

    per_device: Counter = Counter()

    def on_connect(client, _u, _f, reason_code, _p):
        print(f"Subscriber connected to {args.host}:{args.port} ({reason_code}); waiting for messages on {TOPIC}\n")
        client.subscribe(TOPIC, qos=1)
        print(HEADER)
        print("-" * len(HEADER))

    def on_message(_c, _u, m):
        try:
            msg = json.loads(m.payload)
            print(format_row(msg))
            per_device[msg["device"]] += 1
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print(f"  (malformed message ignored: {m.payload[:60]!r})")

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"mp7-sub-{uuid.uuid4().hex[:6]}")
    client.on_connect, client.on_message = on_connect, on_message
    client.connect(args.host, args.port)

    try:
        if args.duration:
            client.loop_start()
            time.sleep(args.duration)
            client.loop_stop()
        else:
            client.loop_forever()
    except KeyboardInterrupt:
        pass
    client.disconnect()
    print(f"\nMessages per device: {dict(per_device)}")


if __name__ == "__main__":
    main()
