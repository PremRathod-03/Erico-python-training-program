"""
Exercise 36: Creating an MQTT Subscriber

- subscribes to test/topic and prints received messages
- handles multiple topics with a wildcard (sensors/#) and logs the data to logs/subscriber.log

Run:  python subscriber.py            (Ctrl+C to stop)
      python subscriber.py --duration 10
"""
import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)
logging.basicConfig(filename=LOG_DIR / "subscriber.log", level=logging.INFO,
                    format="%(asctime)s | %(message)s")
log = logging.getLogger("subscriber")

SUBSCRIPTIONS = [("test/topic", 1), ("sensors/#", 1)]


def on_message(_client, _userdata, msg):
    text = msg.payload.decode(errors="replace")
    if msg.topic == "test/topic":
        print(f"[test/topic] {text}")
        return
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        data = text
    print(f"[{msg.topic}] {data}")
    log.info("%s %s", msg.topic, text)


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--duration", type=float, default=0, help="seconds to run (0 = until Ctrl+C)")
    args = parser.parse_args()

    client = make_client("subscriber")
    client.on_message = on_message
    client.connect(args.host, args.port)
    client.subscribe(SUBSCRIPTIONS)
    print(f"Subscribed to {[t for t, _ in SUBSCRIPTIONS]} on {args.host}:{args.port}")

    if args.duration:
        client.loop_start()
        time.sleep(args.duration)
        client.loop_stop()
    else:
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nStopping subscriber")
    client.disconnect()


if __name__ == "__main__":
    main()
