# KSQLDB — Step 2: Querying and transforming streams

Now we filter, transform, and aggregate the stream — all in SQL. Make sure the `player_scores` stream from the last lesson exists.

---

## Push vs pull queries

- **Push query** (`EMIT CHANGES`) — runs forever, emitting results as new data arrives. Great for live dashboards.
- **Pull query** — a one-time lookup of the current value, like a normal database query. Works against **tables** and **materialized views**.

---

## Filter a stream

Only big scores (a push query):

```sql
SELECT player, points
FROM player_scores
WHERE points > 100
EMIT CHANGES;
```

## Transform / add columns

```sql
SELECT player,
       points,
       points * 2 AS double_points,
       UCASE(player) AS player_upper
FROM player_scores
EMIT CHANGES;
```

KSQLDB has many built-in functions (string, math, date, JSON). You shape events on the fly.

---

## Create a derived stream (a persistent query)

`CREATE STREAM ... AS SELECT` (called **CSAS**) makes a **new** stream backed by a **new** Kafka topic, continuously filled by the query. This is how you build pipelines: one stream feeds the next.

```sql
CREATE STREAM big_scores AS
    SELECT player, points
    FROM player_scores
    WHERE points > 100
    EMIT CHANGES;
```

Now `big_scores` is its own topic that always contains only the high scores. Other apps (or KSQLDB queries) can read it.

```sql
SHOW STREAMS;          -- big_scores now appears
SHOW QUERIES;          -- the persistent query feeding it is listed
```

---

## Aggregate into a table

Totals **per player** are *state* (one value per key), so the result is a **table**, built with `GROUP BY`:

```sql
CREATE TABLE score_totals AS
    SELECT player,
           SUM(points) AS total_points,
           COUNT(*)    AS score_count
    FROM player_scores
    GROUP BY player
    EMIT CHANGES;
```

Because `score_totals` is a table (current value per player), you can run a **pull query** — an instant lookup:

```sql
SELECT player, total_points
FROM score_totals
WHERE player = 'hero_07';
```

This returns the current total immediately, like querying a database — but the value was computed live from the stream.

---

## Windowed aggregation (time buckets)

Real dashboards often ask "how many points in the last minute?". A **windowed** aggregate groups events by time:

```sql
SELECT player,
       COUNT(*) AS scores_last_minute,
       SUM(points) AS points_last_minute
FROM player_scores
WINDOW TUMBLING (SIZE 1 MINUTE)
GROUP BY player
EMIT CHANGES;
```

`WINDOW TUMBLING (SIZE 1 MINUTE)` cuts the stream into back-to-back 1-minute buckets — the streaming cousin of Day 1's TimescaleDB `time_bucket`.

**Statements also in** [`code/02_transform_aggregate.ksql`](code/02_transform_aggregate.ksql).

➡️ Next: **[04-udfs.md](04-udfs.md)** — built-in functions and UDFs.

---

## ⭐ Must-learn from this topic

- **Push vs pull queries** — live `EMIT CHANGES` vs instant lookups on tables.
- **Filter & transform** — `WHERE`, computed columns, built-in functions.
- **CSAS / CTAS** — `CREATE STREAM/TABLE AS SELECT` to build persistent pipelines.
- **Windowed aggregates** — `WINDOW TUMBLING` for per-time-bucket results.

### 📚 Official docs
- [Stream processing concepts](https://docs.confluent.io/platform/current/ksqldb/concepts/stream-processing.html) — push/pull & persistent queries.
- [CREATE STREAM AS SELECT](https://docs.confluent.io/platform/current/ksqldb/developer-guide/ksqldb-reference/create-stream-as-select.html) — derived streams.
- [ksqlDB SQL reference](https://docs.confluent.io/platform/current/ksqldb/developer-guide/ksqldb-reference/) — functions, windows, syntax.
