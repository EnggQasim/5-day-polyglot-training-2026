# KSQLDB — Step 3: LAB (live high-scores pipeline)

This lab ties Day 2 together. You will build a small streaming pipeline with SQL:

1. A **stream** over the live score events.
2. A derived **stream** of only high scores (> 400).
3. A **table** of running totals per player, queryable instantly.
4. A **windowed** count of activity per minute.

You feed it with the Kafka score generator from earlier, so data is always flowing.

---

## Step 1 — start the data flowing

In a terminal, run the generator from the Kafka lab (it emits a score every half second):

```bash
python day2/kafka/code/05_score_generator.py
```

Leave it running.

## Step 2 — open KSQLDB and build the pipeline

In another terminal:

```bash
docker exec -it pq_ksqldb ksql http://localhost:8088
```

Run these at the `ksql>` prompt (also in [`code/03_pipeline.ksql`](code/03_pipeline.ksql)):

```sql
-- read the topic as a stream
CREATE STREAM player_scores (player VARCHAR, points INT)
  WITH (KAFKA_TOPIC='player-scores', VALUE_FORMAT='JSON', PARTITIONS=3);

-- 1) high scores only -> their own topic
CREATE STREAM high_scores AS
  SELECT player, points FROM player_scores
  WHERE points > 400
  EMIT CHANGES;

-- 2) running total per player (a TABLE = current value per key)
CREATE TABLE score_totals AS
  SELECT player, SUM(points) AS total_points, COUNT(*) AS n
  FROM player_scores
  GROUP BY player
  EMIT CHANGES;
```

## Step 3 — watch it work

**Live high scores (push query):**
```sql
SELECT player, points FROM high_scores EMIT CHANGES;
```
Only events above 400 appear. Ctrl+C to stop.

**Instant total for one player (pull query):**
```sql
SELECT player, total_points, n FROM score_totals WHERE player = 'elf_mona';
```
Returns the current total immediately — computed live from the stream.

**Live leaderboard (push query over the table):**
```sql
SELECT player, total_points FROM score_totals EMIT CHANGES;
```
You will see totals climb as the generator keeps producing.

---

## How this connects the whole day

```
 Day 1 Postgres ──Debezium CDC──► Kafka ──KSQLDB SQL──► high_scores / score_totals
   (the data)        (Day 2)      (highway)  (transform)    (live results)
```

You now have data moving from a database, through a streaming highway, transformed by SQL, into live results — with schemas keeping everything safe. That is a real-time data platform in miniature.

---

## What you achieved

- Built a multi-step **streaming pipeline** entirely in SQL.
- Used a **stream** (events), a derived **stream** (filtered topic), and a **table** (current state).
- Ran both **push** (live) and **pull** (instant lookup) queries.

### Deliverable for this track
Commit your `.ksql` files. In your notes: *Which parts of this pipeline are streams and which are tables, and why? How does `score_totals` here compare to the Redis leaderboard (Day 1) and the Kafka-consumer leaderboard (today's Kafka lab)?*

➡️ Back to the day plan: **[../README.md](../README.md)**

---

## ⭐ Must-learn from this topic

- **Multi-step pipeline** — stream → derived stream → aggregated table.
- **Stream vs table choice** — events vs current state, and why each fits.
- **Push & pull together** — live dashboards plus instant lookups.
- **The whole-day picture** — Postgres → CDC → Kafka → KSQLDB → live results.

### 📚 Official docs
- [ksqlDB tutorials](https://docs.confluent.io/platform/current/ksqldb/tutorials/overview.html) — more worked pipelines.
- [Aggregate a stream](https://docs.confluent.io/platform/current/ksqldb/developer-guide/aggregate-streaming-data.html) — GROUP BY & windows.
- [ksqlDB developer guide](https://docs.confluent.io/platform/current/ksqldb/developer-guide/overview.html) — building apps.
