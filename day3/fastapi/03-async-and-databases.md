# FastAPI — Step 3: Async and talking to databases

## What does "async" mean, and why care?

Most of an API's time is spent **waiting** — waiting for the database to answer, waiting for Redis, waiting for the network. That is **I/O-bound** work.

- **Without async (blocking):** while one request waits for PostgreSQL, the worker sits idle and **cannot serve anyone else**. 100 slow queries = a traffic jam.
- **With async:** while one request waits, the server **switches to handle other requests**. The same machine serves far more users.

The tools:
- **`async def`** marks a function that can pause and resume.
- **`await`** means "start this I/O and let others run until it finishes".
- We use **async drivers**: `asyncpg` for PostgreSQL and `redis.asyncio` for Redis.

> Async helps **I/O-bound** work (waiting on DB/network), not **CPU-bound** work (heavy math). Our API is all I/O, so it is a perfect fit.

---

## Open connections once (at startup)

Opening a new DB connection per request is slow. We open a **pool** at startup and reuse it. FastAPI's `lifespan` runs setup code before the app serves traffic and cleanup after. File: [`code/async_db.py`](code/async_db.py).

```python
from contextlib import asynccontextmanager
import asyncpg, redis.asyncio as aioredis

state = {}

@asynccontextmanager
async def lifespan(app):
    state["pg"] = await asyncpg.create_pool(
        host="localhost", port=5432,
        user="trainer", password="trainer", database="pixelquest")
    state["redis"] = aioredis.Redis(host="localhost", port=6379, decode_responses=True)
    yield                       # <-- app serves requests here
    await state["pg"].close()
    await state["redis"].aclose()

app = FastAPI(lifespan=lifespan)
```

---

## An async endpoint

Notice `async def` and `await`:

```python
@app.get("/players/{player_id}")
async def get_player(player_id: int):
    row = await state["pg"].fetchrow(
        "SELECT player_id, username, country, score FROM players WHERE player_id = $1",
        player_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    return dict(row)
```

`await ...fetchrow(...)` starts the query and lets the server handle other requests until the row comes back. Note `$1` is asyncpg's placeholder — it safely passes the value and prevents SQL injection.

---

## Doing two things at once with `asyncio.gather`

The real power: run independent I/O **concurrently**. Here we fetch a player from PostgreSQL **and** their rank from Redis at the same time, so the endpoint takes about as long as the *slower* of the two, not the sum:

```python
import asyncio

@app.get("/players/{player_id}/summary")
async def summary(player_id: int):
    player, rank = await asyncio.gather(
        state["pg"].fetchrow("SELECT username, score FROM players WHERE player_id=$1", player_id),
        _player_rank(player_id),
    )
    if player is None:
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    return {"username": player["username"], "score": player["score"], "rank": rank}
```

`asyncio.gather(a, b)` runs both and waits for both. This is the everyday async win.

---

## Run and try it

```bash
cd day3/fastapi/code
uvicorn async_db:app --reload --port 8000
```

(Day 1 stack must be up, and you must have run `pip install -r day3/requirements.txt`.)

- `GET /players/1` → reads from PostgreSQL.
- `GET /leaderboard?top=5` → reads from Redis.
- `GET /players/1/summary` → reads both **concurrently**.

➡️ Next: the lab — **[04-lab-pixelquest-api.md](04-lab-pixelquest-api.md)**

---

## ⭐ Must-learn from this topic

- **`async def` / `await`** — non-blocking I/O; why it helps I/O-bound APIs.
- **Connection pools at startup** — FastAPI `lifespan`, reuse connections.
- **Async drivers** — `asyncpg` (Postgres), `redis.asyncio` (Redis); `$1` placeholders.
- **`asyncio.gather`** — run independent I/O concurrently.

### 📚 Official docs
- [FastAPI async](https://fastapi.tiangolo.com/async/) — when and why to use async.
- [Lifespan events](https://fastapi.tiangolo.com/advanced/events/) — startup/shutdown.
- [asyncpg](https://magicstack.github.io/asyncpg/current/) and [redis-py asyncio](https://redis.readthedocs.io/en/stable/examples/asyncio_examples.html).
