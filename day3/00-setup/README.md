# Day 3 — Step 0: Setup (about 30 minutes)

Today we run a **FastAPI** app on your laptop, backed by the **Day 1** databases, and watched by the **Day 3** observability stack (Prometheus, Grafana, Loki, Jaeger).

---

## 1. Start the databases and the observability stack

```bash
# Day 1 databases (we use PostgreSQL + Redis today)
docker compose up -d

# Day 3 observability stack
docker compose -f day3/docker-compose.day3.yml up -d
```

Check the new containers:

```bash
docker compose -f day3/docker-compose.day3.yml ps
```

You should see `pq_prometheus`, `pq_grafana`, `pq_loki`, and `pq_jaeger`.

---

## 2. Make sure the Day 1 data exists

The API reads the `players` table and a Redis leaderboard. If you have a fresh machine, load the Day 1 seed:

```bash
docker exec -i pq_postgres psql -U trainer -d pixelquest < day1/postgresql/code/01_schema_and_seed.sql
```

---

## 3. Install the Python packages

```bash
# activate the Day 1 virtual environment
#   Windows PowerShell:  .venv\Scripts\Activate.ps1
#   WSL / Linux / macOS: source .venv/bin/activate

pip install -r day3/requirements.txt
```

---

## 4. Run the API

uvicorn imports a file as a Python module, so we **`cd` into the code folder** and run the file by name (this also avoids the folder named `fastapi` clashing with the installed `fastapi` package):

```bash
cd day3/fastapi/code
uvicorn hello:app --reload --port 8000
```

> `--reload` restarts the server when you edit the file — great while learning. `--port 8000` matches what Prometheus scrapes. Press **Ctrl+C** to stop.

Open **http://localhost:8000/docs** — FastAPI's automatic API documentation. You can call endpoints right from that page.

Each lesson tells you which file to run. The file → run-command map:

| Lesson | `cd` into | Run |
|--------|-----------|-----|
| FastAPI 1 | `day3/fastapi/code` | `uvicorn hello:app --reload --port 8000` |
| FastAPI 2 | `day3/fastapi/code` | `uvicorn models:app --reload --port 8000` |
| FastAPI 3 | `day3/fastapi/code` | `uvicorn async_db:app --reload --port 8000` |
| FastAPI lab | `day3/fastapi/code` | `uvicorn app:app --reload --port 8000` |
| Observability lab | `day3/observability/code` | `uvicorn app_observed:app --reload --port 8000` |

---

## 5. Open the dashboards

| Tool | URL | Login |
|------|-----|-------|
| FastAPI docs | http://localhost:8000/docs | — |
| Prometheus | http://localhost:9090 | — |
| Grafana | http://localhost:3000 | admin / admin |
| Jaeger | http://localhost:16686 | — |

In Grafana, the Prometheus, Loki, and Jaeger data sources are **already wired up** (we provisioned them), so you can go straight to **Explore** and pick a data source.

---

## 6. Quick check

```bash
python day3/00-setup/check_obs.py
```

Good result:

```
FastAPI app    : OK  (/docs reachable on :8000)   [start it first with uvicorn]
Prometheus     : OK  (:9090)
Grafana        : OK  (:3000)
Loki           : OK  (:3100)
Jaeger         : OK  (:16686)
```

> The FastAPI line only passes once you have started uvicorn (step 4). The other four should pass right after `docker compose up`.

---

## Connection details

| Service | From laptop | From inside Docker |
|---------|-------------|--------------------|
| FastAPI app | localhost:8000 | host.docker.internal:8000 |
| Prometheus | localhost:9090 | prometheus:9090 |
| Grafana | localhost:3000 | grafana:3000 |
| Loki (push/query) | localhost:3100 | loki:3100 |
| Jaeger UI | localhost:16686 | jaeger:16686 |
| Jaeger OTLP (traces in) | localhost:4317 | jaeger:4317 |

When everything is up, open **[`../README.md`](../README.md)** and start with FastAPI.
