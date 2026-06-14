# PostgreSQL — Step 2: MVCC (how many users change data at once)

## The problem

Imagine two game admins open the same player at the same time. Admin A adds 100 points. Admin B adds 50 points. If they both save, what happens? Will one change be lost? Will one admin see half-finished data from the other?

PostgreSQL solves this with **MVCC** = **Multi-Version Concurrency Control**.

## The simple idea

Instead of locking a row and making everyone wait, PostgreSQL keeps **multiple versions** of a row.

- When you change a row, PostgreSQL does **not** overwrite it. It writes a **new version** and marks the old one as outdated.
- Every transaction sees a **snapshot**: the version of the data as it was when the transaction started.
- Readers never block writers, and writers never block readers. They just see different versions.

Think of it like a document with "track changes" on: the old text is still there until the changes are accepted and cleaned up.

## See it with your own eyes

Each row secretly carries two hidden columns: `xmin` (the transaction that created this version) and `xmax` (the transaction that deleted/replaced it). Let's look.

```sql
-- the hidden columns are normally invisible; ask for them by name
SELECT player_id, username, score, xmin, xmax
FROM players
WHERE username = 'hero_07';
```

Now update the score and look again:

```sql
UPDATE players SET score = score + 100 WHERE username = 'hero_07';

SELECT player_id, username, score, xmin, xmax
FROM players
WHERE username = 'hero_07';
```

Notice `xmin` changed — this is a **new version** of the row, created by your update.

## Two sessions at once (the real demo)

Open **two** psql windows side by side.

**Window 1:**
```sql
BEGIN;                                   -- start a transaction
UPDATE players SET score = 9999 WHERE username = 'hero_07';
-- do NOT commit yet
```

**Window 2** (while Window 1 is still open):
```sql
SELECT username, score FROM players WHERE username = 'hero_07';
```

Window 2 still shows the **old** score, not 9999. That is because Window 1 has not committed — its new version is private to it. This is MVCC: Window 2 sees a consistent snapshot.

Now in **Window 1**:
```sql
COMMIT;
```

Run the SELECT in Window 2 again — now it shows 9999.

## VACUUM: cleaning up old versions

Because updates leave behind dead old versions, PostgreSQL must clean them up. This is called **VACUUM**. It runs automatically (autovacuum), but you can run it by hand:

```sql
VACUUM (VERBOSE) players;
```

Old, no-longer-needed row versions are removed and the space is reused. If you never vacuumed, the table would slowly fill with dead rows ("bloat").

## Why this matters

MVCC is why PostgreSQL handles thousands of users smoothly. You get **isolation** (each transaction sees a clean snapshot) without everyone waiting in a queue.

**Run the demo file:** [`code/02_mvcc_demo.sql`](code/02_mvcc_demo.sql)

➡️ Next: **[03-replication-and-partitioning.md](03-replication-and-partitioning.md)**

---

## ⭐ Must-learn from this topic

- **MVCC & snapshots** — why readers and writers do not block each other; the hidden `xmin`/`xmax`.
- **Transactions** — `BEGIN`, `COMMIT`, `ROLLBACK`.
- **Isolation levels** — Read Committed (default), Repeatable Read, Serializable.
- **VACUUM / autovacuum** — cleaning dead row versions and avoiding table "bloat".

### 📚 Official docs
- [Concurrency Control (MVCC)](https://www.postgresql.org/docs/current/mvcc.html) — the core chapter.
- [Transaction Isolation](https://www.postgresql.org/docs/current/transaction-iso.html) — what each level guarantees.
- [Routine Vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html) — why and how VACUUM runs.
- [VACUUM command](https://www.postgresql.org/docs/current/sql-vacuum.html) — the syntax.
