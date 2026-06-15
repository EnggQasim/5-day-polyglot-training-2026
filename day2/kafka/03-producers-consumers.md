# Kafka — Step 3: Producers and consumers in Python

The command line is good for poking around, but real apps use a client library. We use **`confluent-kafka`** (installed in setup). Here you write a producer and a consumer.

> Activate the venv first (`source .venv/bin/activate` or `.venv\Scripts\Activate.ps1`).

---

## A producer

A producer connects to the broker and sends messages to a topic.

```python
from confluent_kafka import Producer
import json

# 'bootstrap.servers' is the broker address from your laptop
producer = Producer({"bootstrap.servers": "localhost:9092"})

def report(err, msg):
    if err:
        print("delivery failed:", err)
    else:
        print(f"delivered to {msg.topic()} [partition {msg.partition()}] @ offset {msg.offset()}")

scores = [
    ("hero_07", 150),
    ("elf_mona", 500),
    ("ninja_sara", 300),
]

for player, points in scores:
    value = json.dumps({"player": player, "points": points})
    # key = player name, so one player's events keep order in one partition
    producer.produce("player-scores", key=player, value=value, callback=report)

producer.flush()   # wait for all messages to be sent
```

Key points:
- **`key=player`** sends all of one player's events to the same partition (keeps order).
- **`value`** is bytes/text; we send JSON. (Tomorrow's Schema Registry lesson makes this safer with Avro.)
- **`flush()`** waits until everything is actually delivered. Forgetting it is the #1 beginner mistake — the program exits before sending.

Run it: `python day2/kafka/code/02_producer.py`

---

## A consumer

A consumer joins a **group**, subscribes to the topic, and polls for messages in a loop.

```python
from confluent_kafka import Consumer
import json

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "score-readers",        # the consumer group name
    "auto.offset.reset": "earliest",    # if no saved position, start at the beginning
})
consumer.subscribe(["player-scores"])

try:
    while True:
        msg = consumer.poll(1.0)        # wait up to 1 second for a message
        if msg is None:
            continue
        if msg.error():
            print("error:", msg.error())
            continue
        data = json.loads(msg.value())
        print(f"{data['player']} -> {data['points']} "
              f"(partition {msg.partition()}, offset {msg.offset()})")
finally:
    consumer.close()
```

Key points:
- **`group.id`** — the consumer group (more in the next lesson).
- **`auto.offset.reset = earliest`** — for a brand-new group with no saved offset, start from the first message. Use `latest` to read only new messages.
- **`poll`** — Kafka clients are pull-based: you ask for messages in a loop.
- **`close()`** — leaves the group cleanly and commits the final position.

Run it (in a second terminal): `python day2/kafka/code/03_consumer.py`

---

## Try it together

1. Start the consumer — it prints existing messages, then waits.
2. In another terminal, run the producer.
3. Watch the three scores appear in the consumer instantly, each tagged with its partition and offset.

➡️ Next: **[04-consumer-groups-offsets.md](04-consumer-groups-offsets.md)** — how groups share work and how offsets remember progress.

---

## ⭐ Must-learn from this topic

- **Producer** — `produce(topic, key, value)`, delivery callbacks, and **`flush()`**.
- **Consumer** — `subscribe`, the **`poll`** loop, `auto.offset.reset`, `close()`.
- **Keys** — send a key to keep per-key ordering.
- **confluent-kafka** — the Python client used throughout Day 2.

### 📚 Official docs
- [confluent-kafka Python client](https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/index.html) — API & examples.
- [Kafka Producer design](https://kafka.apache.org/documentation/#producerapi) and [Consumer design](https://kafka.apache.org/documentation/#consumerapi).
- [Kafka clients in Confluent](https://docs.confluent.io/platform/current/clients/index.html) — all languages.
