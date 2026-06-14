"""
Make a bigger players.csv so you can practise indexes and EXPLAIN ANALYZE
on a table with many rows (the 12-row table is too small to feel slow).

Usage:
    python generate_players_csv.py 100000      # makes players.csv with 100k rows

Then load it into postgres:
    docker exec -i pq_postgres psql -U trainer -d pixelquest -c \
      "\copy players_big(username,country,score,created_at) FROM STDIN WITH (FORMAT csv, HEADER true)" < players.csv

(First create the table:
    CREATE TABLE players_big (
        player_id  SERIAL PRIMARY KEY,
        username   TEXT, country CHAR(2), score INTEGER, created_at DATE);
)
"""
import csv
import random
import sys
from datetime import date, timedelta

COUNTRIES = ["PK", "US", "IN", "GB", "DE", "FR", "BR", "JP"]
WORDS = ["hero", "mage", "tank", "ninja", "rogue", "archer", "healer",
         "knight", "witch", "bard", "giant", "elf", "orc", "wolf"]


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    start = date(2026, 1, 1)
    with open("players.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["username", "country", "score", "created_at"])
        for i in range(n):
            username = f"{random.choice(WORDS)}_{i}"
            country = random.choice(COUNTRIES)
            score = random.randint(0, 10000)
            created = start + timedelta(days=random.randint(0, 150))
            w.writerow([username, country, score, created.isoformat()])
    print(f"Wrote players.csv with {n} rows.")


if __name__ == "__main__":
    main()
