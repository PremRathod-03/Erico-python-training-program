"""
Offline tests for the MQTT module (no broker needed).
End-to-end checks against a live broker: see README.md ("Run everything").
"""
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace

MODULE = Path(__file__).resolve().parent.parent
for sub in ["", "ex33_topics", "ex40_iot_sensor", "ex41_integration", "mini_project_7_mqtt_pubsub"]:
    sys.path.insert(0, str(MODULE / sub))

import concurrent_subscriber as cs     # noqa: E402
import publisher as mp7_pub            # noqa: E402
import sensor_logger                   # noqa: E402
import sensor_simulator                # noqa: E402
import subscriber as mp7_sub           # noqa: E402
import topics                          # noqa: E402


def fake_msg(topic: str, payload) -> SimpleNamespace:
    if not isinstance(payload, bytes):
        payload = json.dumps(payload).encode()
    return SimpleNamespace(topic=topic, payload=payload, qos=1)


class TestTopics(unittest.TestCase):
    def test_wildcards(self):
        table = topics.matching_table()
        self.assertEqual(len(table["home/+/temperature"]), 3)
        self.assertEqual(sorted(table["home/kitchen/#"]), ["home/kitchen/smoke", "home/kitchen/temperature"])
        self.assertEqual(len(table["home/#"]), len(topics.TOPICS))
        self.assertNotIn("home/kitchen/smoke", table["home/+/temperature"])


class TestSensor(unittest.TestCase):
    def test_readings_in_range_and_json(self):
        sensor = sensor_simulator.TemperatureSensor(seed=1)
        for _ in range(500):
            r = sensor.read()
            self.assertTrue(15 <= r["value"] <= 40)
        json.dumps(r)
        self.assertEqual(r["sensor"], "temperature")

    def test_logger_writes_csv_and_skips_bad(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "log.csv"
            stats = sensor_logger.SensorStats()
            handler = sensor_logger.make_on_message(stats, alert=30, csv_path=path)
            from io import StringIO
            from contextlib import redirect_stdout
            with redirect_stdout(StringIO()) as out:
                handler(None, None, fake_msg("sensors/temperature", {"value": 25, "sensor_id": "s1"}))
                handler(None, None, fake_msg("sensors/temperature", {"value": 31, "sensor_id": "s1"}))
                handler(None, None, fake_msg("sensors/temperature", b"not json"))
            self.assertIn("ALERT", out.getvalue())
            self.assertIn("malformed", out.getvalue())
            self.assertEqual(len(path.read_text().strip().splitlines()), 3)   # header + 2 rows
            self.assertEqual(stats.values, [25.0, 31.0])


class TestConcurrency(unittest.TestCase):
    def test_workers_process_all_messages_in_parallel(self):
        from io import StringIO
        from contextlib import redirect_stdout
        proc = cs.ConcurrentProcessor(workers=4, work_time=0.1)
        proc.start()
        with redirect_stdout(StringIO()):
            start = time.perf_counter()
            for i in range(8):
                topic = "sensors/temperature" if i % 2 else "sensors/humidity"
                proc.on_message(None, None, fake_msg(topic, {"value": i}))
            proc.stop()
            elapsed = time.perf_counter() - start
        self.assertEqual(sum(len(v) for v in proc.processed.values()), 8)
        self.assertLess(elapsed, 0.6)            # 8 x 0.1 s sequential = 0.8 s
        self.assertGreater(len(proc.by_worker), 1)


class TestMiniProject7(unittest.TestCase):
    def test_message_shape_and_row(self):
        msg = mp7_pub.random_message(1)
        self.assertEqual(set(msg), {"id", "device", "temperature", "humidity",
                                    "battery", "status", "note", "timestamp"})
        row = mp7_sub.format_row(msg)
        self.assertIn(msg["device"], row)


if __name__ == "__main__":
    unittest.main()
