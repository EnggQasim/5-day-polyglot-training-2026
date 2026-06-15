# Observability — Step 1: The three pillars

## What is observability?

**Observability** means being able to **understand what your system is doing from the outside** — especially when something goes wrong. A running API is a black box; observability puts windows in it.

The classic question is: *"the API got slow at 3pm — why?"* You cannot answer that by re-reading the code. You need data the system emitted while it ran. That data comes in **three pillars**.

## The three pillars

### 1. Metrics — *how much / how fast?* (numbers over time)

Counts and measurements sampled continuously: requests per second, error rate, response time, memory used. Metrics are small and cheap, so you keep them for a long time and **alert** on them ("error rate > 5%").

- Tool: **Prometheus** collects them, **Grafana** charts them.
- Answers: *"Is it slow? Since when? How bad?"*

### 2. Traces — *where did the time go?* (one request's journey)

A **trace** follows a **single request** as it moves through your code and out to PostgreSQL and Redis, timing each step (each step is a **span**). When one request is slow, the trace shows you *which part* was slow.

- Tool: **OpenTelemetry** produces traces, **Jaeger** displays them.
- Answers: *"For this slow request, was it the database call or the Redis call?"*

### 3. Logs — *what exactly happened?* (detailed event records)

**Logs** are text records of individual events: "player 999 not found", "created player new_star". They carry the specific details metrics and traces leave out.

- Tool: **Loki** stores them, **Grafana** searches them.
- Answers: *"What was the exact error, for which player, at 3:01pm?"*

## Why you need all three

They answer different questions, and together they tell the whole story:

```
 Metrics: "error rate spiked at 3pm"          (something is wrong, and when)
   │
   ▼
 Traces:  "slow requests spent 2s in Postgres" (which part is wrong)
   │
   ▼
 Logs:    "ERROR: connection pool exhausted"   (the exact cause)
```

You start broad (metrics), zoom to the slow request (traces), then read the detail (logs). Missing a pillar leaves a blind spot.

## What we will do

Our Day 3 app (`app_observed.py`) emits all three:
- a **`/metrics`** page for Prometheus,
- **traces** to Jaeger over OpenTelemetry,
- **logs** to Loki.

The next three lessons set up each pillar; the lab uses them together on one slow/failing request.

➡️ Next: **[02-metrics-prometheus-grafana.md](02-metrics-prometheus-grafana.md)**

---

## ⭐ Must-learn from this topic

- **Observability** — understanding a running system from the outside.
- **Metrics** — numbers over time (how much / how fast); what you alert on.
- **Traces** — one request's journey through spans (where the time went).
- **Logs** — detailed event records (what exactly happened).
- **Use all three** — start at metrics, zoom with traces, read detail in logs.

### 📚 Official docs
- [OpenTelemetry — Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/) — the three signals.
- [Prometheus overview](https://prometheus.io/docs/introduction/overview/) — metrics & alerting.
- [Grafana docs](https://grafana.com/docs/grafana/latest/) — dashboards over all three.
