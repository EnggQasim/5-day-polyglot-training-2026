# Day 2 — Real-Time Streaming & Connectors

**Goal:** Learn how data moves **live** between systems. By the end of today you can publish and subscribe to events with **Kafka**, capture database changes automatically with **Debezium (CDC)**, keep data well-shaped with **Schema Registry**, and transform streams using SQL with **KSQLDB**.

> **How we teach here (same as Day 1):** easy English, one idea at a time, explanation → a small example with our **Pixel Quest** data → the exact command/code to run → what output to expect. Folder per component, runnable code, and a **⭐ Must-learn + 📚 Official docs** box at the end of every lesson.

---

## The big picture: why streaming?

On Day 1 each database held data and you queried it when you asked. But real systems need data to **move on its own, the moment it changes**. When a player's score updates in PostgreSQL, a leaderboard, a fraud check, and an analytics dashboard might all need to know — instantly.

**Kafka** is the highway that carries these events. **Debezium** watches PostgreSQL and turns every change into an event automatically. **Schema Registry** makes sure every event has an agreed shape. **KSQLDB** lets you filter and combine streams using plain SQL.

### Today's story (it builds on Day 1)

```
 PostgreSQL (Day 1)         Kafka            KSQLDB              you watch
 players / scores  ──CDC──►  topic  ──►  filter & aggregate  ──►  live high-scores
        ▲ Debezium captures      (the event highway)    (SQL on streams)
        │ every INSERT/UPDATE
```

Every score change in PostgreSQL flows through Kafka in real time, gets reshaped by KSQLDB, and becomes a live "high scores" stream.

---

## What you will learn

| Component | What it does | Pixel Quest example |
|-----------|--------------|---------------------|
| **Kafka** | the event highway (publish/subscribe) | stream "player scored" events |
| **Debezium (CDC)** | turns DB changes into events automatically | capture edits to the `players` table |
| **Schema Registry** | agrees the shape of each event (Avro) | a `PlayerScore` schema |
| **KSQLDB** | transforms streams with SQL | live "high scores above 6000" stream |

---

## Before you start

Day 2 needs the **Day 1 PostgreSQL** running (for change-data-capture) **plus** the new Kafka stack.

1. Make sure Day 1's databases are up (from the repo top folder):
   ```bash
   docker compose up -d
   ```
2. Start the Day 2 streaming stack:
   ```bash
   docker compose -f day2/docker-compose.day2.yml up -d
   ```
3. Follow **[`00-setup/README.md`](00-setup/README.md)** to enable logical replication and check every service.

> New to the terminal? The Day 1 guide still applies: **[../day1/00-setup/02-how-to-run-queries.md](../day1/00-setup/02-how-to-run-queries.md)**.

---

## Suggested schedule

**Setup (first 30 min)** — start both stacks, enable Postgres logical replication, verify Kafka / Schema Registry / Connect / KSQLDB.

**Morning — Concepts**
- Kafka: brokers, topics, partitions, producers, consumers, groups, offsets; reliability — ISR/replication, `acks`, idempotent producers, exactly-once.
- Debezium: change-data-capture from the Postgres WAL (source).
- Sink connectors: Kafka → Neo4j and a custom Kafka → Milvus sink.
- Schema Registry: schemas, Avro, compatibility modes.
- KSQLDB: streams vs tables, querying/aggregating, functions & UDFs.

**Afternoon — Labs**
- Kafka: producer/consumer score stream; throughput benchmark (≥10k msg/s).
- Debezium: capture live `players` edits as Kafka messages.
- Sinks: stream events into Neo4j nodes and Milvus embeddings.
- Schema Registry: produce/consume Avro with a registered schema.
- KSQLDB: build the live high-scores pipeline end to end.

---

## Lessons in order

### 0. Setup
- [`00-setup/README.md`](00-setup/README.md) — start the stream stack, enable CDC, test connections.

### 1. Kafka — the event highway
1. [Intro & concepts](kafka/01-intro-and-concepts.md)
2. [Topics & the CLI](kafka/02-topics-and-cli.md)
3. [Producers & consumers (Python)](kafka/03-producers-consumers.md)
4. [Consumer groups & offsets](kafka/04-consumer-groups-offsets.md)
5. [LAB: stream Pixel Quest score events](kafka/05-lab-score-stream.md)
6. [Reliability & delivery (ISR, acks, idempotence, exactly-once)](kafka/06-reliability-and-delivery.md)
7. [LAB: throughput benchmark (≥10k msg/s)](kafka/07-lab-throughput-benchmark.md)

### 2. Debezium — Change Data Capture (source)
1. [What is CDC?](debezium/01-what-is-cdc.md)
2. [Register a Postgres connector](debezium/02-register-connector.md)
3. [LAB: capture player changes live](debezium/03-lab-capture-player-changes.md)

### 3. Sink connectors — Kafka → Neo4j & Milvus
1. [Source vs sink](connectors/01-sink-connectors-intro.md)
2. [Kafka → Neo4j sink](connectors/02-neo4j-sink.md)
3. [Custom Kafka → Milvus sink](connectors/03-milvus-sink.md)

### 4. Schema Registry — agreed data shapes
1. [Why schemas?](schema-registry/01-why-schemas.md)
2. [Avro & compatibility](schema-registry/02-avro-and-compatibility.md)
3. [LAB: produce & consume Avro](schema-registry/03-lab-avro-produce-consume.md)

### 5. KSQLDB — SQL on streams
1. [Streams vs tables](ksqldb/01-streams-vs-tables.md)
2. [Querying streams](ksqldb/02-querying-streams.md)
3. [Functions & UDFs](ksqldb/04-udfs.md)
4. [LAB: live high-scores pipeline](ksqldb/03-lab-high-scores-pipeline.md)

---

## End-of-day result (deliverable)

Commit your producer/consumer scripts, the Debezium connector JSON, the Avro schema, and the `.ksql` scripts, plus a short `notes.md` answering: *When would you use Debezium CDC instead of having your app publish events itself? What does Schema Registry protect you from?*

## When you finish, stop the stack to free memory

```bash
docker compose -f day2/docker-compose.day2.yml down
```
