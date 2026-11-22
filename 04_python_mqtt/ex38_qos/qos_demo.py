"""
Exercise 38: Managing QoS Levels in MQTT

Publishes one message at each QoS level and prints the packet exchange
(paho's on_log shows every packet sent/received):

  QoS 0  PUBLISH ->                                   (fire and forget, no acknowledgement)
  QoS 1  PUBLISH ->  <- PUBACK                        (at least once, acknowledged)
  QoS 2  PUBLISH ->  <- PUBREC  PUBREL ->  <- PUBCOMP (exactly once, two-step handshake)

A subscriber on the same topic confirms delivery of each message.
"""
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

TOPIC = "test/qos"
PACKETS = ("PUBLISH", "PUBACK", "PUBREC", "PUBREL", "PUBCOMP")


def run_demo(host: str, port: int) -> dict[int, list[str]]:
    trace: dict[int, list[str]] = {0: [], 1: [], 2: []}
    current = {"qos": None}
    delivered: dict[int, threading.Event] = {q: threading.Event() for q in trace}

    def on_log(_client, _userdata, _level, buf):
        packet = next((p for p in PACKETS if p in buf), None)
        if packet and current["qos"] is not None:
            direction = "->" if buf.startswith("Sending") else "<-"
            trace[current["qos"]].append(f"{direction} {packet}")

    def on_publish(_client, _userdata, mid, reason_code, _props):
        print(f"   on_publish: mid={mid} complete ({reason_code})")

    def on_message(_client, _userdata, msg):
        print(f"   subscriber received QoS {msg.qos} message: {msg.payload.decode()}")
        delivered[int(msg.payload.decode().split()[1])].set()

    sub = make_client("qos-sub")
    sub.on_message = on_message
    sub.connect(host, port)
    sub.subscribe(TOPIC, qos=2)          # subscription QoS caps the delivery QoS
    sub.loop_start()
    time.sleep(0.5)

    pub = make_client("qos-pub")
    pub.on_log = on_log
    pub.on_publish = on_publish
    pub.connect(host, port)
    pub.loop_start()
    time.sleep(0.3)

    for qos in (0, 1, 2):
        print(f"\nQoS {qos}:")
        current["qos"] = qos
        info = pub.publish(TOPIC, f"QoS {qos} message", qos=qos)
        info.wait_for_publish(timeout=5)
        delivered[qos].wait(timeout=5)
        time.sleep(0.3)
        current["qos"] = None
        print("   packet flow:", "  ".join(trace[qos]))

    for c in (pub, sub):
        c.loop_stop()
        c.disconnect()
    return trace


def main() -> None:
    args = base_parser(__doc__).parse_args()
    run_demo(args.host, args.port)
    print("\nSummary: QoS 0 = no ack | QoS 1 = PUBACK | QoS 2 = PUBREC/PUBREL/PUBCOMP handshake")


if __name__ == "__main__":
    main()
