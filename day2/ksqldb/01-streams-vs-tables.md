# KSQLDB — Step 1: Streams vs tables

## What is KSQLDB?

**KSQLDB** lets you process Kafka data using **SQL** instead of writing producer/consumer code. You write familiar `SELECT` / `CREATE` statements, and KSQLDB runs them continuously over the stream. It is perfect for filtering, transforming, joining, and aggregating events in real time.

It runs as a server (`pq_ksqldb`, port 8088). You talk to it with a CLI.

## Open the KSQLDB CLI

```bash
docker exec -it pq_ksqldb ksql http://localhost:8088
```

You get a `ksql>` prompt. To leave, type `exit`.

> First run a quick check at the prompt: `SHOW TOPICS;` lists the Kafka topics KSQLDB can see.

---

## The big idea: stream vs table

KSQLDB has two ways to look at the same Kafka data. Understanding the difference is the whole lesson.

### A STREAM = a log of events ("things that happened")

A **stream** is an unbounded sequence of events, each independent. Every new message is **appended**. Think: *"hero_07 scored 150", "hero_07 scored 60"* — two separate facts, both kept.

Use a stream when each event matters on its own: clicks, scores, payments, sensor readings.

### A TABLE = the latest value per key ("what is true now")

A **table** keeps only the **most recent** value for each key. New messages with the same key **replace** the old value. Think: *current total score per player* — one row per player, always the latest.

Use a table when you care about the current state, not the history.

### The link between them

They are two views of the same log:
- Read a topic as a **stream** → you see every event.
- Read/aggregate it as a **table** → you see the current value per key.

This is often called "stream-table duality". A table is really a stream of updates, folded down to the latest value per key.

---

## Create a stream over our topic

We point a stream at the `player-scores` topic from the Kafka lab (JSON values):

```sql
CREATE STREAM player_scores (
    player VARCHAR,
    points INT
) WITH (
    KAFKA_TOPIC = 'player-scores',
    VALUE_FORMAT = 'JSON',
    PARTITIONS = 3
);
```

- The columns describe the shape of each message.
- `KAFKA_TOPIC` is the source topic.
- `VALUE_FORMAT = 'JSON'` matches how we produced the data.

See it:

```sql
SHOW STREAMS;
DESCRIBE player_scores;
```

---

## Read the stream

A **push query** (`EMIT CHANGES`) keeps running and prints new events as they arrive:

```sql
SELECT player, points
FROM player_scores
EMIT CHANGES;
```

Leave this running, then (in another terminal) run the Day 2 Kafka score generator. New rows print live here. Press **Ctrl+C** to stop the query.

> `EMIT CHANGES` = "keep showing me changes forever". Without it you get a one-time (pull) query — more on that next lesson.

**Statements also in** [`code/01_create_stream.ksql`](code/01_create_stream.ksql).

➡️ Next: **[02-querying-streams.md](02-querying-streams.md)**

---

## ⭐ Must-learn from this topic

- **KSQLDB** — process Kafka data with SQL instead of code.
- **STREAM vs TABLE** — a log of events vs the latest value per key (stream-table duality).
- **`CREATE STREAM ... WITH (KAFKA_TOPIC, VALUE_FORMAT)`** — define a stream over a topic.
- **`EMIT CHANGES`** — a push query that streams results forever.

### 📚 Official docs
- [ksqlDB concepts](https://docs.confluent.io/platform/current/ksqldb/concepts/overview.html) — streams, tables, queries.
- [Streams](https://docs.confluent.io/platform/current/ksqldb/concepts/streams.html) — the event view.
- [CREATE STREAM](https://docs.confluent.io/platform/current/ksqldb/developer-guide/ksqldb-reference/create-stream.html) — the statement reference.
