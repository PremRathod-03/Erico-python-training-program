"""
Exercise 41 (part 1): one script that publishes to test/topic with different QoS levels
and subscribes to the same topic, logging every received message.
"""
import logging
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

LOG_FILE = Path(__file__).resolve().parent / "qos_messages.log"
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s",
                    handlers=[logging.StreamHandler(), logging.FileHandler(LOG_FILE, mode="w")])
log = logging.getLogger("qos-pub-sub")
TOPIC = "test/topic"


def run(host: str, port: int, per_level: int = 2) -> list[tuple[int, str]]:
    expected = per_level * 3
    received: list[tuple[int, str]] = []
    all_done = threading.Event()
    subscribed = threading.Event()

    def on_message(_c, _u, msg):
        received.append((msg.qos, msg.payload.decode()))
        log.info("RECEIVED qos=%d topic=%s payload=%s", msg.qos, msg.topic, msg.payload.decode())
        if len(received) >= expected:
            all_done.set()

    sub = make_client("ex41-sub")
    sub.on_message = on_message
    sub.on_subscribe = lambda *_: subscribed.set()
    sub.connect(host, port)
    sub.subscribe(TOPIC, qos=2)
    sub.loop_start()
    subscribed.wait(5)

    pub = make_client("ex41-pub")
    pub.connect(host, port)
    pub.loop_start()
    for qos in (0, 1, 2):
        for i in range(1, per_level + 1):
            payload = f"QoS{qos} message {i}"
            pub.publish(TOPIC, payload, qos=qos).wait_for_publish(timeout=5)
            log.info("SENT     qos=%d payload=%s", qos, payload)

    all_done.wait(5)
    time.sleep(0.2)
    for c in (pub, sub):
        c.loop_stop()
        c.disconnect()
    return received


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--per-level", type=int, default=2)
    args = parser.parse_args()
    got = run(args.host, args.port, args.per_level)
    print(f"\nReceived {len(got)} messages; log saved to {LOG_FILE.name}")


if __name__ == "__main__":
    main()
