# Day 1 — Step 0: Setup (about 30 minutes)

Before we learn the four databases, we start them and make sure we can talk to each one. Everything runs inside **Docker**, so you do not install the databases on your laptop — Docker does it for you.

Do these steps in order. Do not skip the connection checks: it is much easier to fix a problem now than in the middle of a lesson.

---

## 1. Check the tools you need

Open a terminal and run these. Each should print a version number.

```bash
docker --version
docker compose version
python --version      # should be 3.11 or higher
node --version        # should be 20 or higher
git --version
```

If any of these fail, install the missing tool first (see the software list in the main `README.md`).

---

## 2. Start all the databases

From the **top folder** of this repository (the one that has `docker-compose.yml`), run:

```bash
docker compose up -d
```

- `up` means "create and start the containers".
- `-d` means "detached" — run in the background so you get your terminal back.

The first time, Docker downloads the images. This can take several minutes and a few GB of disk. Be patient.

Check what is running:

```bash
docker compose ps
```

You should see `pq_postgres`, `pq_redis`, `pq_neo4j`, `pq_milvus`, `pq_etcd`, and `pq_minio`. Wait until the database ones show as **healthy** (the health checks take up to a minute after the containers start).

> **Memory tip:** These services together use a lot of RAM. On a 32 GB machine you are fine. If your machine slows down, you can stop a service you are not using right now, e.g. `docker compose stop milvus`.

> **Apple Silicon / ARM users:** If you see a warning like *"The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8)"* for **milvus**, your machine is ARM (e.g. an M1/M2/M3 Mac). Start the stack with the ARM override file instead, so Milvus uses its native arm64 image:
> ```bash
> docker compose -f docker-compose.yml -f docker-compose.arm64.yml up -d
> ```
> The Intel training laptops (HP EliteBook) do **not** need this — they just use `docker compose up -d`. See the note at the bottom of this page for details.

---

## 3. Install the Python client libraries

Day 1 examples use a few Python packages. We put them in a **virtual environment** so they do not mix with your system Python.

```bash
# create and activate a virtual environment (run from the repo top folder)
python -m venv .venv

# activate it:
#   Windows (PowerShell):  .venv\Scripts\Activate.ps1
#   Windows (WSL/Linux/macOS):  source .venv/bin/activate

pip install --upgrade pip
pip install psycopg2-binary redis neo4j pymilvus numpy
```

What each package is for:
- `psycopg2-binary` — talk to **PostgreSQL**.
- `redis` — talk to **Redis**.
- `neo4j` — talk to **Neo4j**.
- `pymilvus` — talk to **Milvus**.
- `numpy` — make the random number "vectors" for the Milvus lab.

---

## 4. Test every connection

Run the connection checker. It tries all four databases and tells you which ones are OK.

```bash
python day1/00-setup/check_connections.py
```

A good result looks like this:

```
PostgreSQL : OK  (PostgreSQL 16.x ...)
Redis      : OK  (PONG)
Neo4j      : OK  (1 test row returned)
Milvus     : OK  (server reachable)
All good. You are ready for Day 1.
```

If one of them fails, the script prints the error. Common fixes:
- The container is not healthy yet — wait a minute and run again.
- A port is already used by another program — stop that program, or change the port in `docker-compose.yml`.
- Wrong password — the passwords used here are set in `docker-compose.yml` (user `trainer`, password `trainer` for PostgreSQL; `neo4j` / `trainer123` for Neo4j).

---

## 5. (Optional) Open the web UIs

Some databases have a web page you can open in your browser:

- **Neo4j Browser:** http://localhost:7474 — log in with user `neo4j`, password `trainer123`.
- **Redis Insight** (if you installed Redis Stack full / the desktop app): connect to `localhost:6379`.

---

## Connection details (write these down)

| Database | Host | Port | User | Password | Database name |
|----------|------|------|------|----------|---------------|
| PostgreSQL | localhost | 5432 | trainer | trainer | pixelquest |
| Redis | localhost | 6379 | (none) | (none) | — |
| Neo4j | localhost | 7687 | neo4j | trainer123 | neo4j |
| Milvus | localhost | 19530 | (none) | (none) | default |

## New to the terminal? Read this next

If you are not sure how to open a terminal, how to run a query line by line, or where the settings live, read the beginner guide before the lessons:

➡️ **[02-how-to-run-queries.md](02-how-to-run-queries.md)** — open a terminal, the 3 ways to run commands, and where config settings go.

---

## Troubleshooting: the Milvus "platform does not match" warning

If `docker compose up -d` prints something like:

```
! milvus  The requested image's platform (linux/amd64) does not match
          the detected host platform (linux/arm64/v8) ...
```

it means your computer's chip is **ARM** (Apple Silicon Mac, or another arm64 host), but the default Milvus image is built for **Intel (amd64)**. Docker will try to run it under emulation, which is slow and unreliable for Milvus.

**Fix — use the ARM override file** (it swaps in Milvus's native arm64 image):

```bash
# stop anything that started
docker compose down

# start using BOTH files
docker compose -f docker-compose.yml -f docker-compose.arm64.yml up -d
```

Use the same two `-f` flags for the other commands too:

```bash
docker compose -f docker-compose.yml -f docker-compose.arm64.yml ps
docker compose -f docker-compose.yml -f docker-compose.arm64.yml down
```

> **Tip:** to avoid typing the long command every time, you can set it once per terminal:
> ```bash
> export COMPOSE_FILE=docker-compose.yml:docker-compose.arm64.yml
> docker compose up -d      # now uses both files automatically
> ```

**On the Intel training laptops (HP EliteBook) you do nothing special** — the plain `docker compose up -d` is correct, and this warning will not appear.

---

When everything passes, open **`day1/README.md`** and begin with PostgreSQL.
