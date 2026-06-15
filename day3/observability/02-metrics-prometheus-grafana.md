# Observability — Step 2: Metrics with Prometheus & Grafana

## The idea

**Metrics** are numbers measured over time. The standard open-source setup is:
- Your app exposes a **`/metrics`** page (plain text numbers).
- **Prometheus** *pulls* (scrapes) that page every few seconds and stores the numbers.
- **Grafana** charts them.

This is a **pull** model: Prometheus reaches out to your app on a schedule (we set 5s in `prometheus/prometheus.yml`).

---

## Add metrics to FastAPI (one line)

We use `prometheus-fastapi-instrumentator`. In [`code/app_observed.py`](code/app_observed.py):

```python
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)    # adds a /metrics endpoint
```

That automatically tracks request **count**, **latency**, and **status codes** for every endpoint. We also add a **custom metric**:

```python
from prometheus_client import Counter
players_created = Counter("pq_players_created_total", "Players created via the API")
# ... and in the POST handler:
players_created.inc()
```

---

## Run everything

```bash
# 1) the observed app
cd day3/observability/code
uvicorn app_observed:app --reload --port 8000

# 2) (new terminal) generate traffic
python day3/observability/code/load.py
```

Look at the raw metrics yourself: open **http://localhost:8000/metrics**. You will see lines like:

```
http_requests_total{handler="/players/{player_id}",method="GET",status="2xx"} 37.0
pq_players_created_total 2.0
```

These are the numbers Prometheus scrapes.

---

## Check Prometheus

Open **http://localhost:9090**.

- Go to **Status → Targets**: `pixelquest-api` should be **UP** (Prometheus is successfully scraping your app via `host.docker.internal:8000`).
- Go to the **Graph** tab and try a query (this is **PromQL**, Prometheus's query language):

```promql
# requests per second per endpoint, averaged over the last minute
rate(http_requests_total[1m])
```

```promql
# 95th percentile latency
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))
```

`rate(...[1m])` turns an ever-growing counter into a per-second rate — the most common PromQL pattern.

---

## Chart it in Grafana

Open **http://localhost:3000** (admin / admin). The **Prometheus** data source is already connected.

1. Left menu → **Explore**.
2. Pick the **Prometheus** data source.
3. Enter `rate(http_requests_total[1m])` and run it. You will see request rate per endpoint climb as `load.py` runs.
4. Try the latency query too.

> From Explore you can click **Add to dashboard** to save a panel. A few panels — request rate, error rate, p95 latency — make a basic service dashboard.

**Key takeaway:** metrics tell you **how much** and **how fast**, and they are what you **alert** on. But they do not tell you *why* a single request was slow — that is the next pillar.

➡️ Next: **[03-tracing-opentelemetry-jaeger.md](03-tracing-opentelemetry-jaeger.md)**

---

## ⭐ Must-learn from this topic

- **Pull model** — your app exposes `/metrics`; Prometheus scrapes it.
- **Instrumentation** — `Instrumentator().instrument(app).expose(app)`; custom `Counter`.
- **PromQL** — `rate(counter[1m])`, `histogram_quantile(...)` for latency.
- **Grafana Explore** — chart a PromQL query, save to a dashboard.

### 📚 Official docs
- [Prometheus — Getting started](https://prometheus.io/docs/prometheus/latest/getting_started/) and [Querying basics (PromQL)](https://prometheus.io/docs/prometheus/latest/querying/basics/).
- [prometheus-fastapi-instrumentator](https://github.com/trallnag/prometheus-fastapi-instrumentator) — the library used.
- [prometheus-client (Python)](https://prometheus.github.io/client_python/) — custom metrics.
