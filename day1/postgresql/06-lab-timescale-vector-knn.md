# PostgreSQL — Step 6: LAB (TimescaleDB hypertable + vector + K-NN)

This is the hands-on lab. You will:
1. Make a **hypertable** with TimescaleDB to store time-based data (player events).
2. Add a **vector** column to a table of game items.
3. Run a **K-NN** ("k nearest neighbours") query to find the most similar items.

Both extensions (TimescaleDB and pgvector) are already in our Docker image.

---

## What is TimescaleDB?

TimescaleDB is an extension that makes PostgreSQL great at **time-series data** — data that arrives over time, like sensor readings or, here, **game events** (every time a player scores, logs in, etc.). It automatically splits the table into time-based chunks behind the scenes (a "hypertable"), so queries over a time range stay fast as data grows.

---

## Step 1 — Make a hypertable of player events

```sql
CREATE EXTENSION IF NOT EXISTS timescaledb;

DROP TABLE IF EXISTS player_events;
CREATE TABLE player_events (
    event_time TIMESTAMPTZ NOT NULL,
    player_id  INTEGER NOT NULL,
    event_type TEXT NOT NULL,     -- 'login', 'score', 'logout'
    points     INTEGER DEFAULT 0
);

-- turn the ordinary table into a hypertable, chunked by event_time
SELECT create_hypertable('player_events', 'event_time');
```

Add some events:

```sql
INSERT INTO player_events (event_time, player_id, event_type, points) VALUES
    ('2026-03-01 09:00', 1, 'login', 0),
    ('2026-03-01 09:05', 1, 'score', 150),
    ('2026-03-01 09:10', 4, 'score', 300),
    ('2026-03-02 10:00', 8, 'login', 0),
    ('2026-03-02 10:15', 8, 'score', 220),
    ('2026-03-03 11:00', 12,'score', 500);
```

A time-series query — total points scored per day:

```sql
SELECT time_bucket('1 day', event_time) AS day,
       sum(points) AS points_that_day
FROM player_events
WHERE event_type = 'score'
GROUP BY day
ORDER BY day;
```

`time_bucket` is a TimescaleDB helper that groups rows into time windows (here, 1 day). This is the bread-and-butter of time-series analytics.

---

## Step 2 — Add a vector column and run K-NN

We reuse the items idea, but now with **bigger vectors** and a real nearest-neighbour search.

```sql
CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS items;
CREATE TABLE items (
    item_id   SERIAL PRIMARY KEY,
    name      TEXT,
    embedding vector(4)        -- 4 numbers this time
);

INSERT INTO items (name, embedding) VALUES
    ('sword',       '[0.90, 0.10, 0.00, 0.05]'),
    ('great sword', '[0.88, 0.12, 0.02, 0.04]'),  -- very similar to sword
    ('dagger',      '[0.70, 0.20, 0.10, 0.05]'),
    ('potion',      '[0.05, 0.90, 0.05, 0.10]'),
    ('shield',      '[0.10, 0.10, 0.90, 0.20]');
```

**K-NN query:** find the 3 items most similar to a sword-like vector.

```sql
SELECT name,
       embedding <-> '[0.90, 0.10, 0.00, 0.05]' AS distance
FROM items
ORDER BY embedding <-> '[0.90, 0.10, 0.00, 0.05]'
LIMIT 3;          -- the "k" in K-NN is 3
```

Expected: `sword` first (distance 0), `great sword` very close behind, then `dagger`. The potion and shield are far away because their numbers point in different directions.

Add an index so this stays fast on big tables:

```sql
CREATE INDEX ON items USING ivfflat (embedding vector_l2_ops) WITH (lists = 10);
```

---

## What you achieved

- A **hypertable** for time-series events, with a `time_bucket` daily report.
- A **vector** column and a working **K-NN** similarity search inside plain PostgreSQL.

This shows PostgreSQL can do a *little* of what the specialist databases do. Later you will see Milvus do vector search at a much bigger scale, and that contrast is the whole point of Day 1: **pick the right tool for the job.**

**Run the whole lab:** [`code/06_lab.sql`](code/06_lab.sql)

### Deliverable for this track
Commit your `.sql` files and write 2–3 lines in your notes: *When would you keep vector search inside PostgreSQL, and when would you move it to Milvus?* (Hint: number of vectors, query speed needed, and whether you want one database or a specialist one.)

➡️ Back to the day plan: **[../README.md](../README.md)** · Next engine: **[../redis/01-intro-and-data.md](../redis/01-intro-and-data.md)**

---

## ⭐ Must-learn from this topic

- **TimescaleDB hypertables** — `create_hypertable`, chunks, and why time-series scales.
- **`time_bucket`** — grouping rows into time windows for reports.
- **Continuous aggregates** — pre-computed rollups (great next step after this lab).
- **pgvector K-NN** — choosing a distance metric and a vector index for nearest-neighbour search.

### 📚 Official docs
- [TimescaleDB — Hypertables](https://docs.timescale.com/use-timescale/latest/hypertables/) — create & use them.
- [time_bucket](https://docs.timescale.com/api/latest/hyperfunctions/time_bucket/) — the function reference.
- [Continuous aggregates](https://docs.timescale.com/use-timescale/latest/continuous-aggregates/) — faster time-series rollups.
- [pgvector (README)](https://github.com/pgvector/pgvector) — vector search reference.
