"""
Exercise 37: Handling MQTT Callbacks

The subscriber now:
  - prints a message when connected            (on_connect)
  - logs topic and payload of received messages (on_message)
  - handles subscription acknowledgements       (on_subscribe)
  - also reports disconnects                    (on_disconnect)

paho-mqtt 2.x callback signatures (CallbackAPIVersion.VERSION2) are used.
"""
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger("callbacks")

TOPICS = [("test/topic", 0), ("sensors/#", 1)]


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        log.error("Connection failed: %s", reason_code)
        return
    log.info("Connected to broker (session present=%s)", flags.session_present)
    # subscribing inside on_connect means subscriptions are restored after a reconnect
    result, mid = client.subscribe(TOPICS)
    userdata["pending"][mid] = [t for t, _ in TOPICS]


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    topics = userdata["pending"].pop(mid, [])
    for topic, rc in zip(topics, reason_code_list):
        if rc.is_failure:
            log.error("Subscription to %s rejected: %s", topic, rc)
        else:
            log.info("Subscription acknowledged: %s (granted QoS %s)", topic, rc.value)


def on_message(client, userdata, msg):
    userdata["count"] += 1
    log.info("Message #%d | topic=%s | qos=%d | payload=%s",
             userdata["count"], msg.topic, msg.qos, msg.payload.decode(errors="replace"))


def on_disconnect(client, userdata, flags, reason_code, properties):
    log.info("Disconnected (%s)", reason_code)


def build_client():
    client = make_client("callbacks")
    client.user_data_set({"pending": {}, "count": 0})
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    return client


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--duration", type=float, default=0, help="seconds to run (0 = until Ctrl+C)")
    args = parser.parse_args()

    client = build_client()
    client.connect(args.host, args.port)
    if args.duration:
        client.loop_start()
        time.sleep(args.duration)
        client.disconnect()
        client.loop_stop()
    else:
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            client.disconnect()


if __name__ == "__main__":
    main()
