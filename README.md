# 5-Day Polyglot Engineering Training (2026)

A hands-on, expert-level training that teaches how to build a modern data platform using **many different databases together** (this is called *polyglot persistence*), connect them with **real-time streaming**, expose them through **APIs and a web UI**, add **dashboards and observability**, and finally **deploy and load-test** the whole system.

This repository holds all the teaching material. We start with **Day 1** and add more days over time.

> **How we teach here:** Every topic is written in simple, easy English. Each idea is explained, then shown with a small real example using **simple data we make ourselves** (no big downloads), and then given the **exact code or query** you can run. You learn by doing.

---

## Who this training is for

IT professionals (developers, data engineers, DBAs, architects) who already know the basics of programming and databases and now want to learn how several specialized databases and tools fit together into one real system.

You do **not** need to be an expert in every tool. The lessons start from simple language and build up.

---

## What you will learn (the 5-day map)

| Day | Title | What you build / learn |
|-----|-------|------------------------|
| **Day 1** | **Polyglot Persistence** | The four storage engines and *when to use each one*: **PostgreSQL** (relational), **Redis** (cache & data structures), **Neo4j** (graph), **Milvus** (vector). |
| **Day 2** | **Real-Time Streaming & Connectors** | Move data between systems live using **Kafka**, **Debezium** (change-data-capture), **Schema Registry**, and **KSQLDB**. |
| **Day 3** | **APIs, Async & Observability** | Build async services with **FastAPI**, add **OpenTelemetry** tracing, metrics with **Prometheus/Grafana**, logs with **Loki**, traces with **Jaeger**. |
| **Day 4** | **Front-End & Business Intelligence** | A **React + TypeScript** UI (Redux Toolkit, RTK Query, graph view with Vis.js) plus **Power BI** dashboards. |
| **Day 5** | **Deployment & Load Testing** | Package and run on **Kubernetes** (minikube, kubectl, Helm) and load-test 5,000 concurrent users with **k6**. |

> This repo currently contains **Day 1** in full. The other days will be added as the course continues.

---

## Day 1 in one paragraph

Day 1 is about **storage engines** — the different kinds of databases. A relational database (PostgreSQL) is great for structured records and transactions. A cache (Redis) is great for very fast reads and simple data structures like leaderboards. A graph database (Neo4j) is great for relationships, like "friends of friends". A vector database (Milvus) is great for "find me things that are *similar*", which powers search and AI features. By the end of Day 1 you can explain **why** you would pick each one, and you have run real queries against all four.

All four databases run inside **Docker**, so everyone has the exact same setup. You start them with one command.

---

## Participant prerequisites

### Hardware (training PC)

The training laptops are **HP EliteBook 840 — Core i7 8th-gen, 32 GB RAM, 256 GB SSD**, which is at the recommended level for this course. RAM is the most important spec because we run several databases at the same time.

| | Minimum | Recommended (our training PC) |
|---|---|---|
| CPU | 4 cores / 8 threads | 6–8 cores (i7 8th-gen is fine) |
| RAM | 16 GB | **32 GB** |
| Storage | 100 GB free SSD | 256 GB SSD (keep **80–100 GB free**) |
| OS | Windows 11 Pro / macOS 12+ / modern Linux | Windows 11 **Pro** |
| BIOS | Virtualization **enabled** (needed for Docker/WSL2) | same |

> Keep plenty of free disk space. Docker images and database volumes grow fast. Prune Docker regularly (`docker system prune`).

### Software to install (natively on the laptop)

**Foundation**
- Windows 11 **Pro** (confirm Pro, not Home — needed later for Hyper-V/minikube). Enable virtualization in BIOS first.
- **WSL2** with Ubuntu 22.04 (the Docker backend on Windows).
- **Docker Desktop** (set to use the WSL2 backend).
- **Git**.
- **VS Code** with extensions: Python, Pylance, Docker, ESLint, Prettier, Thunder Client.

**Language runtimes**
- **Python 3.11+** (via `pyenv` or `conda`).
- **Node.js LTS 20+** (via `nvm`).
- **Java JDK 17** (only if you run Kafka/KSQLDB CLI outside containers — often skippable).

**Convenience clients (optional — they also ship inside containers)**
- `psql`, `redis-cli`, `cypher-shell`, Kafka CLI tools, RedisInsight (GUI).

**Runs in Docker — do NOT install natively** (they come from `docker-compose.yml`):
PostgreSQL, Redis, Neo4j, Milvus, Kafka, Zookeeper, KSQLDB, Schema Registry, Debezium + connectors, Prometheus, Grafana, Jaeger, Loki.

**Per-project packages (installed later, not system-wide):** Python packages go into virtual environments; Node packages go into each project's `node_modules`.

---

## How this repository is organized

```
5-day-polyglot-training-2026/
├── README.md             <- you are here (full course overview)
├── docker-compose.yml    <- starts all Day 1 databases
└── day1/
    ├── README.md         <- Day 1 plan, schedule, checklist
    ├── 00-setup/         <- start the stack & test every connection
    ├── postgresql/       <- relational core
    ├── redis/            <- cache & data structures
    ├── neo4j/            <- graph
    └── milvus/           <- vector
```

Inside each engine folder you will find:
- **Numbered lesson files** (`01-...md`, `02-...md`, ...) — read them in order.
- A **`code/`** folder — runnable files (`.sql`, `.py`, `.js`, `.cypher`) for every example.
- A **`data/`** folder — small sample data, or a tiny script that generates it.

---

## The Day 1 example data: "Pixel Quest" online game

To keep things simple and fun, **all Day 1 lessons use one small make-believe dataset**: a tiny online game called **Pixel Quest**. The same data shows off all four databases:

- **Players** with scores → fits a **relational** table (PostgreSQL).
- **A live leaderboard** of scores → fits a **fast cache** (Redis).
- **Who is friends with whom** → fits a **graph** (Neo4j).
- **Game item descriptions** turned into numbers ("vectors") → fits a **vector** search (Milvus).

We generate this data ourselves with tiny scripts, so there is nothing to download.

---

## How to start (Day 1)

1. Install the foundation software above (Docker is the key one).
2. Open this folder in VS Code.
3. Start the databases:
   ```bash
   docker compose up -d
   ```
4. Open **`day1/README.md`** and follow it from the top.
5. When finished for the day, stop the databases to free memory:
   ```bash
   docker compose down
   ```

---

## A note on learning style

Go slowly. Read the explanation, run the example, look at the output, then change something and run it again. Breaking things on purpose and seeing what happens is one of the fastest ways to understand these tools.
