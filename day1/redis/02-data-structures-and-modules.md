# Redis — Step 2: Data structures and modules

Redis is famous for its **data structures**. Each one solves a common problem. Let's meet the main ones using Pixel Quest data. Run these in `redis-cli`.

---

## Strings (and counters)

The simplest type. Also great as a fast counter.

```
SET player:1:name "hero_07"
GET player:1:name

SET visits 0
INCR visits          -- now 1
INCR visits          -- now 2
INCRBY visits 10     -- now 12
```

`INCR` is **atomic**: even with thousands of users hitting it at once, no count is lost. Perfect for "page views" or "coins spent".

> **Naming tip:** Redis has no tables. People use `:` in key names to fake a structure, like `player:1:name`. It is just a naming habit, but a very useful one.

---

## Hashes (a small record)

A hash stores **fields** under one key — like one row of a table.

```
HSET player:1 name "hero_07" country "PK" score 4200
HGET player:1 score
HGETALL player:1
HINCRBY player:1 score 100      -- add 100 to the score field
```

Use a hash when you want to keep related fields together under one key.

---

## Lists (ordered, like a queue)

```
RPUSH recent_logins hero_07     -- push to the right end
RPUSH recent_logins mage_lily
RPUSH recent_logins ninja_sara
LRANGE recent_logins 0 -1       -- show all (0 to last)
LPOP recent_logins              -- remove from the left
```

Lists are great for queues and "most recent N" feeds.

---

## Sets (unique members, no order)

```
SADD online_players hero_07 mage_lily ninja_sara
SADD online_players hero_07       -- duplicate ignored
SMEMBERS online_players
SISMEMBER online_players hero_07  -- 1 = yes, 0 = no
SCARD online_players              -- how many online
```

Sets answer "is this member present?" and "who is in both sets?" very fast.

---

## Sorted Sets (the leaderboard!)

A sorted set is a set where every member has a **score**, and Redis keeps them **sorted by that score**. This is exactly a leaderboard.

```
ZADD leaderboard 4200 hero_07
ZADD leaderboard 5100 mage_lily
ZADD leaderboard 6700 ninja_sara
ZADD leaderboard 7300 elf_mona

-- top 3 players, highest first
ZREVRANGE leaderboard 0 2 WITHSCORES

-- what rank is hero_07? (0 = top). REV = highest score is rank 0
ZREVRANK leaderboard hero_07

-- player just scored 500 more points
ZINCRBY leaderboard 500 hero_07
```

No sorting code needed — Redis maintains the order for you, instantly. This is why game leaderboards almost always use Redis.

---

## RedisJSON (a JSON document)

With the RedisJSON module you can store and update JSON directly.

```
JSON.SET item:sword $ '{"name":"sword","price":100,"tags":["weapon","metal"]}'
JSON.GET item:sword
JSON.GET item:sword $.price
JSON.SET item:sword $.price 120     -- change just the price
```

`$` means "the root of the document"; `$.price` points at one field.

---

## RediSearch (search and indexes)

RediSearch lets you build an index and search across many keys.

```
-- build an index over hashes whose keys start with "item:"
FT.CREATE idx:items ON HASH PREFIX 1 item: SCHEMA name TEXT price NUMERIC

HSET item:1 name "fire sword" price 150
HSET item:2 name "ice shield" price 90
HSET item:3 name "fire potion" price 30

-- search for items containing the word "fire"
FT.SEARCH idx:items "fire"

-- search with a price filter
FT.SEARCH idx:items "@price:[0 100]"
```

This turns Redis into a fast search engine for your cached data.

**Run the file:** [`code/02_data_structures.redis`](code/02_data_structures.redis) with:
```bash
docker exec -i pq_redis redis-cli < day1/redis/code/02_data_structures.redis
```

➡️ Next: **[03-persistence-rdb-aof.md](03-persistence-rdb-aof.md)**

---

## ⭐ Must-learn from this topic

- **Strings & counters** — `SET`/`GET`, atomic `INCR`/`INCRBY`.
- **Hashes** — `HSET`/`HGETALL`/`HINCRBY` (one record under one key).
- **Lists / Sets / Sorted Sets** — `RPUSH`/`LRANGE`, `SADD`/`SMEMBERS`, and the leaderboard trio `ZADD`/`ZREVRANGE`/`ZINCRBY`.
- **RedisJSON & RediSearch** — `JSON.SET`/`JSON.GET`, `FT.CREATE`/`FT.SEARCH`.

### 📚 Official docs
- [Data types](https://redis.io/docs/latest/develop/data-types/) — strings, hashes, lists, sets.
- [Sorted sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/) — the leaderboard type.
- [JSON](https://redis.io/docs/latest/develop/data-types/json/) — RedisJSON.
- [Search and query](https://redis.io/docs/latest/develop/interact/search-and-query/) — RediSearch indexes.
