# Sink Connectors — Step 2: Kafka → Neo4j

Goal: every score event on `player-scores` automatically becomes/updates a node in the Day 1 Neo4j graph. New players appear as `:Player` nodes without anyone touching Neo4j directly.

---

## The production way: the Neo4j Kafka sink connector (read, don't run)

In production you install the **Neo4j Connector for Kafka** plugin into Kafka Connect and POST a config like [`code/neo4j-sink-connector.json`](code/neo4j-sink-connector.json):

```json
{
  "name": "pq-neo4j-sink",
  "config": {
    "connector.class": "org.neo4j.connectors.kafka.sink.Neo4jConnector",
    "topics": "player-scores",
    "neo4j.uri": "bolt://host.docker.internal:7687",
    "neo4j.authentication.basic.username": "neo4j",
    "neo4j.authentication.basic.password": "trainer123",
    "neo4j.cypher.topic.player-scores":
      "MERGE (p:Player {name: event.player}) ON MATCH SET p.score = coalesce(p.score,0) + event.points ON CREATE SET p.score = event.points"
  }
}
```

The key line is `neo4j.cypher.topic.<topic>`: you write **Cypher** that runs for each message, and `event` is the message value. Debezium's image does not include this plugin, so this block is to **understand** the setup — register it the same way as the Debezium connector (`POST /connectors`) if you install the plugin.

> Docs: the Neo4j Connector for Kafka (linked at the bottom). Production installs the plugin jar into Connect's plugin path.

---

## The runnable way: a Python mini-sink

A sink is "a consumer that writes to a target". Here is exactly that, against the Day 1 Neo4j — fully runnable today. File: [`code/neo4j_sink.py`](code/neo4j_sink.py).

```python
from confluent_kafka import Consumer
from neo4j import GraphDatabase
import json

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "trainer123"))

consumer = Consumer({"bootstrap.servers": "localhost:9092",
                     "group.id": "neo4j-sink", "auto.offset.reset": "earliest"})
consumer.subscribe(["player-scores"])

CYPHER = """
MERGE (p:Player {name: $player})
  ON CREATE SET p.score = $points
  ON MATCH  SET p.score = coalesce(p.score, 0) + $points
"""

with driver.session() as session:
    while True:
        msg = consumer.poll(1.0)
        if msg is None or msg.error():
            continue
        e = json.loads(msg.value())
        session.run(CYPHER, player=e["player"], points=e["points"])
        print(f"upserted {e['player']} (+{e['points']})")
```

Each message runs a `MERGE`, so players are created once and their score accumulates — the same logic as the connector's Cypher.

---

## Run it

```bash
# 1) make sure Day 1 Neo4j is up and you have score events flowing:
python day2/kafka/code/05_score_generator.py        # terminal 1 (produces events)

# 2) run the sink:
python day2/connectors/code/neo4j_sink.py           # terminal 2
```

## Verify in Neo4j

```bash
docker exec -it pq_neo4j cypher-shell -u neo4j -p trainer123 \
  "MATCH (p:Player) RETURN p.name, p.score ORDER BY p.score DESC LIMIT 10;"
```

You will see `:Player` nodes appearing and their scores climbing as events arrive — Neo4j is now **kept in sync with the Kafka stream automatically**.

➡️ Next: **[03-milvus-sink.md](03-milvus-sink.md)**

---

## ⭐ Must-learn from this topic

- **Neo4j sink connector** — `neo4j.cypher.topic.<topic>` runs Cypher per message.
- **`MERGE` upsert** — create-or-update nodes from the stream.
- **Mini-sink pattern** — a consumer + a Cypher write does the same job.
- **Auto-sync** — the graph stays current with the Kafka stream.

### 📚 Official docs
- [Neo4j Connector for Kafka](https://neo4j.com/docs/kafka/) — the official sink/source plugin.
- [Neo4j sink — Cypher strategy](https://neo4j.com/docs/kafka/current/sink/) — mapping topics to Cypher.
- [Kafka Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html) — registering it.
