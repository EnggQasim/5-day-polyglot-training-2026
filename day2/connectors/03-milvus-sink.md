# Sink Connectors — Step 3: Custom Kafka → Milvus sink

There is no off-the-shelf Milvus sink connector, so — as the official outline says — we build a **custom** one. The job: for each event on `player-scores`, turn it into a **vector (embedding)** and store it in Milvus, so later you can do **similarity search** over recent activity ("find events like this one").

A "custom connector" here is a small Python consumer that writes to Milvus. File: [`code/milvus_sink.py`](code/milvus_sink.py).

---

## What "turn an event into a vector" means

In a real system an AI model produces the embedding. For training we use a **simple, deterministic** embedding so it runs with no model: we map the player name + points into a small fixed-length vector of numbers. The *plumbing* (consume → embed → upsert → search) is identical to production; only the embedding function would change.

---

## The sink (key parts)

```python
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from confluent_kafka import Consumer
import json, hashlib, numpy as np

DIM = 8
connections.connect(host="localhost", port="19530")

# create the collection once
if not utility.has_collection("pq_events"):
    fields = [
        FieldSchema("id", DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema("player", DataType.VARCHAR, max_length=32),
        FieldSchema("embedding", DataType.FLOAT_VECTOR, dim=DIM),
    ]
    col = Collection("pq_events", CollectionSchema(fields))
    col.create_index("embedding", {"index_type": "IVF_FLAT", "metric_type": "L2",
                                   "params": {"nlist": 16}})
else:
    col = Collection("pq_events")
col.load()

def embed(event):
    # deterministic toy embedding (a real system would use an AI model)
    h = hashlib.md5(f"{event['player']}:{event['points']}".encode()).digest()
    return (np.frombuffer(h[:DIM], dtype=np.uint8) / 255.0).tolist()

# consume and upsert
consumer = Consumer({"bootstrap.servers": "localhost:9092",
                     "group.id": "milvus-sink", "auto.offset.reset": "earliest"})
consumer.subscribe(["player-scores"])
while True:
    msg = consumer.poll(1.0)
    if msg is None or msg.error():
        continue
    e = json.loads(msg.value())
    col.insert([[e["player"]], [embed(e)]])
    print(f"stored embedding for {e['player']}")
```

---

## Run it

```bash
# events flowing (terminal 1)
python day2/kafka/code/05_score_generator.py
# the custom sink (terminal 2)
python day2/connectors/code/milvus_sink.py
```

## Then do a similarity search

After some events are stored, find the events most similar to a query vector with [`code/milvus_search.py`](code/milvus_search.py):

```bash
python day2/connectors/code/milvus_search.py
```

It embeds a sample event and returns the nearest stored events — the payoff of pushing stream data into a vector database.

---

## The full Day 2 picture

You have now connected **all four Day 1 stores** through Kafka:

```
 PostgreSQL ──Debezium(source)──► Kafka ──► KSQLDB (SQL transforms)
                                    │
                                    ├──► Neo4j  (sink: graph nodes)
                                    └──► Milvus (custom sink: embeddings + similarity)
```

That is event-driven architecture: one stream keeps a relational store, a graph, and a vector index all in sync, each doing what it is best at.

### Deliverable for this track
Commit `neo4j_sink.py` and `milvus_sink.py`. In your notes: *Why use sink connectors instead of having the producer write to every database itself? What do you gain when a new consumer (say, a search index) needs the same events later?*

➡️ Next: **[../schema-registry/01-why-schemas.md](../schema-registry/01-why-schemas.md)**

---

## ⭐ Must-learn from this topic

- **Custom sink** — build one when no ready-made connector exists.
- **consume → embed → upsert** — the streaming-to-vector pipeline.
- **Embeddings** — a model in production; a deterministic stub here.
- **Similarity search** on streamed data — the payoff in Milvus.

### 📚 Official docs
- [Milvus insert & search](https://milvus.io/docs/insert-update-delete.md) — writing vectors.
- [Single-vector search](https://milvus.io/docs/single-vector-search.md) — querying them.
- [Kafka Connect — developing connectors](https://docs.confluent.io/platform/current/connect/devguide.html) — building custom ones.
