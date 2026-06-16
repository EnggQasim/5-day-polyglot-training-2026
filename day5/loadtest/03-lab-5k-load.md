# Load Testing — Step 3: LAB (5,000 concurrent users)

The finale: ramp k6 to **5,000 virtual users** against the deployed API and watch Kubernetes autoscale to cope. Script: [`code/stress_5k.js`](code/stress_5k.js).

> **Reality check:** generating 5,000 VUs from one laptop strains the *client* too, and a one-node minikube has limited CPU. The goal is to **see the system scale and read the numbers**, not to set a record. If your machine struggles, lower the target in the script (e.g. 1000) — every concept still applies. In production you'd run k6 distributed or in the cloud.

---

## Step 1 — make sure the pieces are in place

```bash
# image built + deployed (k8s lab) and metrics-server on
kubectl get deploy pixelquest          # exists
kubectl get hpa pixelquest             # the HPA from the autoscale lesson
# if the HPA isn't applied yet:
kubectl apply -f day5/autoscale/code/hpa.yaml
```

Expose the service:

```bash
kubectl port-forward svc/pixelquest 8080:80     # terminal 1
```

## Step 2 — watch the cluster while the test runs

Open two watchers:

```bash
kubectl get hpa -w        # terminal 2: CPU% and replica count
kubectl get pods -w       # terminal 3: pods being added/removed
```

## Step 3 — run the 5k stress test

```bash
k6 run day5/loadtest/code/stress_5k.js          # terminal 4
```

The script ramps `0 → 1000 → 5000`, holds at 5,000, then ramps down. While it holds:
- **HPA terminal:** CPU shoots above the 50% target; `REPLICAS` climbs toward `maxReplicas` (10).
- **Pods terminal:** new `pixelquest` pods appear and become Ready; the Service spreads load across them.

## Step 4 — read the result

When k6 finishes it prints a summary. Note these for your deliverable:

- **`http_reqs` ... `/s`** — requests per second (throughput).
- **`http_req_duration` `p(95)`** and `max` — tail latency under load.
- **`http_req_failed`** — error rate.
- **Threshold lines** — each shows ✓ (met) or ✗ (breached).

A few minutes after the test ends, watch the HPA **scale back down** to `minReplicas` (2) as CPU falls — the cool-down.

## Step 5 — interpret it

- If p95 stayed under target and errors were low → the autoscaled service handled the load.
- If latency spiked or errors rose at peak → you hit the ceiling of a one-node cluster. That's a *real* finding: you'd raise `maxReplicas`, add nodes, give Pods more CPU, or optimize the endpoint.

---

## What you achieved — and the whole course

- Drove **5,000 VUs** with k6 and read p95 / RPS / error-rate.
- Watched the **HPA** autoscale Pods up under load and back down after.
- Closed the loop: **store (Day 1) → stream (Day 2) → API + observe (Day 3) → UI + BI (Day 4) → deploy, scale & load-test (Day 5).**

### Deliverable for this track
Commit the k6 scripts and paste your summary numbers into `notes.md`: *peak RPS, p95 latency, error rate, and how many Pods the HPA reached. What would you change to handle 10,000?*

➡️ Back to the day plan: **[../README.md](../README.md)** · Course overview: **[../../README.md](../../README.md)**

---

## ⭐ Must-learn from this topic

- **Scenarios / ramping-vus** — schedule a climb to 5,000 VUs.
- **See autoscaling** — HPA raises replicas under load, lowers after.
- **Read results** — peak RPS, p95, error rate, pods reached.
- **Interpret limits** — what to change to go further (nodes, maxReplicas, CPU).

### 📚 Official docs
- [Scenarios](https://grafana.com/docs/k6/latest/using-k6/scenarios/) — executors like ramping-vus.
- [Results output](https://grafana.com/docs/k6/latest/results-output/) — reading the summary.
- [HPA walkthrough](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale-walkthrough/) — scaling under load.
