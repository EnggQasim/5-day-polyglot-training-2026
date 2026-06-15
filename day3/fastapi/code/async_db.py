"""
Async FastAPI that talks to the Day 1 databases:
  - PostgreSQL (players) via asyncpg
  - Redis (leaderboard) via redis.asyncio

It also shows doing two queries CONCURRENTLY with asyncio.gather.

Run:
    cd day3/fastapi/code
    uvicorn async_db:app --reload --port 8000

Needs: Day 1 stack up, and `pip install -r day3/requirements.txt`.
"""
import asyncio
from contextlib import asynccontextmanager

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException

# connections are created once at startup and reused (a pool)
state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup: open a Postgres pool and a Redis client
    state["pg"] = await asyncpg.create_pool(
        host="localhost", port=5432,
        user="trainer", password="trainer", database="pixelquest",
    )
    state["redis"] = aioredis.Redis(host="localhost", port=6379, decode_responses=True)

    # seed a small Redis leaderboard from the players table (once)
    rows = await state["pg"].fetch("SELECT username, score FROM players")
    if rows:
        await state["redis"].zadd("api_leaderboard",
                                  {r["username"]: r["score"] for r in rows})
    yield
    # shutdown: close connections
    await state["pg"].close()
    await state["redis"].aclose()


app = FastAPI(title="Pixel Quest API - async", lifespan=lifespan)


@app.get("/players/{player_id}")
async def get_player(player_id: int):
    row = await state["pg"].fetchrow(
        "SELECT player_id, username, country, score FROM players WHERE player_id = $1",
        player_id,
    )
    if row is None:
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    return dict(row)


@app.get("/leaderboard")
async def leaderboard(top: int = 5):
    # Redis returns [(member, score), ...] highest first
    rows = await state["redis"].zrevrange("api_leaderboard", 0, top - 1, withscores=True)
    return [{"rank": i + 1, "player": m, "score": int(s)} for i, (m, s) in enumerate(rows)]


@app.get("/players/{player_id}/summary")
async def summary(player_id: int):
    # run the DB read and the Redis read AT THE SAME TIME with gather
    player_task = state["pg"].fetchrow(
        "SELECT username, score FROM players WHERE player_id = $1", player_id)
    rank_task = _player_rank(player_id)
    player, rank = await asyncio.gather(player_task, rank_task)
    if player is None:
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    return {"username": player["username"], "score": player["score"], "rank": rank}


async def _player_rank(player_id: int):
    row = await state["pg"].fetchrow(
        "SELECT username FROM players WHERE player_id = $1", player_id)
    if row is None:
        return None
    rank = await state["redis"].zrevrank("api_leaderboard", row["username"])
    return None if rank is None else rank + 1
