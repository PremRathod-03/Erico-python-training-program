"""
Exercise 40 (part 2): subscriber that logs sensor data and displays it in real time

- appends every reading to data/temperature_log.csv
- prints a live line with the latest value, running min/avg/max and a trend arrow
- raises an alert when the temperature crosses --alert (default 30 °C)

    python sensor_logger.py                 # until Ctrl+C
    python sensor_logger.py --duration 15
"""
import csv
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

DATA_DIR = Path(__file__).resolve().parent / "data"
CSV_PATH = DATA_DIR / "temperature_log.csv"
FIELDS = ["timestamp", "sensor_id", "value", "unit"]


class SensorStats:
    def __init__(self):
        self.values: list[float] = []

    def add(self, value: float) -> str:
        trend = "→"
        if self.values:
            trend = "↑" if value > self.values[-1] else "↓" if value < self.values[-1] else "→"
        self.values.append(value)
        return trend

    def summary(self) -> str:
        v = self.values
        return f"min {min(v):.2f} | avg {sum(v) / len(v):.2f} | max {max(v):.2f} | n={len(v)}"


def make_on_message(stats: SensorStats, alert: float, csv_path: Path = CSV_PATH):
    def on_message(_client, _userdata, msg):
        try:
            reading = json.loads(msg.payload)
            value = float(reading["value"])
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print(f"Ignoring malformed payload on {msg.topic}: {msg.payload[:60]!r}")
            return
        new_file = not csv_path.exists()
        with open(csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS, extrasaction="ignore")
            if new_file:
                writer.writeheader()
            writer.writerow(reading)
        trend = stats.add(value)
        flag = "  ⚠ HIGH TEMPERATURE ALERT" if value >= alert else ""
        print(f"{reading.get('timestamp', '')}  {value:6.2f} °C {trend}  ({stats.summary()}){flag}")
    return on_message


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--duration", type=float, default=0, help="seconds to run (0 = until Ctrl+C)")
    parser.add_argument("--alert", type=float, default=30.0, help="alert threshold in °C")
    args = parser.parse_args()
    DATA_DIR.mkdir(exist_ok=True)

    client = make_client("sensor-logger")
    client.on_message = make_on_message(SensorStats(), args.alert)
    client.on_connect = lambda c, *_: c.subscribe([("sensors/temperature", 1), ("sensors/status/#", 1)])
    client.message_callback_add(
        "sensors/status/#", lambda _c, _u, m: print(f"[status] {m.topic.split('/')[-1]} is {m.payload.decode()}"))
    client.connect(args.host, args.port)
    print(f"Logging sensors/temperature to {CSV_PATH} (Ctrl+C to stop)")

    if args.duration:
        client.loop_start()
        time.sleep(args.duration)
        client.loop_stop()
    else:
        try:
            client.loop_forever()
        except KeyboardInterrupt:
            print("\nStopped")
    client.disconnect()


if __name__ == "__main__":
    main()
