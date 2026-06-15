# Debezium — Step 3: LAB (capture player changes live)

Now the satisfying part: change a row in PostgreSQL and **watch the event appear in Kafka** — without any app publishing it.

You will need **three terminals**.

---

## Terminal 1 — watch the change topic

Read the Debezium topic from the beginning:

```bash
docker exec -it pq_broker kafka-console-consumer \
  --bootstrap-server localhost:9092 \
  --topic pq.public.players --from-beginning
```

When the connector first ran, it took a **snapshot**, so you will already see one event per existing player. Leave this running.

## Terminal 2 — change the data in PostgreSQL

Open psql and make some changes:

```bash
docker exec -it pq_postgres psql -U trainer -d pixelquest
```

```sql
-- an UPDATE
UPDATE players SET score = score + 1000 WHERE username = 'hero_07';

-- an INSERT
INSERT INTO players (username, country, score) VALUES ('newbie_max', 'PK', 100);

-- a DELETE
DELETE FROM players WHERE username = 'bard_kai';
```

## Watch Terminal 1

Within a second, new events appear. Each Debezium event describes the change. Simplified, an UPDATE looks like:

```json
{
  "op": "u",                       // c=create, u=update, d=delete, r=snapshot read
  "before": { "username": "hero_07", "score": 4300, ... },
  "after":  { "username": "hero_07", "score": 5300, ... },
  "source": { "table": "players", "lsn": 123456, "ts_ms": 1718... }
}
```

- **`op`** tells you the kind of change: `c`reate, `u`pdate, `d`elete, `r`ead (snapshot).
- **`before`** and **`after`** show the row's old and new values.
- **`source`** carries metadata (table, position in the WAL, timestamp).

So the `+1000` update, the new player, and the delete all flowed automatically from PostgreSQL into Kafka.

---

## Terminal 3 (optional) — a friendlier view in Python

`watch_changes.py` reads the same topic and prints a one-line summary per change:

```bash
python day2/debezium/code/watch_changes.py
```

Example output as you edit rows:

```
UPDATE hero_07: score 4300 -> 5300
CREATE newbie_max: score=100
DELETE bard_kai
```

---

## What you achieved

- Registered a **CDC** connector and saw PostgreSQL changes become Kafka events **automatically**.
- Read the Debezium **`op` / `before` / `after`** envelope.
- Connected Day 1 (the database) to Day 2 (the stream) with zero app changes.

### Deliverable for this track
Commit the connector JSON. In your notes, answer: *Why is CDC safer than asking every app to publish its own events? Name one thing you could keep in sync this way (e.g. a Redis cache or a search index).*

➡️ Next: **[../connectors/01-sink-connectors-intro.md](../connectors/01-sink-connectors-intro.md)**

---

## ⭐ Must-learn from this topic

- **The change envelope** — `op` (c/u/d/r), `before`, `after`, `source`.
- **Snapshot vs streaming** — `r` events on first run, then `c`/`u`/`d`.
- **End-to-end CDC** — a SQL change becomes a Kafka event with no app code.
- **Replication slot** — how Postgres tracks Debezium's read position.

### 📚 Official docs
- [Debezium event structure](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-events) — the message format.
- [Debezium tutorial](https://debezium.io/documentation/reference/stable/tutorial.html) — a full worked example.
- [PostgreSQL logical decoding](https://www.postgresql.org/docs/current/logicaldecoding.html) — what Debezium reads.
