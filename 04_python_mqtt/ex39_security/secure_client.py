"""
Exercise 39: test the secured broker with the correct credentials over TLS.

Credentials are read from environment variables (never hard-code them):
    export MQTT_USER=iotuser
    export MQTT_PASSWORD=...           # the password set with create_password_file.sh
    python secure_client.py            # TLS on port 8883 using certs/ca.crt
    python secure_client.py --wrong    # shows the broker rejecting bad credentials
"""
import os
import ssl
import sys
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

CA_CERT = Path(__file__).resolve().parent / "certs" / "ca.crt"


def secure_round_trip(host: str, port: int, username: str, password: str, timeout: float = 5) -> bool:
    done = threading.Event()
    state = {"ok": False}

    def on_connect(client, _u, _f, reason_code, _p):
        if reason_code.is_failure:
            print(f"Connection refused: {reason_code}")
            done.set()
            return
        print(f"Authenticated and connected over TLS to {host}:{port}")
        client.subscribe("secure/test", qos=1)
        client.publish("secure/test", "encrypted hello", qos=1)

    def on_message(_c, _u, msg):
        print(f"Received over TLS on {msg.topic}: {msg.payload.decode()}")
        state["ok"] = True
        done.set()

    client = make_client("secure")
    client.username_pw_set(username, password)
    client.tls_set(ca_certs=str(CA_CERT), tls_version=ssl.PROTOCOL_TLS_CLIENT)
    client.on_connect, client.on_message = on_connect, on_message
    client.connect(host, port)
    client.loop_start()
    done.wait(timeout)
    client.loop_stop()
    client.disconnect()
    return state["ok"]


def main() -> None:
    parser = base_parser(__doc__)
    parser.set_defaults(port=8883)
    parser.add_argument("--wrong", action="store_true", help="use a wrong password on purpose")
    args = parser.parse_args()

    if not CA_CERT.exists():
        sys.exit("certs/ca.crt not found - run ./generate_certs.sh first")
    user = os.environ.get("MQTT_USER", "iotuser")
    password = "definitely-wrong" if args.wrong else os.environ.get("MQTT_PASSWORD", "")
    ok = secure_round_trip(args.host, args.port, user, password)
    print("Secure round trip:", "SUCCESS" if ok else "FAILED")


if __name__ == "__main__":
    main()
