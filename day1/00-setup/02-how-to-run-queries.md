# Day 1 — How to open a terminal and run every query (beginner guide)

This guide explains, in very simple steps:
1. **How to open a terminal** on the training laptops (Windows 11).
2. **The 3 ways to run database commands** (type one by one, run a whole file, or use a web UI).
3. **Where the config (settings) live** and how to change them.

Read this once. After that, every lesson will make sense.

---

## Part 1 — How to open a terminal

A "terminal" (also called a *command line*, *shell*, *PowerShell*, or *prompt*) is a black window where you type commands. We use it for everything in this course.

On our Windows laptops you have a few options. **Use option C (VS Code) — it is the easiest.**

### Option A — PowerShell
1. Press the **Windows key**.
2. Type `PowerShell`.
3. Click **Windows PowerShell**.

### Option B — WSL / Ubuntu terminal
(Our Docker runs inside WSL2 Ubuntu.)
1. Press the **Windows key**.
2. Type `Ubuntu` (or `wsl`).
3. Press Enter. A Linux terminal opens.

### Option C — VS Code terminal (recommended)
1. Open **VS Code**.
2. Open this training folder: **File → Open Folder…** and pick `5-day-polyglot-training-2026`.
3. Open the built-in terminal: menu **Terminal → New Terminal**, or press **Ctrl + `** (the key above Tab).
4. A terminal opens **already inside the project folder** — this is why it is the easiest. All the commands in the lessons assume you are in this folder.

> **Tip:** to confirm where you are, type `pwd` (print working directory) and press Enter. You should see a path ending in `5-day-polyglot-training-2026`.

### Moving into the project folder by hand (if needed)
If your terminal opened somewhere else, move into the folder with `cd` ("change directory"):

```bash
cd "C:\Users\<your-name>\Desktop\...\5-day-polyglot-training-2026"
```

Now you are ready to run commands.

---

## Part 2 — Start the databases first

Before running any query, the databases must be running. From the project folder:

```bash
docker compose up -d        # start all databases in the background
docker compose ps           # check they are running / healthy
```

When you finish for the day:

```bash
docker compose down         # stop them and free memory
```

---

## Part 3 — The 3 ways to run database commands

Every database in this course can be used in more than one way. You will use all three. Here is the pattern, with one example per engine.

### Way 1 — Interactive client (type queries one by one)

You open a small program *inside* the database container and type queries at a prompt. This is best for **learning and trying things**.

**PostgreSQL** (prompt is `pixelquest=#`):
```bash
docker exec -it pq_postgres psql -U trainer -d pixelquest
```
Then type one query, end it with a **semicolon `;`**, and press Enter:
```sql
SELECT username, score FROM players ORDER BY score DESC;
```
- One query per line. The `;` tells PostgreSQL "this query is finished — run it."
- A query can span several lines; nothing runs until you type `;` and Enter.
- To leave, type `\q` and press Enter.

**Redis** (prompt is `127.0.0.1:6379>`):
```bash
docker exec -it pq_redis redis-cli
```
Then type commands (no semicolon needed in Redis):
```
PING
ZREVRANGE leaderboard 0 4 WITHSCORES
```
To leave, type `exit`.

**Neo4j** (prompt is `neo4j@neo4j>`):
```bash
docker exec -it pq_neo4j cypher-shell -u neo4j -p trainer123
```
Type a Cypher query, end with `;`:
```cypher
MATCH (p:Player) RETURN p.name, p.score;
```
To leave, type `:exit`.

**Milvus** has **no interactive shell.** You always use Python (Way 3 below).

---

### Way 2 — Run a whole file at once

Each lesson ships ready-made files in its `code/` folder. Instead of typing every line, you can feed the whole file into the client. This is best for the **seed scripts and labs**.

The pattern is `docker exec -i <container> <client> < path/to/file`. The `<` means "send this file into the program".

**PostgreSQL** — run a `.sql` file:
```bash
docker exec -i pq_postgres psql -U trainer -d pixelquest < day1/postgresql/code/01_schema_and_seed.sql
```

**Redis** — run a `.redis` file:
```bash
docker exec -i pq_redis redis-cli < day1/redis/code/02_data_structures.redis
```

**Neo4j** — run a `.cypher` file:
```bash
docker exec -i pq_neo4j cypher-shell -u neo4j -p trainer123 < day1/neo4j/code/01_seed.cypher
```

> **`-it` vs `-i`:** use `-it` when *you* will type (interactive). Use `-i` when you are *feeding a file*. Small difference, easy to remember: add the `t` only when you type.

---

### Way 3 — Run a Python script

The labs (and all of Milvus) use Python. First activate the virtual environment you made in setup, then run the script.

```bash
# activate the virtual environment (once per terminal session)
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# WSL / Linux / macOS:
source .venv/bin/activate

# run a script
python day1/milvus/code/03_lab_vector_search.py
python day1/redis/code/05_lab_leaderboard.py
```

When the environment is active you will see `(.venv)` at the start of your prompt.

---

### Way 4 — Web UI (click instead of type)

Some databases have a web page, nice for seeing results visually.

- **Neo4j Browser:** open `http://localhost:7474` in your browser. Log in with user `neo4j`, password `trainer123`. Type Cypher in the top bar and press the ▶ run button — it **draws the graph** for you.
- **RedisInsight:** if installed, connect to `localhost:6379` to browse keys with a GUI.

---

## Part 4 — Where the config (settings) live

"Config" means the settings that control each database: ports, passwords, memory limits, enabled features. There are **two levels**: settings you set **when the container starts** (in `docker-compose.yml`), and settings you change **while it is running**.

### Level 1 — Container settings: `docker-compose.yml` (in the project's top folder)

This single file is the main place for setup-time config. Open it in VS Code. Examples already inside it:

- **Ports** (which port on your laptop maps to the database):
  ```yaml
  ports:
    - "5432:5432"     # laptop_port : container_port
  ```
- **Username / password / database name** (PostgreSQL):
  ```yaml
  environment:
    POSTGRES_USER: trainer
    POSTGRES_PASSWORD: trainer
    POSTGRES_DB: pixelquest
  ```
- **Neo4j password and plugins:**
  ```yaml
  environment:
    NEO4J_AUTH: neo4j/trainer123
    NEO4J_PLUGINS: '["apoc","graph-data-science"]'
  ```

**How to apply a change:** edit `docker-compose.yml`, save, then re-run:
```bash
docker compose up -d
```
Docker recreates only the containers that changed.

> Neo4j has a neat rule: any setting from its config file `neo4j.conf` can be set here as an environment variable by writing `NEO4J_` and replacing dots with underscores. Example: the setting `dbms.memory.heap.max_size` becomes `NEO4J_dbms_memory_heap_max__size`.

### Level 2 — Runtime settings (change while running)

Some settings can be changed live, without restarting.

**PostgreSQL** — per-session or global:
```sql
SHOW work_mem;                       -- read a setting
SET work_mem = '32MB';               -- change for THIS session only
ALTER SYSTEM SET work_mem = '32MB';  -- change permanently (needs reload)
SELECT pg_reload_conf();             -- apply ALTER SYSTEM changes
```

**Redis** — live config (this is how we turn on AOF in the persistence lesson):
```
CONFIG GET maxmemory-policy          -- read a setting
CONFIG SET appendonly yes            -- change it now (until restart)
```
To make a Redis setting **permanent**, put it in a `redis.conf` file and mount it in `docker-compose.yml`, or pass it as a command flag. For this training, `CONFIG SET` is enough.

**Neo4j** — most server config is set via the `NEO4J_*` environment variables in `docker-compose.yml` (Level 1). Some things can be changed live in Cypher, e.g.:
```cypher
SHOW DATABASES;
```

**Milvus** — connection settings (host, port) are passed in your Python code:
```python
connections.connect(host="localhost", port="19530")
```
Server-side tuning lives in Milvus's own `milvus.yaml`, which we do not need to touch for Day 1.

---

## Quick cheat sheet

| Action | Command |
|--------|---------|
| Start all databases | `docker compose up -d` |
| Stop all databases | `docker compose down` |
| See what's running | `docker compose ps` |
| Open PostgreSQL prompt | `docker exec -it pq_postgres psql -U trainer -d pixelquest` |
| Open Redis prompt | `docker exec -it pq_redis redis-cli` |
| Open Neo4j prompt | `docker exec -it pq_neo4j cypher-shell -u neo4j -p trainer123` |
| Run a SQL file | `docker exec -i pq_postgres psql -U trainer -d pixelquest < FILE.sql` |
| Run a Cypher file | `docker exec -i pq_neo4j cypher-shell -u neo4j -p trainer123 < FILE.cypher` |
| Run a Redis file | `docker exec -i pq_redis redis-cli < FILE.redis` |
| Run a Python script | `python PATH/TO/script.py` (after activating `.venv`) |
| Change container config | edit `docker-compose.yml` → `docker compose up -d` |

---

Now go to **[../README.md](../README.md)** and start the lessons. Whenever a lesson shows a query, use **Way 1** (type it) or **Way 2** (run the file) from this guide.
