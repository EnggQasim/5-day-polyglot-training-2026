# Redis — Step 1: What it is, and our sample data

## What is Redis?

Redis is an **in-memory data store**. "In-memory" means it keeps data in **RAM**, not on a slow disk, so reads and writes are extremely fast (microseconds). It is most often used as a **cache** (a fast layer in front of a slower database) and for **simple data structures** like lists, sets, counters, and leaderboards.

We use Redis when we need:
- **Speed above all** — show a leaderboard, a live counter, a session.
- **Simple shapes** — strings, hashes, lists, sets, sorted sets.
- **Throwaway or short-lived data** — data we can rebuild if lost (though Redis can save to disk too, as we will see).

Redis is **not** the place for complex relationships or large permanent records — that is PostgreSQL's job. Redis is the speedy specialist.

## Redis Stack

We run **Redis Stack**, which is Redis plus extra modules:
- **RediSearch** — search and secondary indexes.
- **RedisJSON** — store and query JSON documents.
- (and more)

## Our Day 1 data: the Pixel Quest leaderboard

For Redis we keep the **live leaderboard** of player scores. A leaderboard is a perfect fit for a Redis **sorted set**: every member has a score, and Redis keeps them in order automatically.

## Connect to Redis

> **First time with the terminal?** Read **[../00-setup/02-how-to-run-queries.md](../00-setup/02-how-to-run-queries.md)** — how to open a terminal, run commands step by step, and where settings live. In short: open the VS Code terminal (**Ctrl + `**), make sure the stack is up with `docker compose up -d`, then run the command below.

The database is running in Docker. Connect with `redis-cli` (an interactive prompt — type one command per line, no semicolon needed):

```bash
docker exec -it pq_redis redis-cli
```

You are now at the `127.0.0.1:6379>` prompt. Test it:

```
PING
```

It replies `PONG`. To leave, type `exit`.

## Your first commands

Redis commands are short words. Try these one by one:

```
SET welcome "hello pixel quest"
GET welcome
DEL welcome
```

- `SET key value` stores a value.
- `GET key` reads it.
- `DEL key` deletes it.

That is the whole feel of Redis: tiny, fast commands on keys.

➡️ Next: **[02-data-structures-and-modules.md](02-data-structures-and-modules.md)**

---

## ⭐ Must-learn from this topic

- **In-memory model** — why Redis is so fast, and that it can still save to disk.
- **Key naming** — the `object:id:field` convention (e.g. `player:1:name`).
- **`SET` / `GET` / `DEL`** — the simplest commands; how to use `redis-cli`.
- **Redis Stack** — Redis plus modules (RediSearch, RedisJSON).

### 📚 Official docs
- [Redis docs home](https://redis.io/docs/latest/) — start here.
- [Introduction to data types](https://redis.io/docs/latest/develop/data-types/) — the big picture.
- [Commands reference](https://redis.io/commands/) — every command, searchable.
- [redis-cli](https://redis.io/docs/latest/develop/tools/cli/) — using the command-line client.
