"""
A durable producer: acks=all + idempotence (no duplicates on retry).

Run:  python 06_reliable_producer.py
Needs: pip install confluent-kafka   and the Day 2 stack running.
"""
import json
from confluent_kafka import Producer


def report(err, msg):
    if err:
        print("delivery FAILED:", err)
    else:
        print(f"delivered @ partition {msg.partition()} offset {msg.offset()}")


def main():
    producer = Producer({
        "bootstrap.servers": "localhost:9092",
        "acks": "all",                 # wait for all in-sync replicas
        "enable.idempotence": True,    # safe retries, no duplicates
        "retries": 5,
    })

    for player, points in [("hero_07", 150), ("elf_mona", 500), ("hero_07", 60)]:
        producer.produce("player-scores", key=player,
                         value=json.dumps({"player": player, "points": points}),
                         callback=report)
        producer.poll(0)

    producer.flush()
    print("done (durable settings: acks=all, idempotent).")


if __name__ == "__main__":
    main()
