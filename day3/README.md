# Day 3 — APIs, Async & Observability

**Goal:** Put a real **web API** in front of our data, make it **async** (fast under load), and then **see inside it** using the three pillars of observability: **metrics** (Prometheus + Grafana), **traces** (OpenTelemetry + Jaeger), and **logs** (Loki).

> **How we teach here (same as Days 1–2):** easy English, one idea at a time, explanation → a small example with our **Pixel Quest** data → the exact code/command to run → what to expect. Folder per topic, runnable code, and a **⭐ Must-learn + 📚 Official docs** box at the end of every lesson.

---

## The big picture

On Day 1 we stored data; on Day 2 we streamed it. But people and other systems need a **front door** to read and write it — that is an **API**. Today we build that door with **FastAPI**, make it **async** so it serves many users at once, and then add **observability** so that when something is slow or broken, we can actually find out *why*.

```
   Browser / app
        │  HTTP
        ▼
   FastAPI service (async)  ──►  PostgreSQL (players)   [Day 1]
        │                   └─►  Redis (leaderboard)    [Day 1]
        │
        ├── /metrics ──► Prometheus ──► Grafana   (how much / how fast?)
        ├── traces  ──► Jaeger                    (where did the time go?)
        └── logs    ──► Loki ──► Grafana          (what exactly happened?)
```

We reuse the Day 1 PostgreSQL `players` table and Redis. The API exposes them; the observability stack watches the API.

---

## What you will learn

| Topic | What it does | Pixel Quest example |
|-------|--------------|---------------------|
| **FastAPI** | a modern Python web API framework | `GET /players`, `GET /leaderboard` |
| **Async** | handle many requests without blocking | query Postgres + Redis at the same time |
| **Metrics (Prometheus/Grafana)** | numbers over time | requests/sec, latency, error rate |
| **Traces (OpenTelemetry/Jaeger)** | follow one request through the code | API → Postgres → Redis timing |
| **Logs (Loki)** | searchable event records | "player 12 not found" |

---

## Before you start

Day 3 reuses **Day 1 PostgreSQL and Redis**, and adds the observability stack.

1. Make sure Day 1 is up (from the repo top folder):
   ```bash
   docker compose up -d
   ```
2. Start the Day 3 observability stack:
   ```bash
   docker compose -f day3/docker-compose.day3.yml up -d
   ```
3. Follow **[`00-setup/README.md`](00-setup/README.md)** to install the Python packages and run the API.

> New to the terminal? The Day 1 guide still applies: **[../day1/00-setup/02-how-to-run-queries.md](../day1/00-setup/02-how-to-run-queries.md)**.

---

## Suggested schedule

**Setup (first 30 min)** — start Day 1 + the observability stack, install packages, run the API, open the dashboards.

**Morning — Concepts**
- FastAPI: endpoints, Pydantic models, automatic docs.
- Async: `async`/`await`, async database drivers, doing work concurrently.
- Observability: the three pillars (metrics, traces, logs) and why you need all three.

**Afternoon — Labs**
- Build the Pixel Quest API over the Day 1 stores.
- Instrument it: metrics on a Grafana dashboard, a request trace in Jaeger, logs searchable in Loki.

---

## Lessons in order

### 0. Setup
- [`00-setup/README.md`](00-setup/README.md) — start the stack, install packages, run the API, open the UIs.

### 1. FastAPI — the front door
1. [Intro & your first API](fastapi/01-intro-and-first-api.md)
2. [Pydantic models & endpoints](fastapi/02-pydantic-and-endpoints.md)
3. [Async & talking to databases](fastapi/03-async-and-databases.md)
4. [LAB: the Pixel Quest API](fastapi/04-lab-pixelquest-api.md)

### 2. Observability — seeing inside
1. [The three pillars](observability/01-three-pillars.md)
2. [Metrics with Prometheus & Grafana](observability/02-metrics-prometheus-grafana.md)
3. [Tracing with OpenTelemetry & Jaeger](observability/03-tracing-opentelemetry-jaeger.md)
4. [Logs with Loki](observability/04-logs-loki.md)
5. [LAB: observe the API end to end](observability/05-lab-observe-the-api.md)

---

## The web UIs you will use today

| Tool | URL | Login |
|------|-----|-------|
| FastAPI docs (Swagger) | http://localhost:8000/docs | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin |
| Jaeger | http://localhost:16686 | — |

---

## End-of-day result (deliverable)

Commit your API code and a short `notes.md`: *Why does async help an I/O-bound API? Which pillar (metrics, traces, or logs) would you reach for first to answer "the API got slow at 3pm — why?", and why?*

## When you finish, stop the stack

```bash
docker compose -f day3/docker-compose.day3.yml down
```
