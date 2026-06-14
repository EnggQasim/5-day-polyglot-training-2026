# PostgreSQL — Step 3: Replication and Partitioning (growing big)

When a database grows — more users, more data — we need two things: **copies** (so we don't lose data and can spread out reads) and **smaller pieces** (so big tables stay fast). These are **replication** and **partitioning**.

---

## Part A: Logical Replication (making copies)

**Replication** means one database (the **publisher**) sends its changes to another database (the **subscriber**), so the second one stays in sync.

There are two kinds:
- **Physical replication:** copies the whole database byte-for-byte. Good for a full standby backup.
- **Logical replication:** copies **chosen tables** as a stream of row changes (insert/update/delete). More flexible — you can copy just the `players` table to another server, even a different PostgreSQL version.

Day 2 of this course uses the *same idea* (change-data-capture with Debezium) to feed Kafka. So understanding logical replication now helps later.

### How it looks (you do not need two servers to understand the commands)

On the **source** database you create a *publication* — a named set of tables to share:

```sql
-- share all changes to the players table
CREATE PUBLICATION players_pub FOR TABLE players;
```

On the **second** database you create a *subscription* that connects and pulls those changes:

```sql
-- (run on a SECOND postgres) - just to show the shape of the command
CREATE SUBSCRIPTION players_sub
  CONNECTION 'host=source_host dbname=pixelquest user=trainer password=trainer'
  PUBLICATION players_pub;
```

From then on, every insert/update/delete on `players` in the source automatically appears in the subscriber.

> Logical replication needs the setting `wal_level = logical`. Our training image already allows it. You can check with:
> ```sql
> SHOW wal_level;
> ```

**Key point to remember:** replication = automatic copying of changes. It gives you backups, read-only copies for reports, and the foundation for streaming data to other systems.

---

## Part B: Partitioning (splitting a big table)

Imagine the `purchases` table grows to 100 million rows. Searching it gets slow. **Partitioning** splits one logical table into smaller physical pieces, usually **by date**. PostgreSQL automatically sends each query to the right piece.

### Create a partitioned purchases table

```sql
-- a parent table, partitioned by month using the bought_at date
CREATE TABLE purchases_part (
    purchase_id SERIAL,
    player_id   INTEGER NOT NULL,
    item        TEXT NOT NULL,
    coins       INTEGER NOT NULL,
    bought_at   DATE NOT NULL
) PARTITION BY RANGE (bought_at);

-- one child partition per month
CREATE TABLE purchases_2026_02 PARTITION OF purchases_part
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');

CREATE TABLE purchases_2026_03 PARTITION OF purchases_part
    FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
```

Now insert rows — PostgreSQL puts each into the correct monthly partition automatically:

```sql
INSERT INTO purchases_part (player_id, item, coins, bought_at) VALUES
    (1, 'sword',  100, '2026-02-10'),
    (4, 'potion', 20,  '2026-03-04');
```

### See partition pruning (the speed win)

When you filter by date, PostgreSQL only scans the matching partition — it **prunes** (skips) the rest:

```sql
EXPLAIN
SELECT * FROM purchases_part WHERE bought_at = '2026-03-04';
```

Look at the plan: it only touches `purchases_2026_03`, not the February partition. With 100 million rows spread across months, skipping irrelevant partitions is a huge speed-up.

**Run the file:** [`code/03_replication_partitioning.sql`](code/03_replication_partitioning.sql)

➡️ Next: **[04-pgvector-and-columnar.md](04-pgvector-and-columnar.md)**

---

## ⭐ Must-learn from this topic

- **Logical vs physical replication** — and `wal_level = logical`, `PUBLICATION` / `SUBSCRIPTION`.
- **Table partitioning** — `PARTITION BY RANGE/LIST/HASH` and creating child partitions.
- **Partition pruning** — how filtering by the partition key skips irrelevant partitions.
- **WAL (Write-Ahead Log)** — the basis of both replication and crash recovery.

### 📚 Official docs
- [Logical Replication](https://www.postgresql.org/docs/current/logical-replication.html) — publications & subscriptions.
- [Table Partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html) — the full guide.
- [High Availability & Replication](https://www.postgresql.org/docs/current/high-availability.html) — overview of options.
- [Write-Ahead Logging (WAL)](https://www.postgresql.org/docs/current/wal-intro.html) — what the WAL is.
