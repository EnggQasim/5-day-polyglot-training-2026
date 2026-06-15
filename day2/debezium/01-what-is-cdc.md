# Debezium — Step 1: What is Change Data Capture (CDC)?

## The problem

On Day 1, scores lived in PostgreSQL. On the last lesson, our **app** published score events to Kafka by hand. But what if a score changes through some other path — an admin tool, a SQL script, a different service? Those changes would **not** reach Kafka, and the leaderboard would be wrong.

We want: *whenever the `players` table changes in any way, an event automatically appears in Kafka.* That is **Change Data Capture (CDC)**.

## What is CDC?

**Change Data Capture** means watching a database and turning every **INSERT / UPDATE / DELETE** into a stream of change events — without changing the application that writes the data.

**Debezium** is the most popular open-source CDC tool. It runs as a **Kafka Connect** connector. For PostgreSQL it reads the **WAL** (write-ahead log) using *logical decoding* — the same logical replication feature you met on Day 1.

```
 someone changes the players table
        │  (INSERT / UPDATE / DELETE)
        ▼
 PostgreSQL WAL  ──read by──►  Debezium (Kafka Connect)  ──►  Kafka topic
                                                              e.g. pq.public.players
```

Because Debezium reads the WAL — the database's own change log — it captures **every** change, no matter who made it. The app does not need to know CDC exists.

## Why this is powerful

- **No app changes.** You add CDC beside an existing database; the app keeps working.
- **Nothing missed.** Every committed change is in the WAL, so every change becomes an event.
- **Decoupling.** Many consumers (search index, cache, analytics, another database) can react to the same changes.
- **Foundation for sync.** CDC is how you keep a cache (Redis), a search index, or a data warehouse in step with your main database.

## Key words

- **Kafka Connect** — a framework for moving data **into** and **out of** Kafka using ready-made **connectors**. It runs as a service (`pq_connect`) with a REST API on port 8083.
- **Source connector** — pulls data *into* Kafka (Debezium is a source connector).
- **Sink connector** — pushes data *out of* Kafka into another system.
- **Logical decoding / `pgoutput`** — the PostgreSQL feature Debezium uses to read changes. `pgoutput` is built into PostgreSQL, so no extra plugin is needed.

## What we will build

We will register a Debezium connector that watches the Day 1 `players` table. Then, when you run an `UPDATE players SET score = ...`, a change event will appear on a Kafka topic — and we will watch it arrive live.

> Make sure you completed setup step 2 (**`ALTER SYSTEM SET wal_level = logical`** and a Postgres restart). Without it, CDC cannot read the WAL.

➡️ Next: **[02-register-connector.md](02-register-connector.md)**

---

## ⭐ Must-learn from this topic

- **CDC** — capturing every INSERT/UPDATE/DELETE as an event, with no app changes.
- **Debezium reads the WAL** — via PostgreSQL logical decoding (`pgoutput`).
- **Kafka Connect** — the framework; **source** vs **sink** connectors.
- **Why it matters** — keeping caches, search indexes, and warehouses in sync.

### 📚 Official docs
- [Debezium connector for PostgreSQL](https://debezium.io/documentation/reference/stable/connectors/postgresql.html) — the connector we use.
- [Debezium architecture](https://debezium.io/documentation/reference/stable/architecture.html) — how it fits with Kafka Connect.
- [Kafka Connect](https://docs.confluent.io/platform/current/connect/index.html) — the connector framework.
