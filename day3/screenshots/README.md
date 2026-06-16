# Day 3 screenshots — capture & placement guide

This folder holds screenshots of the running Day 3 stack. Each image is embedded
in a lesson right after the matching example.

**Two ways to fill it:**
- **Claude captures them** — connect Chrome with the Claude extension, make sure the
  app + load generator are running, and ask Claude to capture. Claude will take each
  shot and embed it in the lesson automatically.
- **You capture them** — take the screenshots yourself, save each with the exact
  filename below into this folder, and Claude will embed them.

Before capturing, have these running so the UIs show real data:
```bash
docker compose up -d                                   # Day 1 (Postgres/Redis)
docker compose -f day3/docker-compose.day3.yml up -d   # Day 3 (Prom/Grafana/Loki/Jaeger)
cd day3/observability/code && uvicorn app_observed:app --reload --port 8000   # terminal 1
python day3/observability/code/load.py                 # terminal 2 (traffic)
```

## Shot list

| # | Filename | URL | What to show | Goes in lesson |
|---|----------|-----|--------------|----------------|
| 1 | `fastapi-docs.png` | http://localhost:8000/docs | The Swagger page listing all endpoints | `fastapi/01-intro-and-first-api.md` (after "Try it") |
| 2 | `fastapi-try-summary.png` | http://localhost:8000/docs | `GET /players/{id}/summary` expanded, after **Execute**, showing the JSON response | `fastapi/04-lab-pixelquest-api.md` (after the curl block) |
| 3 | `prometheus-targets.png` | http://localhost:9090/targets | The `pixelquest-api` target showing **UP** | `observability/02-metrics-prometheus-grafana.md` (after "Check Prometheus") |
| 4 | `prometheus-rate-graph.png` | http://localhost:9090/graph | Graph tab with `rate(http_requests_total[1m])` plotted | `observability/02-...` (after the PromQL block) |
| 5 | `grafana-explore-metrics.png` | http://localhost:3000 → Explore → Prometheus | The same rate query charted in Grafana | `observability/02-...` (after "Chart it in Grafana") |
| 6 | `jaeger-trace.png` | http://localhost:16686 | A `/players/{id}/summary` trace expanded, showing the `compute_summary` span | `observability/03-tracing-opentelemetry-jaeger.md` (after "See traces in Jaeger") |
| 7 | `grafana-loki-logs.png` | http://localhost:3000 → Explore → Loki | `{app="pixelquest-api", level="WARNING"}` results | `observability/04-logs-loki.md` (after "View logs in Grafana") |

> Use PNG, full-window, light or dark theme is fine. Keep the browser address bar
> visible so the URL/port is part of the evidence.

Once the files are here (named exactly as above), Claude inserts each as
`![caption](../screenshots/<filename>)` at the noted spot.
