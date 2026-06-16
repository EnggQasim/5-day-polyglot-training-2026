# Load Testing — Step 1: Intro to k6

## What is load testing, and what is k6?

**Load testing** means sending lots of simulated traffic at your service to answer: *How fast is it under load? At what point does it break? Does it scale?* You can't know your system handles 5,000 users until you try.

**k6** is an open-source load-testing tool from Grafana. You write the test in **JavaScript**, run it from the command line, and it reports response times, requests/second, and error rates. It's scriptable, fast, and great in a closed environment (a single binary, no SaaS required).

## Key words

- **VU (Virtual User)** — one simulated user looping through your script. 5,000 VUs ≈ 5,000 concurrent users.
- **Iteration** — one run of your test function by a VU.
- **Stages** — a schedule that ramps VUs up and down over time.
- **Thresholds** — pass/fail rules (e.g. "95% of requests under 500ms"); if violated, k6 exits non-zero (great for CI).
- **Metrics** — k6's output: `http_req_duration` (latency), `http_reqs` (throughput), `http_req_failed` (error rate).

## A tiny test

[`code/smoke.js`](code/smoke.js) — one VU for 30 seconds, just to confirm everything works:

```js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = { vus: 1, duration: "30s" };
const BASE = __ENV.BASE_URL || "http://localhost:8080";

export default function () {
  const res = http.get(`${BASE}/players`);
  check(res, { "status is 200": (r) => r.status === 200 });
  sleep(1);
}
```

- **`options`** controls the run (here 1 VU, 30s).
- **`export default function`** is what each VU runs repeatedly.
- **`check`** records pass/fail assertions (doesn't stop the test, just reports).
- **`__ENV.BASE_URL`** lets you point the test at any URL without editing the file.

## Point it at the deployed app and run

Expose the in-cluster service to your laptop, then run k6 against it:

```bash
# terminal 1: make the service reachable at localhost:8080
kubectl port-forward svc/pixelquest 8080:80      # or svc/pq-pixelquest if installed via Helm

# terminal 2: run the smoke test
k6 run day5/loadtest/code/smoke.js
```

Read the summary: `http_req_duration` (look at `avg` and `p(95)`), `http_reqs` (throughput), `checks` (% passed). If the smoke test is green, you're ready to turn up the load.

➡️ Next: **[02-writing-tests.md](02-writing-tests.md)**

---

## ⭐ Must-learn from this topic

- **k6** — scriptable, CLI load testing in JavaScript.
- **VU / iteration** — a virtual user looping your test function.
- **`options` / `check` / `__ENV`** — configure the run, assert, parameterize.
- **Reach the app** — `kubectl port-forward` then point k6 at it.

### 📚 Official docs
- [k6 — Get started](https://grafana.com/docs/k6/latest/get-started/running-k6/) — first test.
- [Checks](https://grafana.com/docs/k6/latest/using-k6/checks/) — assertions.
- [HTTP requests](https://grafana.com/docs/k6/latest/using-k6/http-requests/) — the `http` module.
