"""
Kafka producer: send a few Pixel Quest score events to the 'player-scores' topic.

Run:  python 02_producer.py
Needs: pip install confluent-kafka   and the Day 2 stack running.
"""

import json

from confluent_kafka import Producer


def report(err, msg):
    if err:
        print("delivery failed:", err)
    else:
        print(
            f"delivered to {msg.topic()} [partition {msg.partition()}] @ offset {msg.offset()}"
        )


def main():
    producer = Producer({"bootstrap.servers": "localhost:9092"})

    scores = [
        ("XYZ_01", 150),
        # ("elf_mona", 500),
        # ("ninja_sara", 300),
        # ("hero_07", 60),
        ("ABC_12", 700),
    ]

    for player, points in scores:
        value = json.dumps({"player": player, "points": points})
        producer.produce("player-scores", key=player, value=value, callback=report)
        producer.poll(0)  # serve delivery callbacks

    producer.flush()  # wait for all messages to be delivered
    print("done.")


if __name__ == "__main__":
    main()
