"""
Exercise 33: MQTT Topics and Messages - smart-home topic structure + wildcards

python topics.py --offline   # only the wildcard-matching table (no broker needed)
python topics.py             # also publishes to every topic and shows which wildcard subscriptions receive them
"""
import sys
import time
from pathlib import Path

from paho.mqtt.client import topic_matches_sub

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

TOPICS = {
    "home/living-room/temperature": "24.5",
    "home/living-room/humidity": "48",
    "home/living-room/light/state": "ON",
    "home/kitchen/temperature": "27.1",
    "home/kitchen/smoke": "false",
    "home/bedroom/temperature": "22.8",
    "home/bedroom/light/state": "OFF",
    "home/garage/door/state": "closed",
}
SUBSCRIPTIONS = ["home/+/temperature", "home/+/light/state", "home/kitchen/#", "home/#"]


def matching_table() -> dict[str, list[str]]:
    return {sub: [t for t in TOPICS if topic_matches_sub(sub, t)] for sub in SUBSCRIPTIONS}


def live_demo(host: str, port: int) -> dict[str, list[str]]:
    received: dict[str, list[str]] = {s: [] for s in SUBSCRIPTIONS[:2] + ["home/kitchen/#"]}

    def on_message(_client, _userdata, msg):
        for sub in received:
            if topic_matches_sub(sub, msg.topic):
                received[sub].append(f"{msg.topic}={msg.payload.decode()}")

    sub = make_client("topics-sub")
    sub.on_message = on_message
    sub.connect(host, port)
    for s in received:
        sub.subscribe(s, qos=1)
    sub.loop_start()
    time.sleep(0.5)

    pub = make_client("topics-pub")
    pub.connect(host, port)
    pub.loop_start()
    for topic, value in TOPICS.items():
        pub.publish(topic, value, qos=1).wait_for_publish()
    time.sleep(1)
    for c in (pub, sub):
        c.loop_stop()
        c.disconnect()
    return received


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--offline", action="store_true", help="skip the live broker demo")
    args = parser.parse_args()

    print("Wildcard matching (paho topic_matches_sub):")
    for sub, topics in matching_table().items():
        print(f"  {sub:<20} -> {len(topics)} topics: {topics}")

    if not args.offline:
        print(f"\nLive demo on {args.host}:{args.port}")
        for sub, msgs in live_demo(args.host, args.port).items():
            print(f"  {sub:<20} received {msgs}")


if __name__ == "__main__":
    main()
