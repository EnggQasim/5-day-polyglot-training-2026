# PostgreSQL — Step 5: Connection pooling and reading query plans

Two skills every PostgreSQL user needs: handling **lots of connections** (PgBouncer) and understanding **why a query is slow** (`EXPLAIN ANALYZE`).

---

## Part A: Connection pooling with PgBouncer

Every connection to PostgreSQL costs memory (each one is a small process on the server). If 5,000 web users each open a connection, the server runs out of memory and slows down.

**PgBouncer** sits **in front of** PostgreSQL. Your app connects to PgBouncer; PgBouncer keeps a small **pool** of real connections to PostgreSQL and shares them. 5,000 app connections might use only 20 real database connections.

```
   App 1 ┐
   App 2 ┤
   ...   ├──►  PgBouncer  ──►  PostgreSQL (small pool of real connections)
   App N ┘   (a pool)
```

A typical PgBouncer config looks like this (you do not need to run it today — just read it):

```ini
[databases]
pixelquest = host=postgres port=5432 dbname=pixelquest

[pgbouncer]
listen_port = 6432
pool_mode = transaction      ; reuse a connection after each transaction
max_client_conn = 5000       ; how many apps can connect to pgbouncer
default_pool_size = 20       ; real connections to postgres per database
```

**Pool modes (most to least sharing):**
- `transaction` — a real connection is borrowed for one transaction, then returned. Best for web apps.
- `session` — one real connection per client session.
- `statement` — returned after every single statement (rarely used).

**Key point:** PgBouncer lets a small database serve a huge number of users. We will see why this matters on Day 5 when k6 throws 5,000 concurrent users at the system.

---

## Part B: EXPLAIN ANALYZE (why is my query slow?)

### First, what is a "query plan"?

When you send SQL like `SELECT * FROM players WHERE username = 'elf_mona'`, you only say **what** you want, not **how** to get it. PostgreSQL's **planner** decides the *how*: should it read the whole table? use an index? in what order should it join tables? That step-by-step recipe is the **query plan**.

`EXPLAIN` is how you **see that recipe**.

### EXPLAIN vs EXPLAIN ANALYZE (the key difference)

- **`EXPLAIN`** — shows the plan and the planner's **estimates**, but does **not run** the query. Fast and safe.
- **`EXPLAIN ANALYZE`** — actually **runs** the query and shows the plan with **real measured numbers** (time taken, rows actually seen). More truthful, but it really executes the query.

> ⚠️ Because `EXPLAIN ANALYZE` *runs* the query, be careful with `INSERT`, `UPDATE`, or `DELETE` — it will really change your data. To measure those safely, wrap them in a transaction you roll back:
> ```sql
> BEGIN;
> EXPLAIN ANALYZE DELETE FROM players WHERE score < 0;
> ROLLBACK;   -- undo it; you still get the timings
> ```

This is the **number-one tool for tuning**: it tells you exactly why a query is fast or slow.

### Searching the small table

```sql
EXPLAIN ANALYZE
SELECT * FROM players WHERE username = 'elf_mona';
```

You will see a **`Seq Scan`** — a *sequential scan*, meaning PostgreSQL read **every row** to find the match. The plan looks like this:

```
Seq Scan on players  (cost=0.00..1.15 rows=1 width=25) ...
  Filter: (username = 'elf_mona'::text)
  Rows Removed by Filter: 11
```

### Important: adding an index does NOT change this on a tiny table

You might expect that creating an index makes PostgreSQL switch to an Index Scan. **It will not — not here.** Try it:

```sql
CREATE INDEX IF NOT EXISTS idx_players_username ON players (username);
ANALYZE players;

EXPLAIN ANALYZE
SELECT * FROM players WHERE username = 'elf_mona';
```

You will **still see a `Seq Scan`.** That is correct, not a bug. With only 12 rows, reading the whole table (`cost=0.00..1.15`) is *cheaper* than jumping through an index, so the planner ignores the index on purpose. PostgreSQL always picks the plan it thinks is cheapest for the data it actually has.

> Note: if you run `CREATE INDEX` without `IF NOT EXISTS` and the index already exists, you get `ERROR: relation "idx_players_username" already exists`. Use `IF NOT EXISTS`, or drop it first with `DROP INDEX idx_players_username;`.

### Now actually SEE an Index Scan (on a big table)

The index only wins when the table is big enough that scanning all rows would be slow. Let's build one and watch the planner switch.

```sql
-- 200k players, so a full scan is genuinely expensive
DROP TABLE IF EXISTS players_big;
CREATE TABLE players_big (id SERIAL PRIMARY KEY, username TEXT);
INSERT INTO players_big (username)
SELECT 'player_' || g FROM generate_series(1, 200000) AS g;

-- no index yet: this is a Seq Scan over 200k rows
EXPLAIN ANALYZE
SELECT * FROM players_big WHERE username = 'player_150000';

-- add the index and refresh statistics
CREATE INDEX idx_players_big_username ON players_big (username);
ANALYZE players_big;

-- now the planner switches to an Index Scan
EXPLAIN ANALYZE
SELECT * FROM players_big WHERE username = 'player_150000';
```

On the 200k-row table the second plan shows an **`Index Scan using idx_players_big_username`** — PostgreSQL jumps straight to the row instead of reading all 200,000. *This* is the contrast the lesson is about: an index helps when the table is large, and the planner is smart enough to skip it when it would not.

### How to read the output (line by line)

A real `EXPLAIN ANALYZE` line looks like this:

```
Index Scan using idx_players_username on players
  (cost=0.28..8.29 rows=1 width=40)
  (actual time=0.025..0.027 rows=1 loops=1)
Planning Time: 0.110 ms
Execution Time: 0.052 ms
```

Read it piece by piece:

- **`Index Scan using idx_players_username on players`** — the **operation** (the "node"). Here PostgreSQL used the index `idx_players_username` on the `players` table. This is the *how*.
- **`cost=0.28..8.29`** — the planner's **estimate** in arbitrary units (not seconds). The first number (`0.28`) is the cost to return the *first* row; the second (`8.29`) is the cost to return *all* rows. Lower = cheaper. Use it to compare plans, not as a real-world time.
- **`rows=1`** (inside `cost=...`) — how many rows the planner **expected**.
- **`width=40`** — estimated average row size in bytes.
- **`actual time=0.025..0.027`** — the **real** time in milliseconds (only shown with `ANALYZE`): time to first row .. time to last row.
- **`rows=1 loops=1`** (inside `actual time=...`) — how many rows it **really** got, and how many times this step ran.
- **`Planning Time`** — how long it took to *build* the plan.
- **`Execution Time`** — how long it took to actually *run* the query. This is the number you usually care about most.

#### The single most useful check: estimated vs actual rows

Compare the `rows=` in the **cost** part (estimate) with the `rows=` in the **actual** part (reality).

- Close numbers → the planner understands your data, so it is choosing good plans.
- Very different (e.g. estimate `rows=1` but actual `rows=50000`) → the planner's **statistics are stale**, and it may be picking bad plans. Refresh them with:
  ```sql
  ANALYZE players;     -- updates the table's statistics
  ```

#### Common operations you will see

- **`Seq Scan`** (sequential scan) — reads **every row** in the table. Fine for tiny tables, a red flag on big ones when you filtered on a column.
- **`Index Scan`** — jumps to matching rows using an index. Usually good.
- **`Index Only Scan`** — answers the query from the index alone, without touching the table. Even better.
- **`Bitmap Heap Scan`** — a middle ground used when many rows match: it gathers matches from the index first, then reads them in disk order.
- **`Nested Loop` / `Hash Join` / `Merge Join`** — the three ways PostgreSQL combines two tables in a `JOIN`.
- **`Sort`**, **`Aggregate`**, **`Limit`** — extra steps for `ORDER BY`, `avg()/count()`, and `LIMIT`.

#### How to read the tree shape

Plans are a **tree**, shown with indentation. **The most indented lines run first**, and their results feed the lines above them. So to follow what happens, read from the **deepest/innermost** node **outward to the top**.

> **Tip:** `EXPLAIN (ANALYZE, BUFFERS)` adds how much data came from memory (cache) vs disk — useful when a query is slow because it is reading from disk a lot.

### Rule of thumb

If a frequent query does a `Seq Scan` on a large table and filters on a column, that column probably needs an **index**. But do not index everything — indexes speed up reads and slow down writes, and use disk.

**Run the file:** [`code/05_explain.sql`](code/05_explain.sql)

➡️ Next: the hands-on lab — **[06-lab-timescale-vector-knn.md](06-lab-timescale-vector-knn.md)**

---

## ⭐ Must-learn from this topic

- **PgBouncer pooling** — `pool_mode` (transaction / session / statement), `default_pool_size`, `max_client_conn`.
- **`EXPLAIN` vs `EXPLAIN ANALYZE`** — estimates vs real measured execution.
- **Reading a plan** — `Seq Scan` vs `Index Scan`, `cost`, `actual time`, estimated vs actual `rows`, `BUFFERS`.
- **`ANALYZE`** — keeping the planner's statistics fresh so it picks good plans.

### 📚 Official docs
- [PgBouncer](https://www.pgbouncer.org/) and its [config reference](https://www.pgbouncer.org/config.html).
- [Using EXPLAIN](https://www.postgresql.org/docs/current/using-explain.html) — how to read query plans.
- [EXPLAIN command](https://www.postgresql.org/docs/current/sql-explain.html) — all options (ANALYZE, BUFFERS…).
- [Indexes](https://www.postgresql.org/docs/current/indexes.html) — index types and when they help.
