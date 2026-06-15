"""
Register (or re-register) the Debezium players connector via the Kafka Connect REST API.
A no-curl alternative to the POST in the lesson.

Run:  python register_connector.py
Needs: pip install requests   and the Day 2 stack running.
"""
import json
import os
import requests

CONNECT = "http://localhost:8083"
HERE = os.path.dirname(__file__)


def main():
    with open(os.path.join(HERE, "players-connector.json")) as f:
        body = json.load(f)

    name = body["name"]

    # delete first if it already exists, so this script is repeatable
    existing = requests.get(f"{CONNECT}/connectors").json()
    if name in existing:
        requests.delete(f"{CONNECT}/connectors/{name}")
        print(f"deleted existing connector '{name}'")

    r = requests.post(f"{CONNECT}/connectors", json=body)
    print("POST status:", r.status_code)
    print(r.text)

    status = requests.get(f"{CONNECT}/connectors/{name}/status").json()
    print("connector state:", status.get("connector", {}).get("state"))


if __name__ == "__main__":
    main()
