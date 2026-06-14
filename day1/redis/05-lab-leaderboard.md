# Redis — Step 5: LAB (real-time leaderboard + AOF durability)

In this lab you will:
1. Build a **live leaderboard** with a sorted set, loaded fast using **pipelining**.
2. Store each player's profile as **JSON**.
3. Turn on **AOF**, restart Redis, and prove the data survived (durability test).

Run the Python script (needs `pip install redis` from setup):

```bash
python day1/redis/code/05_lab_leaderboard.py
```

---

## What the script does (read along)

### 1. Connect

```python
import redis
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.ping()
```

### 2. Load 1,000 players into the leaderboard with a pipeline

```python
import random
pipe = r.pipeline()
for i in range(1000):
    pipe.zadd("leaderboard", {f"player_{i}": random.randint(0, 10000)})
pipe.execute()        # one round-trip for all 1000 writes
```

### 3. Read the top 5 and a player's rank

```python
top5 = r.zrevrange("leaderboard", 0, 4, withscores=True)
rank = r.zrevrank("leaderboard", "player_0")   # 0 = first place
```

### 4. Store a profile as JSON (RedisJSON)

```python
r.execute_command(
    "JSON.SET", "profile:player_0", "$",
    '{"name":"player_0","country":"PK","level":7}'
)
profile = r.execute_command("JSON.GET", "profile:player_0")
```

### 5. Durability test (AOF)

```python
r.config_set("appendonly", "yes")           # turn AOF on
r.zadd("leaderboard", {"durable_player": 9999})
r.execute_command("BGREWRITEAOF")            # write the AOF log
```

---

## Prove durability yourself

After running the script, **restart only Redis** and check the value is still there:

```bash
docker compose restart redis
docker exec -it pq_redis redis-cli ZSCORE leaderboard durable_player
```

You should get `9999` back. Because AOF logged the change to disk, the restart did not lose it. If AOF had been off and there was no recent snapshot, the value could be gone.

---

## What you achieved

- A **leaderboard** that stays sorted automatically (sorted set).
- A fast bulk load using **pipelining**.
- **JSON** profiles stored and read.
- A real **AOF durability** test across a restart.

### Deliverable for this track
Commit `05_lab_leaderboard.py` and note in your own words: *Why is a sorted set the right structure for a leaderboard, and what would go wrong if you used a normal SQL table queried with `ORDER BY score` for millions of live players?*

➡️ Next engine: **[../neo4j/01-intro-and-data.md](../neo4j/01-intro-and-data.md)**

---

## ⭐ Must-learn from this topic

- **Sorted sets for leaderboards** — why `ZADD`/`ZREVRANGE`/`ZREVRANK` beat sorting in SQL.
- **Pipelining for bulk loads** — one round-trip instead of thousands.
- **AOF durability** — proving data survives a restart.
- **redis-py** — the Python client used in the lab.

### 📚 Official docs
- [Sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/) — the leaderboard type.
- [redis-py docs](https://redis-py.readthedocs.io/en/stable/) — the Python client.
- [Persistence](https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/) — RDB/AOF reference.
