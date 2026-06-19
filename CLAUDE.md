# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A **teaching repository**, not a single deployable application. It holds the hands-on material for a 6-day polyglot-engineering course. Each `dayN/` folder is a self-contained module with its own `README.md`, numbered lesson markdown files (`01-...md`, `02-...md`, read in order), runnable `code/` examples, an `images/`/`screenshots/` folder, and usually its own `docker-compose.dayN.yml`. Lessons are written in deliberately plain English and each builds one small example on a shared toy dataset called **"Pixel Quest"** (an online game: players, scores, friendships, item descriptions).

Because it is course material, **prioritize clarity and consistency with the existing lesson style over cleverness.** When editing a lesson, match the tone and the explain → show → exact-command structure already in use. Lesson code is intentionally small and self-contained; don't refactor it into shared abstractions.

## The stack runs in Docker, layered per day

Containers are the runtime for almost everything. The root `docker-compose.yml` is **Day 1 only** (PostgreSQL, Redis, Neo4j, Milvus + its etcd/minio deps). Later days add their own services in `dayN/docker-compose.dayN.yml` and assume the Day 1 stack (or a subset) is already up. There is also a `docker-compose.arm64.yml` for Apple-Silicon/ARM hosts.

```bash
docker compose up -d                          # start Day 1 databases (root compose)
docker compose ps                             # see what's running
docker compose down                           # stop (keeps data volumes)
docker compose down -v                        # stop AND delete data (destructive)
docker compose -f day3/docker-compose.day3.yml up -d   # add a later day's services
```

Service containers are named `pq_*` (e.g. `pq_postgres`, `pq_redis`, `pq_neo4j`, `pq_milvus`).

Key default credentials / ports (from `docker-compose.yml`): Postgres `trainer/trainer`, db `pixelquest`, `:5432`; Neo4j `neo4j/trainer123`, browser `:7474`, bolt `:7687`; Redis `:6379`; Milvus SDK `:19530`.

## Common commands by area

**Python lessons (Day 3 FastAPI, observability):** packages install into one shared virtualenv.
```bash
pip install -r day3/requirements.txt
uvicorn app:app --reload          # run a FastAPI example from its code/ dir
```

**React UI (`day4/app/`, the real Vite + TS + Redux Toolkit app — note: `day4/react/` is lesson text, not the app):**
```bash
cd day4/app
npm install
npm run dev        # Vite dev server
npm run build      # tsc -b && vite build
npm test           # Vitest
npm run preview
```

**Day 5 deployment / load testing:**
```bash
day5/00-setup/check_cluster.sh                # verify minikube/kubectl readiness
kubectl apply -f day5/kubernetes/manifests/   # deployment.yaml, service.yaml, configmap.yaml
helm install <name> day5/helm/chart           # Helm chart lives here
k6 run day5/loadtest/code/smoke.js            # also load.js, stress_5k.js (5k users)
```
The app deployed in Day 5 is `day5/kubernetes/app/` (its own `Dockerfile`, `main.py`, `requirements.txt`) — separate from the Day 3 FastAPI code.

## Two areas outside the day-by-day flow

- **`day6/`** — advanced material on Claude Code, MCP servers (including the Blender and Playwright MCP servers configured for this session), and Spec-Driven Development with GitHub Spec Kit. The Blender `.blend`/`.fbx`/`.mp4` artifacts here come from the MCP lab. MCP server config conventions live in `day6/claude-code/`.
- **`real-problems-organization/multi-city-postgres-replication/`** — a standalone scenario with **per-city compose files** (`docker-compose.city1.yml` … `city3.yml`) and orchestration scripts in `scripts/` (`up.sh`, `setup-replication.sh`, `teardown.sh`, `demo.sh`). Run it via those scripts, not the root compose.
