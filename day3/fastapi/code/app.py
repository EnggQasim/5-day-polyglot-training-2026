"""
FastAPI LAB: the Pixel Quest API over the Day 1 databases.

Endpoints:
  GET  /players                 list players (optional ?country=PK)
  GET  /players/{id}            one player
  GET  /players/{id}/summary    player + their leaderboard rank (concurrent reads)
  GET  /leaderboard?top=5       top N from the Redis leaderboard
  POST /players                 add a player (writes to Postgres + leaderboard)

Run:
    cd day3/fastapi/code
    uvicorn app:app --reload --port 8000
"""
import asyncio
from contextlib import asynccontextmanager

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["pg"] = await asyncpg.create_pool(
        host="localhost", port=5432,
        user="trainer", password="trainer", database="pixelquest",
    )
    state["redis"] = aioredis.Redis(host="localhost", port=6379, decode_responses=True)
    rows = await state["pg"].fetch("SELECT username, score FROM players")
    if rows:
        await state["redis"].zadd("api_leaderboard",
                                  {r["username"]: r["score"] for r in rows})
    yield
    await state["pg"].close()
    await state["redis"].aclose()


app = FastAPI(title="Pixel Quest API", lifespan=lifespan)


class NewPlayer(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    country: str = Field(min_length=2, max_length=2)
    score: int = Field(default=0, ge=0)


@app.get("/players")
async def list_players(country: str | None = None):
    if country:
        rows = await state["pg"].fetch(
            "SELECT player_id, username, country, score FROM players "
            "WHERE country = $1 ORDER BY score DESC", country)
    else:
        rows = await state["pg"].fetch(
            "SELECT player_id, username, country, score FROM players ORDER BY score DESC")
    return [dict(r) for r in rows]


@app.get("/players/{player_id}")
async def get_player(player_id: int):
    row = await state["pg"].fetchrow(
        "SELECT player_id, username, country, score FROM players WHERE player_id = $1",
        player_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    return dict(row)


@app.get("/players/{player_id}/summary")
async def summary(player_id: int):
    player, rank = await asyncio.gather(
        state["pg"].fetchrow(
            "SELECT username, score FROM players WHERE player_id = $1", player_id),
        _player_rank(player_id),
    )
    if player is None:
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    return {"username": player["username"], "score": player["score"], "rank": rank}


@app.get("/leaderboard")
async def leaderboard(top: int = 5):
    rows = await state["redis"].zrevrange("api_leaderboard", 0, top - 1, withscores=True)
    return [{"rank": i + 1, "player": m, "score": int(s)} for i, (m, s) in enumerate(rows)]


@app.post("/players", status_code=201)
async def create_player(new: NewPlayer):
    try:
        row = await state["pg"].fetchrow(
            "INSERT INTO players (username, country, score) VALUES ($1, $2, $3) "
            "RETURNING player_id, username, country, score",
            new.username, new.country, new.score)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409, detail="username already exists")
    await state["redis"].zadd("api_leaderboard", {new.username: new.score})
    return dict(row)


async def _player_rank(player_id: int):
    row = await state["pg"].fetchrow(
        "SELECT username FROM players WHERE player_id = $1", player_id)
    if row is None:
        return None
    rank = await state["redis"].zrevrank("api_leaderboard", row["username"])
    return None if rank is None else rank + 1
