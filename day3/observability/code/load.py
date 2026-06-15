"""
Make some traffic against the API so the dashboards have data to show.
Hits a mix of endpoints, including some 404s.

Run:  python load.py        (Ctrl+C to stop)
Needs: pip install requests   and the API running on :8000.
"""
import random
import time
import requests

BASE = "http://localhost:8000"


def main():
    print("sending requests... (Ctrl+C to stop)")
    try:
        while True:
            r = random.random()
            if r < 0.4:
                requests.get(f"{BASE}/players/{random.randint(1, 12)}")
            elif r < 0.6:
                requests.get(f"{BASE}/players/{random.randint(900, 999)}")   # 404s
            elif r < 0.8:
                requests.get(f"{BASE}/leaderboard", params={"top": 5})
            else:
                requests.get(f"{BASE}/players/{random.randint(1, 12)}/summary")
            time.sleep(0.2)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
