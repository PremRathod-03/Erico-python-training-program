"""
Exercise 34: connect to a broker, publish to a topic and subscribe to the same topic
to see the message (also visible in MQTT Explorer).
"""
import json
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402


def round_trip(host: str, port: int, topic: str, payload: str, timeout: float = 5) -> str | None:
    received = threading.Event()
    result: dict = {}

    def on_connect(client, _userdata, _flags, reason_code, _props):
        print(f"Connected to {host}:{port} ({reason_code})")
        client.subscribe(topic, qos=1)

    def on_subscribe(client, _userdata, _mid, _codes, _props):
        print(f"Subscribed to {topic}, publishing...")
        client.publish(topic, payload, qos=1)

    def on_message(_client, _userdata, msg):
        result["payload"] = msg.payload.decode()
        print(f"Received on {msg.topic}: {result['payload']}")
        received.set()

    client = make_client("explorer")
    client.on_connect, client.on_subscribe, client.on_message = on_connect, on_subscribe, on_message
    client.connect(host, port)
    client.loop_start()
    received.wait(timeout)
    client.loop_stop()
    client.disconnect()
    return result.get("payload")


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--topic", default="test/explorer")
    args = parser.parse_args()
    message = json.dumps({"source": "python", "text": "Hello from Python", "ts": time.time()})
    if round_trip(args.host, args.port, args.topic, message) is None:
        print("No message received - is the broker running?")


if __name__ == "__main__":
    main()
