# Observability — Step 4: Logs with Loki

## The idea

**Logs** are text records of individual events — the detail that metrics and traces leave out: *"player 999 not found"*, *"created player new_star"*, *"connection pool exhausted"*.

**Loki** is a log store from Grafana, designed to be cheap: instead of indexing every word (expensive), it indexes only a few **labels** (like `app` and `level`) and stores the log lines compressed. You then search by label + text inside **Grafana**.

```
 your app ──log lines──► Loki ──► Grafana (search & view)
            (with labels: app, level)
```

---

## How our app ships logs

Real systems usually run an agent (Promtail/Alloy) that tails container logs into Loki. To keep the training simple and dependency-light, our app **pushes** logs straight to Loki's HTTP API using a tiny handler, [`code/loki_handler.py`](code/loki_handler.py):

```python
# Loki push API: POST http://localhost:3100/loki/api/v1/push
payload = {"streams": [
    {"stream": {"app": "pixelquest-api", "level": record.levelname},
     "values": [[str(time.time_ns()), line]]}
]}
requests.post(url, json=payload, timeout=2)
```

`get_logger()` returns a logger that prints to the console **and** ships to Loki. The handler is **fail-safe**: if Loki is down, logging silently continues (logging must never crash the app).

In `app_observed.py` we just log normally:

```python
log = get_logger("pixelquest")
log.info("served player %s", player_id)
log.warning("player %s not found", player_id)
```

> The labels matter: we label each line with `app=pixelquest-api` and `level=INFO/WARNING`. You search by those labels in Grafana — keep labels few and low-cardinality (don't label by player id!).

---

## Generate some logs

```bash
cd day3/observability/code
uvicorn app_observed:app --reload --port 8000
# in another terminal, create traffic incl. 404s:
python day3/observability/code/load.py
```

The 404 requests produce `WARNING player ... not found` lines; successful ones produce `INFO` lines.

---

## View logs in Grafana (Loki)

Open **http://localhost:3000** → **Explore** → choose the **Loki** data source.

Try these **LogQL** queries (Loki's query language):

```logql
{app="pixelquest-api"}
```

```logql
# only warnings (our 404s)
{app="pixelquest-api", level="WARNING"}
```

```logql
# text search within the app's logs
{app="pixelquest-api"} |= "not found"
```

- `{label="value"}` selects a log stream by label.
- `|= "text"` keeps only lines containing that text.

You will see your API's log lines, filterable by level and text — exactly what you want when chasing a specific failure.

---

## The three pillars together

You now have all three: **metrics** (Prometheus/Grafana), **traces** (Jaeger), **logs** (Loki). The lab uses them as a team to diagnose one request.

➡️ Next: the lab — **[05-lab-observe-the-api.md](05-lab-observe-the-api.md)**

---

## ⭐ Must-learn from this topic

- **Logs** — detailed event records; the "what exactly happened".
- **Loki labels** — index a few low-cardinality labels (`app`, `level`), not every word.
- **Shipping logs** — push API (here) or an agent (Promtail/Alloy) in production.
- **LogQL** — `{app="..."}`, filter with `|= "text"`.

### 📚 Official docs
- [Loki docs](https://grafana.com/docs/loki/latest/) — store & query logs.
- [LogQL](https://grafana.com/docs/loki/latest/query/) — the query language.
- [Loki HTTP API (push)](https://grafana.com/docs/loki/latest/reference/loki-http-api/) — the endpoint we use.
