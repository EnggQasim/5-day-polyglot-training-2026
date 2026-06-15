"""
LAB consumer: keep a running leaderboard from the 'player-scores' stream.

Run:  python 05_leaderboard_consumer.py    (Ctrl+C to stop)
Needs: pip install confluent-kafka   and the Day 2 stack running.
"""
import json
from collections import defaultdict
from confluent_kafka import Consumer

totals = defaultdict(int)


def print_board():
    print("\n--- LIVE LEADERBOARD ---")
    top = sorted(totals.items(), key=lambda kv: kv[1], reverse=True)[:5]
    for i, (player, score) in enumerate(top, start=1):
        print(f"{i}. {player:<12} {score}")


def main():
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "leaderboard-builder",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(["player-scores"])
    print("building leaderboard... (Ctrl+C to stop)")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("error:", msg.error())
                continue
            data = json.loads(msg.value())
            totals[data["player"]] += data["points"]
            print_board()
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
