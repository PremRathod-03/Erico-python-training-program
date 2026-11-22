"""
Shared helpers for the MQTT module (paho-mqtt 2.x).

Broker settings come from environment variables so every script works against
a local Mosquitto (default) or any other broker:
    MQTT_HOST (default: localhost)   MQTT_PORT (default: 1883)
"""
import argparse
import os
import uuid

import paho.mqtt.client as mqtt

DEFAULT_HOST = os.environ.get("MQTT_HOST", "localhost")
DEFAULT_PORT = int(os.environ.get("MQTT_PORT", "1883"))


def make_client(prefix: str = "training") -> mqtt.Client:
    """Create a client using the paho-mqtt v2 callback API with a unique id."""
    client_id = f"{prefix}-{uuid.uuid4().hex[:6]}"
    return mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)


def base_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--host", default=DEFAULT_HOST, help="broker host (default: %(default)s)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="broker port (default: %(default)s)")
    return parser
