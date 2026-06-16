# Day 3 screenshots — what's captured and where

Every Day 3 example now has a screenshot embedded in its lesson, right after the
matching code/command. Images live in a per-topic `images/` folder next to the
lessons (not in this folder), so each lesson links them with `images/<file>`.

## FastAPI — [`fastapi/images/`](../fastapi/images/)

Browser (Swagger `/docs`, raw JSON) and styled-terminal (`curl`, `uvicorn`) shots,
embedded across the four FastAPI lessons.

| Lesson | Images |
|--------|--------|
| [01-intro-and-first-api](../fastapi/01-intro-and-first-api.md) | `fa1-run`, `fa1-root`, `fa1-health`, `fa1-docs`, `fa1-curl` |
| [02-pydantic-and-endpoints](../fastapi/02-pydantic-and-endpoints.md) | `fa2-docs`, `fa2-exec`, `fa2-curl`, `fa2-post` |
| [03-async-and-databases](../fastapi/03-async-and-databases.md) | `fa3-run`, `fa3-docs`, `fa3-curl`, `fa3-summary`, `fa3-leaderboard` |
| [04-lab-pixelquest-api](../fastapi/04-lab-pixelquest-api.md) | `fa4-docs`, `fa4-exec`, `fa4-curl`, `fa4-summary`, `fa4-post` |

## Observability — [`observability/images/`](../observability/images/)

Captured live from the running stack (API + `load.py` generating traffic).

| Filename | URL | Embedded in |
|----------|-----|-------------|
| `prometheus-targets.png` | http://localhost:9090/targets | [02-metrics](../observability/02-metrics-prometheus-grafana.md) |
| `prometheus-rate-graph.png` | http://localhost:9090/graph | [02-metrics](../observability/02-metrics-prometheus-grafana.md) |
| `grafana-explore-metrics.png` | http://localhost:3000 → Explore → Prometheus | [02-metrics](../observability/02-metrics-prometheus-grafana.md), [05-lab](../observability/05-lab-observe-the-api.md) |
| `jaeger-trace.png` | http://localhost:16686 | [03-tracing](../observability/03-tracing-opentelemetry-jaeger.md), [05-lab](../observability/05-lab-observe-the-api.md) |
| `grafana-loki-logs.png` | http://localhost:3000 → Explore → Loki | [04-logs](../observability/04-logs-loki.md), [05-lab](../observability/05-lab-observe-the-api.md) |

The three-pillars concept lesson ([`observability/01-three-pillars.md`](../observability/01-three-pillars.md))
is theory only — no example to screenshot.

## Re-capturing

To refresh the observability shots, have the stack running with traffic, then ask
Claude (or capture by hand and overwrite the files above):

```bash
docker compose up -d                                   # Day 1 (Postgres/Redis)
docker compose -f day3/docker-compose.day3.yml up -d   # Day 3 (Prom/Grafana/Loki/Jaeger)
cd day3/observability/code && uvicorn app_observed:app --reload --port 8000   # terminal 1
python day3/observability/code/load.py                 # terminal 2 (traffic)
```

> Grafana login is `admin` / `admin`. Use PNG, keep the address bar / nav visible
> so the URL and tool are part of the evidence.
