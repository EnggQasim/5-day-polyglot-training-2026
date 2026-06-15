"""
LAB generator: keep sending random Pixel Quest score events to 'player-scores'.

Run:  python 05_score_generator.py    (Ctrl+C to stop)
Needs: pip install confluent-kafka   and the Day 2 stack running.
"""
import json
import random
import time
from confluent_kafka import Producer

PLAYERS = ["hero_07", "elf_mona", "ninja_sara", "mage_lily", "tank_omar"]


def main():
    producer = Producer({"bootstrap.servers": "localhost:9092"})
    print("streaming score events... (Ctrl+C to stop)")
    try:
        while True:
            player = random.choice(PLAYERS)
            points = random.randint(10, 200)
            value = json.dumps({"player": player, "points": points})
            producer.produce("player-scores", key=player, value=value)
            producer.poll(0)
            print(f"sent {player} +{points}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()


if __name__ == "__main__":
    main()
