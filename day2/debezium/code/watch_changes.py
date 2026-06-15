"""
Watch the Debezium change topic and print a friendly one-line summary per change.

Run:  python watch_changes.py    (Ctrl+C to stop)
Needs: pip install confluent-kafka   and the connector registered.

Note: our connector uses the JSON converter with schemas disabled, so each
message value is a JSON object with op / before / after fields.
"""
import json
from confluent_kafka import Consumer


def summarize(value):
    if value is None:
        return "(tombstone / delete marker)"
    rec = json.loads(value)
    op = rec.get("op")
    before, after = rec.get("before"), rec.get("after")
    if op in ("c", "r"):   # create or snapshot-read
        who = after.get("username")
        return f"{'CREATE' if op=='c' else 'SNAPSHOT'} {who}: score={after.get('score')}"
    if op == "u":
        who = after.get("username")
        return f"UPDATE {who}: score {before.get('score')} -> {after.get('score')}"
    if op == "d":
        who = before.get("username")
        return f"DELETE {who}"
    return f"op={op}"


def main():
    consumer = Consumer({
        "bootstrap.servers": "localhost:9092",
        "group.id": "cdc-watcher",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(["pq.public.players"])
    print("watching pq.public.players ... (Ctrl+C to stop)")

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print("error:", msg.error())
                continue
            try:
                print(summarize(msg.value()))
            except Exception as e:
                print("could not parse message:", e)
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
