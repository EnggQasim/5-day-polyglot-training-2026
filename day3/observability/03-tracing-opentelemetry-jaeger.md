# Observability — Step 3: Tracing with OpenTelemetry & Jaeger

## The idea

A **trace** follows **one request** through your system and times each step. Each step is a **span**. A request to `/players/1/summary` might look like:

```
trace: GET /players/1/summary                      total 14 ms
 ├─ span: compute_summary                           12 ms
 │   ├─ span: SELECT ... players (Postgres)          8 ms
 │   └─ span: ZREVRANK (Redis)                       3 ms
 └─ span: send response                              1 ms
```

When that request is slow, the trace shows **exactly which span** ate the time. Metrics said "it's slow"; the trace says "the Postgres query is the slow part".

## The tools

- **OpenTelemetry (OTel)** — the open standard + libraries that *produce* traces from your app.
- **Jaeger** — a system that *receives, stores, and displays* traces. Our app sends traces to Jaeger using **OTLP** (the OTel wire protocol) on port 4317.

---

## Wire it up (in `app_observed.py`)

```python
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

resource = Resource.create({"service.name": "pixelquest-api"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="localhost:4317", insecure=True)))
trace.set_tracer_provider(provider)

# auto-create a span for EVERY incoming request
FastAPIInstrumentor.instrument_app(app)
```

- **`service.name`** is how your app appears in Jaeger.
- **`FastAPIInstrumentor`** automatically wraps every request in a span — no per-endpoint code needed.
- **`BatchSpanProcessor`** sends spans to Jaeger in the background.

### Add a manual span for a step you care about

Auto-instrumentation traces the request; a **manual span** lets you time a specific block:

```python
tracer = trace.get_tracer("pixelquest")

with tracer.start_as_current_span("compute_summary"):
    player, rank = await asyncio.gather(...)
```

Now `compute_summary` shows up as its own span inside the request's trace.

---

## See traces in Jaeger

```bash
cd day3/observability/code
uvicorn app_observed:app --reload --port 8000
# make some requests (another terminal):
python day3/observability/code/load.py
```

Open **http://localhost:16686** (Jaeger UI):

1. In **Service**, choose **pixelquest-api**.
2. Click **Find Traces**.
3. Click a `/players/{player_id}/summary` trace. You will see the request span with the **`compute_summary`** child span inside it, each with a duration.

> If `pixelquest-api` does not appear, make a few requests first and wait a few seconds — `BatchSpanProcessor` sends in batches.

---

## Why traces matter

Metrics show the *symptom* ("p95 latency rose"). A trace shows the *location* ("the database span is 200ms on slow requests"). Without tracing, finding which of several backend calls is slow is guesswork. With it, you click the slow trace and read the answer.

➡️ Next: **[04-logs-loki.md](04-logs-loki.md)**

---

## ⭐ Must-learn from this topic

- **Trace & span** — one request, timed step by step.
- **OpenTelemetry SDK** — TracerProvider + BatchSpanProcessor + OTLP exporter.
- **Auto + manual spans** — `FastAPIInstrumentor` plus `start_as_current_span`.
- **`service.name`** — how your app shows up in Jaeger.

### 📚 Official docs
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/) — SDK & instrumentation.
- [OTel FastAPI instrumentation](https://opentelemetry-python-contrib.readthedocs.io/en/latest/instrumentation/fastapi/fastapi.html) — auto-tracing.
- [Jaeger docs](https://www.jaegertracing.io/docs/) — receiving & viewing traces.
