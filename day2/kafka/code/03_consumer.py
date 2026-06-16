"""
Kafka consumer: read Pixel Quest score events from 'player-scores'.

Run:  python 03_consumer.py    (Ctrl+C to stop)
Needs: pip install confluent-kafka   and the Day 2 stack running.
"""

import json

from confluent_kafka import Consumer


def main():
    consumer = Consumer(
        {
            "bootstrap.servers": "localhost:9092",
            "group.id": "analytics",
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe(["player-scores"])
    print("listening... (Ctrl+C to stop)")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("error:", msg.error())
                continue
            raw = msg.value()
            if not raw:  # skip null/empty (e.g. tombstone) messages
                continue
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                print(
                    f"skipping non-JSON message at "
                    f"partition {msg.partition()}, offset {msg.offset()}: {raw!r}"
                )
                continue
            print(
                f"{data['player']} -> {data['points']} "
                f"(partition {msg.partition()}, offset {msg.offset()})"
            )
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
