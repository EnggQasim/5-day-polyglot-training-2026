# Debezium — Step 2: Register a PostgreSQL connector

A connector is configured with a small **JSON** document and registered by POSTing it to Kafka Connect's REST API (port 8083). Let's understand the config, then register it.

---

## The connector config

Here is our connector (also saved as [`code/players-connector.json`](code/players-connector.json)):

```json
{
  "name": "pq-players-connector",
  "config": {
    "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
    "tasks.max": "1",
    "database.hostname": "host.docker.internal",
    "database.port": "5432",
    "database.user": "trainer",
    "database.password": "trainer",
    "database.dbname": "pixelquest",
    "topic.prefix": "pq",
    "table.include.list": "public.players",
    "plugin.name": "pgoutput",
    "slot.name": "pq_slot",
    "publication.autocreate.mode": "filtered"
  }
}
```

What each line means, in plain words:

- **`connector.class`** — use Debezium's PostgreSQL connector.
- **`database.hostname: host.docker.internal`** — reach the Day 1 Postgres through your laptop (the two stacks are on different Docker networks; see setup).
- **`database.user/password/dbname`** — the Day 1 credentials.
- **`topic.prefix: pq`** — every change topic starts with `pq.`. The `players` table becomes the topic **`pq.public.players`**.
- **`table.include.list: public.players`** — only watch this one table.
- **`plugin.name: pgoutput`** — use PostgreSQL's built-in logical decoding (no extra install).
- **`slot.name`** — a *replication slot*; PostgreSQL uses it to remember how far Debezium has read.
- **`publication.autocreate.mode: filtered`** — let Debezium create the publication for just the included tables.

---

## Register it

POST the JSON to Kafka Connect. With `curl`:

```bash
curl -i -X POST http://localhost:8083/connectors \
  -H "Content-Type: application/json" \
  -d @day2/debezium/code/players-connector.json
```

A `201 Created` (or `409` if it already exists) means success.

> No `curl`? Use the Python helper instead: `python day2/debezium/code/register_connector.py`.

---

## Check it is running

```bash
# list connectors
curl http://localhost:8083/connectors

# check status of ours (look for "state": "RUNNING")
curl http://localhost:8083/connectors/pq-players-connector/status
```

When Debezium first connects, it takes a **snapshot**: it reads the current rows of `players` and emits them as events, so consumers start with the full picture. After the snapshot, it streams only new changes.

## See the topic appear

```bash
docker exec -it pq_broker kafka-topics --bootstrap-server localhost:9092 --list
```

You should now see **`pq.public.players`** in the list — created automatically by Debezium.

---

## Managing the connector

```bash
# pause / resume
curl -X PUT http://localhost:8083/connectors/pq-players-connector/pause
curl -X PUT http://localhost:8083/connectors/pq-players-connector/resume

# delete (also frees the replication slot after a moment)
curl -X DELETE http://localhost:8083/connectors/pq-players-connector
```

➡️ Next: the lab — **[03-lab-capture-player-changes.md](03-lab-capture-player-changes.md)**

---

## ⭐ Must-learn from this topic

- **Connector config** — `connector.class`, `database.*`, `topic.prefix`, `table.include.list`, `plugin.name`, `slot.name`.
- **Connect REST API** — POST to register, GET `/status`, PUT pause/resume, DELETE.
- **Topic naming** — `<topic.prefix>.<schema>.<table>` (here `pq.public.players`).
- **Snapshot then stream** — initial rows first, then live changes.

### 📚 Official docs
- [PostgreSQL connector properties](https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-connector-properties) — every config option.
- [Kafka Connect REST API](https://docs.confluent.io/platform/current/connect/references/restapi.html) — register/manage connectors.
- [Logical decoding plug-ins](https://debezium.io/documentation/reference/stable/postgres-plugins.html) — `pgoutput` & others.
