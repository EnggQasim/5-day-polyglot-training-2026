# Sink Connectors — Step 1: Source vs sink

So far Debezium pulled changes **into** Kafka (a **source** connector). Now we go the other way: take data **out of** Kafka and write it into another system. That is a **sink** connector.

```
            SOURCE                         SINK
 PostgreSQL ──► Kafka topic ──► Neo4j   (auto-create nodes)
                      │
                      └──────► Milvus  (store embeddings for similarity search)
```

This is the heart of "event-driven architecture": one stream of events updates **many** systems automatically, each shaped for its job (graph queries in Neo4j, similarity search in Milvus) — exactly the Day 1 "right tool for the job" idea, now kept in sync in real time.

---

## Two ways to build a sink

1. **A ready-made Kafka Connect sink connector** — you give Connect a JSON config and it does the work, no code. This is how the Neo4j sink works in production (you install the Neo4j Kafka Connector plugin into Kafka Connect).
2. **A custom sink** — for systems without an off-the-shelf connector (like Milvus), you write a small consumer that reads the topic and writes to the target. The official Day 2 outline calls this a *"custom Milvus sink connector"*.

> **Honest note about our training image:** the `debezium/connect` container only ships **Debezium** plugins, not the Neo4j sink plugin. So in these lessons we:
> - show the **real connector config** so you understand the production setup (**read, don't run**), and
> - provide a **runnable Python mini-sink** that does the same job against the Day 1 Neo4j / Milvus, so you can actually see it work today.
>
> A "sink connector" is conceptually just *a consumer that writes to a target* — the Python version makes that concrete.

---

## What we will build

- **Neo4j sink:** consume the `player-scores` stream and **MERGE** a `:Player` node (and a `:SCORED` relationship) for each event — the graph updates itself as scores flow.
- **Milvus sink:** turn each event into a small **vector** and upsert it into a Milvus collection, so you can later do similarity search over recent activity.

Both reuse the Day 1 databases, so make sure Day 1 is up (`docker compose up -d`) and you have produced some messages to `player-scores` (the Kafka lab, or run the score generator).

➡️ Next: **[02-neo4j-sink.md](02-neo4j-sink.md)**

---

## ⭐ Must-learn from this topic

- **Source vs sink** — into Kafka vs out of Kafka.
- **Two ways** — a ready-made Connect sink (config only) vs a custom consumer.
- **Event-driven sync** — one stream updates many systems automatically.
- **A sink = a consumer that writes to a target.**

### 📚 Official docs
- [Kafka Connect concepts](https://docs.confluent.io/platform/current/connect/index.html#connect-concepts) — source & sink.
- [Confluent Hub connectors](https://www.confluent.io/hub/) — ready-made sinks.
- [Kafka Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html) — register any connector.
