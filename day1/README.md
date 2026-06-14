# Day 1 — Polyglot Persistence

**Goal:** Master the four storage engines and understand *when each is the right tool* — relational (PostgreSQL), cache (Redis), graph (Neo4j), and vector (Milvus).

By the end of today you can explain **why** you would pick each database, and you have run real queries and labs against all four — all using one small make-believe dataset, the **Pixel Quest** online game.

---

## The one idea of Day 1

There is no single "best" database. Each engine is shaped for a different job:

| Engine | Best at | Pixel Quest example | The question it answers |
|--------|---------|---------------------|--------------------------|
| **PostgreSQL** | structured records, transactions, joins | player accounts & purchases | "Give me this player's full record." |
| **Redis** | speed, simple structures, caching | live score leaderboard | "Who are the top 10 right now?" |
| **Neo4j** | relationships & connections | who is friends with whom | "Who are the friends of my friends?" |
| **Milvus** | similarity search over vectors | item embeddings | "Which items are most *similar* to this one?" |

Choosing the right one (or combining several — *polyglot persistence*) is the skill of Day 1.

---

## Before you start

1. Install the foundation software (see the main [`../README.md`](../README.md)). Docker is the key one.
2. From the repo top folder, start all databases:
   ```bash
   docker compose up -d
   ```
3. Do the setup and connection checks: **[`00-setup/README.md`](00-setup/README.md)**.

---

## Suggested schedule

**Setup (first 30 min)** — start the Docker stack, confirm runtimes (Python, Node), Git, and verify connectivity to every service.

**Morning — Concepts**
- PostgreSQL: MVCC, replication & partitioning, pgvector & columnar, PgBouncer & EXPLAIN.
- Redis: data structures & modules, RDB vs AOF, clustering, eviction, ACLs, pipelining, Functions.
- Neo4j: property-graph modeling, Cypher, indexes, GDS, APOC, multi-DB/HA.
- Milvus: collections, metadata, IVF-PQ indexing, `load_collection`.

**Afternoon — Labs (one per engine)**
- PostgreSQL: TimescaleDB hypertable + vector column + K-NN.
- Redis: real-time leaderboard (sorted sets + JSON) + AOF durability test.
- Neo4j: load a CSV, run PageRank, add indexes.
- Milvus: ingest 50k 128-dim vectors, build IVF-PQ, benchmark 100 searches.

---

## Lessons in order

### 0. Setup
- [`00-setup/README.md`](00-setup/README.md) — start the stack, test every connection.
- [`00-setup/02-how-to-run-queries.md`](00-setup/02-how-to-run-queries.md) — **beginner guide:** open a terminal, the 3 ways to run queries, and where config settings live. Read this if the terminal is new to you.

### 1. PostgreSQL — relational core
1. [Intro & sample data](postgresql/01-intro-and-data.md)
2. [MVCC & concurrency](postgresql/02-mvcc-and-concurrency.md)
3. [Replication & partitioning](postgresql/03-replication-and-partitioning.md)
4. [pgvector & columnar storage](postgresql/04-pgvector-and-columnar.md)
5. [PgBouncer & EXPLAIN ANALYZE](postgresql/05-pgbouncer-and-explain.md)
6. [LAB: TimescaleDB + vector + K-NN](postgresql/06-lab-timescale-vector-knn.md)

### 2. Redis — cache & data structures
1. [Intro & sample data](redis/01-intro-and-data.md)
2. [Data structures & modules](redis/02-data-structures-and-modules.md)
3. [Persistence: RDB vs AOF](redis/03-persistence-rdb-aof.md)
4. [Clustering, eviction, ACLs, pipelining, Functions](redis/04-clustering-eviction-acl.md)
5. [LAB: leaderboard + AOF durability](redis/05-lab-leaderboard.md)

### 3. Neo4j — graph
1. [Intro & sample data](neo4j/01-intro-and-data.md)
2. [Modeling & Cypher](neo4j/02-modeling-and-cypher.md)
3. [Indexes, GDS, APOC, multi-DB/HA](neo4j/03-indexes-gds-apoc.md)
4. [LAB: load CSV + PageRank + indexes](neo4j/04-lab-pagerank.md)

### 4. Milvus — vector
1. [Intro & sample data](milvus/01-intro-and-data.md)
2. [Collections & IVF-PQ indexing](milvus/02-collections-and-indexing.md)
3. [LAB: 50k vectors + benchmark](milvus/03-lab-vector-search.md)

---

## How each lesson is built

Every lesson follows the same easy pattern: **plain explanation → small example with Pixel Quest data → the exact code/query to run → what output to expect.** Each engine folder has:
- numbered `.md` lessons (read in order),
- a `code/` folder with runnable files,
- a `data/` folder with sample data or a generator.

---

## End-of-day result (deliverable)

Commit your work for each store (SQL / Redis / Cypher / Python scripts) plus a short `notes.md` with your performance numbers and your answers to the "deliverable" questions at the end of each lab. The big takeaway to write down in your own words:

> *Given a new feature, how do I decide which database to use — and when is it worth using more than one?*

---

## When you finish, stop the stack to free memory

```bash
docker compose down
```
