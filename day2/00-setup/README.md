# Day 2 — Step 0: Setup (about 30 minutes)

Today we add the **streaming stack** on top of Day 1. The new pieces (Kafka, Schema Registry, Kafka Connect with Debezium, KSQLDB) all run in Docker, just like Day 1.

Do these steps in order.

---

## 1. Start both stacks

The Day 2 Debezium connector needs the **Day 1 PostgreSQL** running, so start Day 1 first, then Day 2. From the repo top folder:

```bash
# Day 1 databases (PostgreSQL is the one we need today)
docker compose up -d

# Day 2 streaming stack
docker compose -f day2/docker-compose.day2.yml up -d
```

Check the streaming containers:

```bash
docker compose -f day2/docker-compose.day2.yml ps
```

You should see `pq_zookeeper`, `pq_broker`, `pq_schema_registry`, `pq_connect`, and `pq_ksqldb`. The first download is large (a few GB) — be patient.

> **Memory note:** the Kafka stack is JVM-based and uses a lot of RAM on top of Day 1. On a 32 GB machine you are fine. If it gets heavy, stop Day 1 services you are not using today (e.g. `docker compose stop milvus neo4j`).

> **Apple Silicon / ARM:** Confluent images run best on Intel. On an ARM Mac you may see a `platform (linux/amd64) does not match` warning and slower start-up under emulation; it still works for this training. (Our Intel HP EliteBooks are unaffected.)

---

## 2. Enable logical replication in PostgreSQL (needed for CDC)

Debezium reads PostgreSQL's **WAL** (write-ahead log) using *logical* decoding. We must turn that on once.

```bash
# set the two required settings
docker exec pq_postgres psql -U trainer -d pixelquest -c "ALTER SYSTEM SET wal_level = logical;"

# restart Postgres so the change takes effect
docker restart pq_postgres
```

Confirm it worked:

```bash
docker exec pq_postgres psql -U trainer -d pixelquest -c "SHOW wal_level;"
```

It should print `logical`. (This is the same logical-replication idea you met in Day 1, lesson 03 — now we use it for real.)

---

## 3. Install the Python client libraries

We reuse the Day 1 virtual environment and add the streaming clients.

```bash
# activate the venv made on Day 1
#   Windows PowerShell:  .venv\Scripts\Activate.ps1
#   WSL / Linux / macOS: source .venv/bin/activate

pip install confluent-kafka requests
```

- `confluent-kafka` — produce and consume Kafka messages from Python.
- `requests` — call the Connect, Schema Registry, and KSQLDB REST APIs.

(For the Avro lab we will add `"confluent-kafka[avro]"` then.)

---

## 4. Test every service

Run the checker:

```bash
python day2/00-setup/check_stream.py
```

A good result:

```
Kafka broker     : OK  (localhost:9092 reachable)
Schema Registry  : OK  (HTTP 200 from :8081)
Kafka Connect    : OK  (Debezium plugin present)
KSQLDB           : OK  (server is RUNNING)
All good. You are ready for Day 2.
```

If something fails, wait a minute (the JVM services take time to boot) and run again.

---

## Connection details (write these down)

| Service | From your laptop | From inside Docker | Web/REST |
|---------|------------------|--------------------|----------|
| Kafka broker | localhost:9092 | broker:29092 | — |
| Schema Registry | localhost:8081 | schema-registry:8081 | http://localhost:8081/subjects |
| Kafka Connect | localhost:8083 | connect:8083 | http://localhost:8083/connectors |
| KSQLDB | localhost:8088 | ksqldb-server:8088 | http://localhost:8088/info |
| PostgreSQL (Day 1) | localhost:5432 | host.docker.internal:5432 | — |

> **Why `host.docker.internal` for Postgres?** The Day 1 and Day 2 stacks are separate Docker projects on different networks. `host.docker.internal` lets the Day 2 Connect container reach the Day 1 Postgres through your laptop. This works on Docker Desktop (Windows/Mac). On plain Linux, add `extra_hosts: ["host.docker.internal:host-gateway"]` to the `connect` service.

When everything passes, open **[`../README.md`](../README.md)** and start with Kafka.
