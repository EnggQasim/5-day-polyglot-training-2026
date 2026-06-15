# Redis — Step 4: Clustering, eviction, ACLs, pipelining, Functions

Five practical topics that come up once you run Redis seriously.

---

## 1. Clustering (when one server is not enough)

A single Redis server is limited by one machine's RAM. **Redis Cluster** spreads data across many servers ("nodes").

- The key space is divided into **16384 hash slots**.
- Each key is assigned to a slot using a hash of its name. Each node owns a range of slots.
- Add more nodes → more total RAM and throughput. This is **horizontal scaling**.

You do not set up a cluster today (it needs several nodes), but know the idea: **data is sharded by key across nodes**, and the client is redirected to the node that owns a key's slot.

```
-- on a real cluster you would see:
CLUSTER INFO
CLUSTER NODES
```

---

## 2. Eviction (what happens when memory is full)

Because Redis lives in RAM, RAM can fill up. The **maxmemory** setting caps usage, and the **eviction policy** decides what to throw away when full.

```
CONFIG GET maxmemory
CONFIG GET maxmemory-policy
```

Common policies:
- `noeviction` — reject new writes when full (default; safest for a database).
- `allkeys-lru` — remove the **least recently used** keys (great for a cache).
- `allkeys-lfu` — remove the **least frequently used** keys.
- `volatile-ttl` — remove keys with the soonest expiry first.

For a **cache**, `allkeys-lru` is the usual pick: rarely used data drops out, hot data stays.

### Expiry (TTL)

You can also tell a key to delete itself after some seconds — perfect for sessions or cached results.

```
SET session:abc "user42"
EXPIRE session:abc 30        -- gone after 30 seconds
TTL session:abc              -- seconds left
```

---

## 3. ACLs (who can do what)

By default Redis is wide open. **ACLs** (Access Control Lists) let you make users with limited rights.

```
-- make a read-only user "reporter" who can only run GET and read-type commands
ACL SETUSER reporter on >report_pass ~* +@read

-- list users
ACL LIST

-- check what a user can do
ACL GETUSER reporter
```

`~*` = all keys, `+@read` = allow the "read" category of commands. This stops, say, a reporting tool from accidentally deleting data.

---

## 4. Pipelining (fewer round-trips = faster)

Normally each command is a round-trip: send → wait → reply. If you send 1,000 commands one at a time over a network, the waiting adds up. **Pipelining** sends many commands at once, then reads all replies together.

Here is a **complete, runnable** Python script (the snippet above was only the key lines). Save it and run with `python pipelining_demo.py` after activating the `.venv` from setup:

```python
import time
import redis

# 1) connect (this line is what the short snippet left out)
r = redis.Redis(host="localhost", port=6379, decode_responses=True)
r.delete("leaderboard")

# 2) WITHOUT pipelining: 1000 separate round-trips
start = time.time()
for i in range(1000):
    r.zadd("leaderboard", {f"player_{i}": i})
slow = time.time() - start
print(f"one-by-one : {slow*1000:.1f} ms")

r.delete("leaderboard")

# 3) WITH pipelining: queue all 1000, send in one round-trip
start = time.time()
pipe = r.pipeline()
for i in range(1000):
    pipe.zadd("leaderboard", {f"player_{i}": i})
pipe.execute()                 # all 1000 sent together, replies read together
fast = time.time() - start
print(f"pipelined  : {fast*1000:.1f} ms")
print(f"speed-up   : {slow/fast:.1f}x faster")
```

The two loops look almost identical; the only difference is that the pipelined version sends `pipe.zadd(...)` into a queue and fires them all at once with `pipe.execute()`. You should see the pipelined version finish several times faster, because it pays the network wait **once** instead of 1,000 times.

> This file is also saved as [`code/06_pipelining_demo.py`](code/06_pipelining_demo.py) so you can run it directly.

---

## 5. Functions (server-side logic)

Redis **Functions** let you store a small script (in Lua) on the server and call it by name. The logic runs **inside Redis**, atomically, close to the data.

The library is saved as a file, [`code/06_functions.lua`](code/06_functions.lua):

```lua
#!lua name=pq
redis.register_function('add_and_rank', function(keys, args)
  redis.call('ZINCRBY', keys[1], args[2], args[1])
  return redis.call('ZREVRANK', keys[1], args[1])
end)
```

The first line `#!lua name=pq` is required: it tells Redis the script language and names the **library** `pq`. `register_function` adds one callable function, `add_and_rank`.

### How to actually load it (this is the part that trips people up)

`FUNCTION LOAD` takes the **whole library as one argument**. Pasting multi-line Lua into `redis-cli` by hand does not work well. The reliable way is to pipe the **file** in using `redis-cli -x` (the `-x` flag reads the last argument from standard input):

```bash
docker exec -i pq_redis redis-cli -x FUNCTION LOAD REPLACE < day1/redis/code/06_functions.lua
```

It prints the library name back: `pq`. (`REPLACE` lets you load again after editing the file.)

### Call it

`FCALL` syntax is `FCALL <function> <numkeys> <keys...> <args...>`. Here there is 1 key (the sorted set), then two args (member, points):

```bash
# make a leaderboard first
docker exec -it pq_redis redis-cli ZADD leaderboard 4200 hero_07 7300 elf_mona 5100 mage_lily

# add 250 points to hero_07 and get the new rank (0 = top)
docker exec -it pq_redis redis-cli FCALL add_and_rank 1 leaderboard hero_07 250
```

So `keys[1]=leaderboard`, `args[1]=hero_07`, `args[2]=250`. The function adds the points **and** returns the new rank in a single atomic server-side step.

### Useful management commands

```bash
docker exec -it pq_redis redis-cli FUNCTION LIST     # see loaded libraries
docker exec -it pq_redis redis-cli FUNCTION DELETE pq  # remove the library
```

### Prefer Python? (no shell-quoting pain)

The script [`code/06_load_function.py`](code/06_load_function.py) loads the same file and calls the function with `r.function_load(...)` and `r.fcall(...)`:

```bash
python day1/redis/code/06_load_function.py
```

Use Functions when you want several commands to run together as one fast, **atomic** step on the server, close to the data.

**Run the admin file:** [`code/04_admin.redis`](code/04_admin.redis)

➡️ Next: the lab — **[05-lab-leaderboard.md](05-lab-leaderboard.md)**

---

## ⭐ Must-learn from this topic

- **Redis Cluster** — 16384 hash slots, sharding keys across nodes.
- **Eviction & TTL** — `maxmemory-policy` (e.g. `allkeys-lru`), `EXPIRE` / `TTL`.
- **ACLs** — `ACL SETUSER`, command categories like `+@read`.
- **Pipelining & Functions** — batching commands; server-side Lua logic.

### 📚 Official docs
- [Scaling with Redis Cluster](https://redis.io/docs/latest/operate/oss_and_stack/management/scaling/) — sharding & slots.
- [Key eviction](https://redis.io/docs/latest/develop/reference/eviction/) — maxmemory policies.
- [ACL](https://redis.io/docs/latest/operate/oss_and_stack/management/security/acl/) — users & permissions.
- [Pipelining](https://redis.io/docs/latest/develop/use/pipelining/) and [Functions](https://redis.io/docs/latest/develop/interact/programmability/functions-intro/).
