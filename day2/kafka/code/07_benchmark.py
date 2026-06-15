"""
Simple Python producer throughput benchmark.

Run:  python 07_benchmark.py
Needs: pip install confluent-kafka   and the Day 2 stack running.

Key idea: queue many messages and flush ONCE at the end (batching),
rather than waiting for each message individually.
"""
import time
from confluent_kafka import Producer

TOPIC = "perf-test"
N = 100_000
SIZE = 200


def main():
    producer = Producer({
        "bootstrap.servers": "localhost:9092",
        "acks": "1",
        "linger.ms": 5,            # let the client batch for up to 5ms
        "batch.size": 64 * 1024,   # bigger batches = higher throughput
    })

    payload = b"x" * SIZE
    start = time.time()
    for i in range(N):
        producer.produce(TOPIC, key=str(i % 100), value=payload)
        if i % 10000 == 0:
            producer.poll(0)       # serve delivery callbacks periodically
    producer.flush()               # wait for everything to be delivered
    elapsed = time.time() - start

    rate = N / elapsed
    print(f"produced {N} msgs in {elapsed:.2f}s -> {rate:,.0f} msg/s")
    print("target was >= 10,000 msg/s")


if __name__ == "__main__":
    main()
