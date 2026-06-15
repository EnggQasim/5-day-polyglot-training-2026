"""
Kafka consumer: read Pixel Quest score events from 'player-scores'.

Run:  python 03_consumer.py    (Ctrl+C to stop)
Needs: pip install confluent-kafka   and the Day 2 stack running.
"""
import json
from confluent_kafka import Consumer


def main():
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "score-readers",
        "auto.offset.reset": "earliest",
    })
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
            data = json.loads(msg.value())
            print(f"{data['player']} -> {data['points']} "
                  f"(partition {msg.partition()}, offset {msg.offset()})")
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
