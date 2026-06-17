# Day 5 — Deployment & Load Testing

**Goal:** Take the API from a script on your laptop to a **deployed, scalable service** on **Kubernetes** (minikube), package it with **Helm**, make it **auto-scale** under pressure, and prove it holds up with a **k6 load test of 5,000 concurrent users**.

> **How we teach here (same as Days 1–4):** easy English, one idea at a time, explanation → a small example with our **Pixel Quest** service → the exact command → what to expect. Folder per topic, runnable manifests/scripts, and a **⭐ Must-learn + 📚 Official docs** box at the end of every lesson.

---

## The big picture

So far the API ran with one `uvicorn` process on your machine. Real systems run **many copies** across a cluster, behind a load balancer, that **scale up** when traffic spikes and **heal** when a copy crashes. That is **Kubernetes**.

```
   k6 (5,000 virtual users)
            │  HTTP load
            ▼
   Kubernetes Service  ──►  Deployment (many Pods of the API)
            ▲                         │
            └── Horizontal Pod Autoscaler adds Pods when CPU climbs
   Helm packages all of the above as one installable chart
```

We deploy a small **stateless** version of the Pixel Quest API (so the focus is scaling/deployment, not databases) and hammer it with k6 to watch Kubernetes scale.

---

## What you will learn

| Topic | Tooling | What you do |
|-------|---------|-------------|
| **Kubernetes** | minikube, kubectl | containerize the API, deploy it, expose it, scale it |
| **Helm** | helm | package the app as a reusable chart |
| **Autoscaling** | HPA | add Pods automatically when CPU rises |
| **Load testing** | k6 | ramp to 5,000 virtual users, read p95/RPS/errors |

---

## Before you start

Day 5 is self-contained (it deploys its own small API image), so you do **not** need Days 1–4 running. You do need the cluster tools installed (see setup).

```bash
# start a local cluster (details in 00-setup)
minikube start
```

Then follow **[`00-setup/README.md`](00-setup/README.md)**.

> New to the terminal? The Day 1 guide still applies: **[../day1/00-setup/02-how-to-run-queries.md](../day1/00-setup/02-how-to-run-queries.md)**.

---

## Suggested schedule

**Setup (first 30 min)** — install minikube/kubectl/helm/k6, start the cluster, verify.

**Morning — Concepts**
- Kubernetes: containers vs Pods, Deployments, Services, ConfigMaps/Secrets, scaling.
- Helm: charts, templates, values.
- Autoscaling: the Horizontal Pod Autoscaler.

**Afternoon — Labs**
- Containerize and deploy the Pixel Quest API; scale it; expose it.
- Package it as a Helm chart and install it.
- Load-test with k6 to 5,000 virtual users and watch the HPA add Pods.

---

## Lessons in order

### 0. Setup
- [`00-setup/README.md`](00-setup/README.md) — install the tools, start minikube, verify.

### 1. Kubernetes
1. [Intro & concepts](kubernetes/01-intro-and-concepts.md)
2. [Containerize the API](kubernetes/02-containerize-the-app.md)
3. [Deployments & Services](kubernetes/03-deployments-and-services.md)
4. [Config & scaling](kubernetes/04-config-and-scaling.md)
5. [LAB: deploy Pixel Quest](kubernetes/05-lab-deploy-pixelquest.md)

### 2. Helm
1. [Why Helm?](helm/01-why-helm.md)
2. [Chart anatomy](helm/02-chart-anatomy.md)
3. [LAB: package & install](helm/03-lab-package-and-install.md)

### 3. Autoscaling
1. [Horizontal Pod Autoscaler (HPA)](autoscale/01-hpa.md)

### 4. Load testing (k6)
1. [Intro to k6](loadtest/01-k6-intro.md)
2. [Writing tests & thresholds](loadtest/02-writing-tests.md)
3. [LAB: 5,000 concurrent users](loadtest/03-lab-5k-load.md)

---

> 📸 **Screenshots:** every lesson has its command output captured inline. See them all in one place: **[`screenshots/README.md`](screenshots/README.md)**.

---

## End-of-day result (deliverable)

Commit the manifests, the Helm chart, and the k6 scripts, plus a short `notes.md`: *What did the HPA do during the 5k test? What was your p95 latency and error rate, and what would you change to handle more?*

## When you finish

```bash
minikube stop      # or `minikube delete` to remove the cluster entirely
```
