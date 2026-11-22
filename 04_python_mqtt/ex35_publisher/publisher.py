"""
Exercise 35: Creating an MQTT Publisher

Publishes:
  - a text message to            test/topic
  - a JSON payload to            sensors/temperature   e.g. {"sensor": "temperature", "value": 25}

Run a subscriber first to see them, e.g.:  mosquitto_sub -t 'test/topic' -t 'sensors/#' -v
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402


def publish_messages(host: str, port: int) -> list[tuple[str, str]]:
    client = make_client("publisher")
    client.connect(host, port, keepalive=60)
    client.loop_start()

    sent = []
    text_topic, text = "test/topic", "Hello from the Python publisher!"
    client.publish(text_topic, text, qos=1).wait_for_publish()
    sent.append((text_topic, text))

    json_topic = "sensors/temperature"
    payload = json.dumps({"sensor": "temperature", "value": 25})
    client.publish(json_topic, payload, qos=1).wait_for_publish()
    sent.append((json_topic, payload))

    client.loop_stop()
    client.disconnect()
    return sent


def main() -> None:
    args = base_parser(__doc__).parse_args()
    for topic, payload in publish_messages(args.host, args.port):
        print(f"Published to {topic}: {payload}")


if __name__ == "__main__":
    main()
