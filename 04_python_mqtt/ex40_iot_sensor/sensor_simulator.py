"""
Exercise 40 (part 1): simulated IoT temperature sensor

Publishes a random-walk temperature reading as JSON to sensors/temperature every --interval seconds.
    python sensor_simulator.py                   # until Ctrl+C
    python sensor_simulator.py --count 10 --interval 0.5
"""
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

TOPIC = "sensors/temperature"


class TemperatureSensor:
    """Realistic readings: small random steps around a base value, clamped to a range."""

    def __init__(self, sensor_id: str = "temp-sensor-01", base: float = 25.0, seed: int | None = None):
        self.sensor_id = sensor_id
        self.value = base
        self.rng = random.Random(seed)

    def read(self) -> dict:
        self.value = min(max(self.value + self.rng.uniform(-0.6, 0.6), 15.0), 40.0)
        return {
            "sensor_id": self.sensor_id,
            "sensor": "temperature",
            "value": round(self.value, 2),
            "unit": "C",
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }


def run(host: str, port: int, count: int, interval: float) -> int:
    sensor = TemperatureSensor()
    client = make_client(sensor.sensor_id)
    # Last Will: the broker announces if the sensor disappears unexpectedly
    client.will_set("sensors/status/temp-sensor-01", "offline", qos=1, retain=True)
    client.connect(host, port)
    client.loop_start()
    client.publish("sensors/status/temp-sensor-01", "online", qos=1, retain=True)

    sent = 0
    try:
        while count == 0 or sent < count:
            reading = sensor.read()
            client.publish(TOPIC, json.dumps(reading), qos=1).wait_for_publish()
            sent += 1
            print(f"[{sent}] published {reading['value']} °C")
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        client.publish("sensors/status/temp-sensor-01", "offline", qos=1, retain=True).wait_for_publish()
        client.loop_stop()
        client.disconnect()
    return sent


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--count", type=int, default=0, help="number of readings (0 = forever)")
    parser.add_argument("--interval", type=float, default=2.0, help="seconds between readings")
    args = parser.parse_args()
    run(args.host, args.port, args.count, args.interval)


if __name__ == "__main__":
    main()
