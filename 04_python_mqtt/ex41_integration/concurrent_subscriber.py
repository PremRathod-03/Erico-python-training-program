"""
Exercise 41 (part 2): Handling Message Queues and Concurrency in Python

The subscriber:
  - handles multiple topics at once (sensors/temperature, sensors/humidity)
  - never does slow work inside on_message: it only puts the message on a queue.Queue
  - a pool of worker threads takes messages off the queue and processes them concurrently
  - shuts down cleanly (queue.join + sentinel values)

Try it with the built-in load generator:
    python concurrent_subscriber.py --demo
or against real publishers:
    python concurrent_subscriber.py --duration 30
"""
import json
import queue
import random
import sys
import threading
import time
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from mqtt_common import base_parser, make_client  # noqa: E402

TOPICS = [("sensors/temperature", 1), ("sensors/humidity", 1)]
STOP = object()   # sentinel telling a worker to exit


class ConcurrentProcessor:
    def __init__(self, workers: int = 4, work_time: float = 0.2):
        self.q: queue.Queue = queue.Queue(maxsize=1000)
        self.work_time = work_time
        self.lock = threading.Lock()
        self.processed: dict[str, list[float]] = defaultdict(list)
        self.by_worker: dict[str, int] = defaultdict(int)
        self.first_received: float | None = None
        self.last_processed: float | None = None
        self.threads = [threading.Thread(target=self._worker, name=f"worker-{i + 1}", daemon=True)
                        for i in range(workers)]

    def start(self):
        for t in self.threads:
            t.start()

    def on_message(self, _client, _userdata, msg):
        # runs on paho's network thread: keep it fast and just enqueue
        if self.first_received is None:
            self.first_received = time.perf_counter()
        self.q.put((msg.topic, msg.payload))

    def _worker(self):
        name = threading.current_thread().name
        while True:
            item = self.q.get()
            try:
                if item is STOP:
                    return
                topic, payload = item
                value = float(json.loads(payload)["value"])
                time.sleep(self.work_time)            # simulate slow work (DB write, ML inference...)
                with self.lock:
                    self.processed[topic].append(value)
                    self.by_worker[name] += 1
                    self.last_processed = time.perf_counter()
                print(f"{name:<9} processed {topic:<20} value={value}")
            except (ValueError, KeyError, json.JSONDecodeError) as err:
                print(f"{name}: bad message ignored ({err})")
            finally:
                self.q.task_done()

    def stop(self):
        self.q.join()                      # wait for queued work to finish
        for _ in self.threads:
            self.q.put(STOP)
        for t in self.threads:
            t.join()

    def report(self) -> str:
        lines = []
        for topic, values in self.processed.items():
            lines.append(f"  {topic:<20} n={len(values):<3} avg={sum(values) / len(values):.2f}")
        lines.append("  work per thread: " + ", ".join(f"{k}={v}" for k, v in sorted(self.by_worker.items())))
        return "\n".join(lines)


def demo_publisher(host: str, port: int, n: int = 10):
    pub = make_client("ex41-demo-pub")
    pub.connect(host, port)
    pub.loop_start()
    for i in range(n):
        pub.publish("sensors/temperature", json.dumps({"value": round(random.uniform(20, 30), 1)}), qos=1)
        pub.publish("sensors/humidity", json.dumps({"value": round(random.uniform(40, 60), 1)}), qos=1)
    time.sleep(0.5)
    pub.loop_stop()
    pub.disconnect()


def main() -> None:
    parser = base_parser(__doc__)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--duration", type=float, default=0, help="seconds to listen (0 = until Ctrl+C)")
    parser.add_argument("--demo", action="store_true", help="publish 20 test messages and exit")
    args = parser.parse_args()

    processor = ConcurrentProcessor(workers=args.workers)
    processor.start()
    client = make_client("ex41-concurrent")
    client.on_message = processor.on_message
    client.connect(args.host, args.port)
    client.subscribe(TOPICS)
    client.loop_start()
    time.sleep(0.5)

    try:
        if args.demo:
            demo_publisher(args.host, args.port)
            time.sleep(1)
        elif args.duration:
            time.sleep(args.duration)
        else:
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    client.loop_stop()
    client.disconnect()
    processor.stop()
    total = sum(len(v) for v in processor.processed.values())
    if total:
        elapsed = processor.last_processed - processor.first_received
        print(f"\nProcessed {total} messages with {args.workers} threads in {elapsed:.2f}s "
              f"(one thread would need ~{total * processor.work_time:.1f}s)")
    else:
        print("\nNo messages received.")
    print(processor.report())


if __name__ == "__main__":
    main()
