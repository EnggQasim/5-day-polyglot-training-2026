"""
A small STATELESS Pixel Quest API for Day 5 deployment.

No database — it serves an in-memory leaderboard. That keeps the focus on
Kubernetes, Helm, scaling, and load testing (not on data stores).

Endpoints:
  GET /health        -> liveness/readiness probe target
  GET /players       -> the in-memory leaderboard
  GET /work?n=10000  -> burns a little CPU (so load tests can trigger autoscaling)
"""
import os
from fastapi import FastAPI

app = FastAPI(title="Pixel Quest API (stateless, k8s)")

PLAYERS = [
    {"rank": 1, "player": "elf_mona", "score": 7300},
    {"rank": 2, "player": "ninja_sara", "score": 6700},
    {"rank": 3, "player": "giant_sam", "score": 6200},
    {"rank": 4, "player": "knight_max", "score": 5600},
    {"rank": 5, "player": "mage_lily", "score": 5100},
]

# which pod answered (handy to SEE load spread across replicas)
POD = os.environ.get("HOSTNAME", "local")


@app.get("/health")
def health():
    return {"status": "ok", "pod": POD}


@app.get("/players")
def players():
    return {"pod": POD, "leaderboard": PLAYERS}


@app.get("/work")
def work(n: int = 10000):
    # a tiny CPU burn so load tests raise CPU and the autoscaler reacts
    total = 0
    for i in range(n):
        total += i * i
    return {"pod": POD, "n": n, "result": total}
