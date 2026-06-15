"""
The Pixel Quest API, fully instrumented with the three pillars:
  - METRICS : Prometheus (/metrics), scraped by the Day 3 Prometheus.
  - TRACES  : OpenTelemetry -> Jaeger (OTLP on localhost:4317).
  - LOGS    : structured logs shipped to Loki (and printed to the console).

Run:
    cd day3/observability/code
    uvicorn app_observed:app --reload --port 8000

Needs: Day 1 stack + Day 3 observability stack up, and
       pip install -r day3/requirements.txt
"""
import asyncio
from contextlib import asynccontextmanager

import asyncpg
import redis.asyncio as aioredis
from fastapi import FastAPI, HTTPException
from prometheus_client import Counter
from prometheus_fastapi_instrumentator import Instrumentator

# ---- OpenTelemetry tracing setup ----
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from loki_handler import get_logger

# logger that prints AND ships to Loki
log = get_logger("pixelquest")

# trace provider -> export spans to Jaeger via OTLP gRPC
_resource = Resource.create({"service.name": "pixelquest-api"})
_provider = TracerProvider(resource=_resource)
_provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317", insecure=True))
)
trace.set_tracer_provider(_provider)
tracer = trace.get_tracer("pixelquest")

# a custom metric: how many players were created
players_created = Counter("pq_players_created_total", "Players created via the API")

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["pg"] = await asyncpg.create_pool(
        host="localhost", port=5432,
        user="trainer", password="trainer", database="pixelquest")
    state["redis"] = aioredis.Redis(host="localhost", port=6379, decode_responses=True)
    rows = await state["pg"].fetch("SELECT username, score FROM players")
    if rows:
        await state["redis"].zadd("api_leaderboard",
                                  {r["username"]: r["score"] for r in rows})
    log.info("startup complete: connected to postgres and redis")
    yield
    await state["pg"].close()
    await state["redis"].aclose()
    log.info("shutdown complete")


app = FastAPI(title="Pixel Quest API (observed)", lifespan=lifespan)

# add /metrics for Prometheus, and auto-trace every request to Jaeger
Instrumentator().instrument(app).expose(app)
FastAPIInstrumentor.instrument_app(app)


@app.get("/players/{player_id}")
async def get_player(player_id: int):
    row = await state["pg"].fetchrow(
        "SELECT player_id, username, country, score FROM players WHERE player_id = $1",
        player_id)
    if row is None:
        log.warning("player %s not found", player_id)
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    log.info("served player %s", player_id)
    return dict(row)


@app.get("/players/{player_id}/summary")
async def summary(player_id: int):
    # a manual child span so we can SEE this step in the Jaeger trace
    with tracer.start_as_current_span("compute_summary"):
        player, rank = await asyncio.gather(
            state["pg"].fetchrow(
                "SELECT username, score FROM players WHERE player_id = $1", player_id),
            _player_rank(player_id),
        )
    if player is None:
        log.warning("summary: player %s not found", player_id)
        raise HTTPException(status_code=404, detail=f"player {player_id} not found")
    log.info("served summary for player %s (rank %s)", player_id, rank)
    return {"username": player["username"], "score": player["score"], "rank": rank}


@app.get("/leaderboard")
async def leaderboard(top: int = 5):
    rows = await state["redis"].zrevrange("api_leaderboard", 0, top - 1, withscores=True)
    return [{"rank": i + 1, "player": m, "score": int(s)} for i, (m, s) in enumerate(rows)]


@app.post("/players", status_code=201)
async def create_player(new: dict):
    username, country, score = new["username"], new["country"], int(new.get("score", 0))
    try:
        row = await state["pg"].fetchrow(
            "INSERT INTO players (username, country, score) VALUES ($1, $2, $3) "
            "RETURNING player_id, username, country, score", username, country, score)
    except asyncpg.UniqueViolationError:
        raise HTTPException(status_code=409, detail="username already exists")
    await state["redis"].zadd("api_leaderboard", {username: score})
    players_created.inc()                       # bump the custom metric
    log.info("created player %s", username)
    return dict(row)


async def _player_rank(player_id: int):
    row = await state["pg"].fetchrow(
        "SELECT username FROM players WHERE player_id = $1", player_id)
    if row is None:
        return None
    rank = await state["redis"].zrevrank("api_leaderboard", row["username"])
    return None if rank is None else rank + 1
