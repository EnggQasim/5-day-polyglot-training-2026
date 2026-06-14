# PostgreSQL — Step 1: What it is, and our sample data

## What is PostgreSQL?

PostgreSQL (say "post-gres") is a **relational database**. "Relational" means data is stored in **tables** — rows and columns, like a spreadsheet. Each table has a fixed set of columns, and each row is one record.

We use a relational database when:
- The data has a clear shape (every player has a name, a country, a score).
- We care about **correctness**: money, orders, accounts. A change either fully happens or not at all.
- We want to **join** tables together (e.g. players and their purchases).

PostgreSQL is the "core" database in our training. The other three (Redis, Neo4j, Milvus) are *specialists*; PostgreSQL is the reliable all-rounder.

## Our Day 1 data: Pixel Quest players

All Day 1 lessons use a tiny make-believe game called **Pixel Quest**. For PostgreSQL we store the **players**.

Each player has:

| Column | Meaning | Example |
|--------|---------|---------|
| `player_id` | unique number for the player | 1 |
| `username` | their name in the game | `hero_07` |
| `country` | 2-letter country code | `PK` |
| `score` | total points | 4200 |
| `created_at` | when they joined | 2026-01-05 |

## Connect to PostgreSQL

> **First time with the terminal?** Read **[../00-setup/02-how-to-run-queries.md](../00-setup/02-how-to-run-queries.md)** — it shows how to open a terminal, run queries step by step, and where settings live. In short: open VS Code → **Terminal → New Terminal** (or press **Ctrl + `**), make sure the databases are up with `docker compose up -d`, then run the command below.

The database is already running in Docker (from `docker compose up -d`). Connect with the `psql` client (this opens an interactive prompt where you type one query at a time, ending each with `;`):

```bash
docker exec -it pq_postgres psql -U trainer -d pixelquest
```

You are now at the `pixelquest=#` prompt. To leave, type `\q`.

> If you have `psql` installed on your laptop you can also run:
> `psql "postgresql://trainer:trainer@localhost:5432/pixelquest"`

## Create the table and add data

Run the script that builds the `players` table and inserts 12 sample rows:

```bash
docker exec -i pq_postgres psql -U trainer -d pixelquest < day1/postgresql/code/01_schema_and_seed.sql
```

> `docker exec -i ... < file.sql` means: take the SQL file from your laptop and feed it into psql inside the container.

Now check it worked. Open psql again and run:

```sql
SELECT player_id, username, country, score FROM players ORDER BY score DESC;
```

You should see 12 players, highest score first.

## What just happened

- `CREATE TABLE` defined the shape (columns and their types).
- `INSERT` added rows.
- `SELECT ... ORDER BY` read the rows back, sorted.

This is the foundation. Every later PostgreSQL lesson builds on this `players` table.

➡️ Next: **[02-mvcc-and-concurrency.md](02-mvcc-and-concurrency.md)** — how PostgreSQL lets many people change data at the same time without breaking.

---

## ⭐ Must-learn from this topic

- **`CREATE TABLE`** — columns, data types, `PRIMARY KEY`, `UNIQUE`, `NOT NULL`, `DEFAULT`.
- **`INSERT INTO` and `SELECT ... WHERE ... ORDER BY`** — the everyday read/write commands.
- **Foreign keys (`REFERENCES`) and `JOIN`** — how tables link together.
- **`psql` basics** — connecting, and meta-commands: `\q` (quit), `\dt` (list tables), `\d players` (describe a table).

### 📚 Official docs
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html) — gentle start.
- [Data Types](https://www.postgresql.org/docs/current/datatype.html) — every column type.
- [SELECT](https://www.postgresql.org/docs/current/sql-select.html) — the full query syntax.
- [psql reference](https://www.postgresql.org/docs/current/app-psql.html) — the client and its `\` commands.
