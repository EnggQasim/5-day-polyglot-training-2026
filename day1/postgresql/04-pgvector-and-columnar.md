# PostgreSQL — Step 4: pgvector and columnar storage

PostgreSQL is not only for normal tables. With **extensions** it can do new tricks. We look at two: storing **vectors** (for similarity/AI search) and **columnar** storage (for analytics).

---

## Part A: pgvector — similarity search inside PostgreSQL

A **vector** is just a list of numbers, like `[0.12, 0.98, 0.55]`. In AI, text or images are turned into vectors so that **similar things have nearby numbers**. "Sword" and "blade" would have vectors close to each other.

`pgvector` adds a `vector` column type plus a way to measure distance between vectors. It is already installed in our training image.

### Turn it on and add a vector column

```sql
CREATE EXTENSION IF NOT EXISTS vector;

-- a tiny table of game items, each with a 3-number vector
DROP TABLE IF EXISTS items_vec;
CREATE TABLE items_vec (
    item_id  SERIAL PRIMARY KEY,
    name     TEXT,
    embedding vector(3)        -- 3 dimensions, to keep it readable
);

INSERT INTO items_vec (name, embedding) VALUES
    ('sword',  '[0.9, 0.1, 0.0]'),
    ('blade',  '[0.85, 0.15, 0.0]'),   -- close to sword
    ('potion', '[0.0, 0.9, 0.1]'),
    ('shield', '[0.2, 0.1, 0.9]');
```

### Ask "what is most similar to a sword?"

The `<->` operator gives the distance between two vectors. **Smaller distance = more similar.**

```sql
SELECT name, embedding <-> '[0.9, 0.1, 0.0]' AS distance
FROM items_vec
ORDER BY distance
LIMIT 3;
```

You will see `sword` (distance 0, it is itself) and `blade` right behind it, because their numbers are close. This is the same idea Milvus does at huge scale later today.

### Make it fast with an index

For big tables, add a vector index so the search does not check every row:

```sql
CREATE INDEX ON items_vec USING ivfflat (embedding vector_l2_ops) WITH (lists = 10);
```

---

## Part B: Columnar storage (for analytics)

Normal PostgreSQL stores data **row by row**. That is great when you read whole rows (one player's full record). But for **analytics** — "what is the average score across millions of players?" — you only need *one column*, and reading entire rows wastes effort.

**Columnar storage** stores each column together. Reading one column becomes very fast, and the data compresses well because similar values sit next to each other.

### What is `cstore_fdw`?

`cstore_fdw` is the classic PostgreSQL extension that adds **columnar storage**. Let's break the name down in plain words:

- **cstore** = "**c**olumnar **store**" — it keeps data column-by-column instead of row-by-row.
- **fdw** = "**F**oreign **D**ata **W**rapper". An FDW is PostgreSQL's plug-in system for storing or reading data in a *different* format or place, while still using normal SQL. `cstore_fdw` uses this mechanism to store a table's data in a special columnar file on disk instead of the usual row format.

How it actually stores data: rows are grouped into big blocks called **stripes**, and inside each stripe every column is written together and **compressed**. Two big wins follow from this:

1. **Less disk read for analytics.** If your query only needs the `score` column, PostgreSQL reads just that column's data and skips the rest. With row storage it would have to read every full row.
2. **Strong compression.** Because similar values sit next to each other (all the scores together, all the countries together), they squeeze down a lot — often 3–10× smaller on disk.

It also keeps small **min/max summaries** per stripe, so it can skip whole stripes that cannot match your filter (a trick called "skip indexes").

#### What using it looks like

> **Read, don't run:** this extension is **not** installed in our training Docker image, so the block below is to *understand the shape* of columnar tables — it is not meant to be executed today. The runnable analytics example is in the next section.

```sql
-- 1) turn on the extension and the columnar "server"
CREATE EXTENSION IF NOT EXISTS cstore_fdw;
CREATE SERVER cstore_server FOREIGN DATA WRAPPER cstore_fdw;

-- 2) create a columnar table (note FOREIGN TABLE + SERVER)
CREATE FOREIGN TABLE players_columnar (
    player_id  INTEGER,
    username   TEXT,
    country    CHAR(2),
    score      INTEGER,
    created_at DATE
)
SERVER cstore_server
OPTIONS (compression 'pglz');     -- compress the columns

-- 3) load data into it, then run analytics that read only one column
INSERT INTO players_columnar SELECT * FROM players;

SELECT country, avg(score)
FROM players_columnar
GROUP BY country;                  -- reads score + country columns only
```

The table behaves like any other table in SQL — you just get columnar speed and compression for big analytic scans.

#### An important caveat

`cstore_fdw` is the **original** columnar extension (from Citus Data). On modern PostgreSQL most teams now use its successor, **Citus columnar** (built into the `citus` extension), or reach for dedicated column databases like **DuckDB** or **ClickHouse** when analytics get really heavy. The *idea* — store by column, compress, scan less — is identical across all of them, and that idea is what matters for Day 1.

### Getting *close* to the idea without the extension: the Index Only Scan

Plain PostgreSQL cannot truly store data by column. But there is one feature that gives a *taste* of the columnar benefit — the **Index Only Scan**.

The idea: an index on `score` already contains a **copy of every score value**, on its own, sorted. So a query that needs *only* the `score` column — like `SELECT avg(score)` — can sometimes be answered **from the index alone**, without ever opening the full table rows. That is a little like columnar storage: read just the one column's data, skip the rest.

But — and this is the important honest part — **PostgreSQL only does this when it decides it is actually cheaper, and only when it is allowed to.** Two things must be true:

1. **The table must be big enough.** On a tiny table (our `players` has 12 rows) PostgreSQL will just read the whole table with a **`Seq Scan`**, because for 12 rows that is faster than going through an index. So on our small table the example below will show a `Seq Scan`, **not** an Index Only Scan. That is correct behaviour, not a bug.
2. **The visibility map must be set**, which happens after a `VACUUM`. PostgreSQL needs to know a row is visible to everyone without checking the table; `VACUUM` records that.

So let's do it properly and actually *see* an Index Only Scan, instead of just claiming it.

```sql
-- 1) a bigger table so the planner prefers an index over a full scan
DROP TABLE IF EXISTS scores_big;
CREATE TABLE scores_big (id SERIAL PRIMARY KEY, score INTEGER);
INSERT INTO scores_big (score)
SELECT (random() * 10000)::int FROM generate_series(1, 200000);   -- 200k rows

-- 2) index that holds the score values (sorted)
CREATE INDEX idx_scores_big ON scores_big (score);

-- 3) update statistics AND set the visibility map (needed for index-only scans)
VACUUM ANALYZE scores_big;

-- 4) now an aggregate over only the score column can use the index alone
EXPLAIN ANALYZE
SELECT avg(score) FROM scores_big;
```

In the plan you should now see an **`Index Only Scan using idx_scores_big`** (often with `Heap Fetches: 0`, meaning it never had to read the table rows). Compare that with the tiny table:

```sql
-- on the 12-row table, the SAME kind of query just does a Seq Scan
EXPLAIN ANALYZE
SELECT avg(score) FROM players;
```

This contrast *is* the lesson: the index-only trick only pays off at scale — exactly where real columnar storage shines too.

> **Be honest about the limits:** an Index Only Scan is **not** real columnar storage. It works for one query reading one (indexed) column, it does not compress like `cstore_fdw`, and you would need a separate index per column. For heavy multi-column analytics over millions of rows you still reach for true columnar (Citus columnar, DuckDB, ClickHouse). This is just the closest taste of the idea in plain PostgreSQL.

**Remember the trade-off:**
- **Row storage** → best for "give me this whole record" (normal apps).
- **Columnar storage** → best for "scan one column across millions of rows" (reports, analytics).

**Run the file:** [`code/04_pgvector_columnar.sql`](code/04_pgvector_columnar.sql)

➡️ Next: **[05-pgbouncer-and-explain.md](05-pgbouncer-and-explain.md)**

---

## ⭐ Must-learn from this topic

- **pgvector** — the `vector` type, distance operators `<->` (L2), `<#>` (inner product), `<=>` (cosine), and `ivfflat` / `hnsw` indexes.
- **Columnar storage idea** — store by column, compress, scan less (cstore_fdw / Citus columnar).
- **Index Only Scan** — answering a query from the index alone; needs `VACUUM` to set the visibility map.

### 📚 Official docs
- [pgvector (README)](https://github.com/pgvector/pgvector) — install, types, operators, indexes.
- [Index-Only Scans](https://www.postgresql.org/docs/current/indexes-index-only-scans.html) — the official explanation.
- [Citus columnar](https://github.com/citusdata/citus) — the modern successor to cstore_fdw.
- [cstore_fdw (archived)](https://github.com/citusdata/cstore_fdw) — the original columnar extension.
