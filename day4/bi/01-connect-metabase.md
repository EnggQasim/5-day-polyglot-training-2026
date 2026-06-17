# Business Intelligence — Step 1: Connect Metabase to PostgreSQL

## What is Metabase, and why it (not Power BI)

**Metabase** is an open-source **business intelligence** tool: connect it to a database and non-developers can ask questions and build dashboards through a friendly UI — no code needed. We use it instead of Power BI because Power BI is closed and Windows-only; Metabase is **open source, self-hosted in Docker**, and perfect for a closed/secure environment. (Apache Superset is a heavier open-source alternative.)

**BI vs the app UI:** the React app is for *players* (live, interactive). BI is for the *business* — "which countries spend the most?", "how did scores trend this month?" — exploratory questions and dashboards over the raw data.

---

## Step 1 — start Metabase

```bash
docker compose -f day4/docker-compose.day4.yml up -d
```

Open **http://localhost:3001**. First run asks you to create an admin account (name, email, password) — this is local to your machine.

> Metabase here stores its own settings in an internal H2 database (fine for training). It uses port **3001** so it doesn't clash with Grafana on 3000.

---

## Step 2 — add the Pixel Quest database

In Metabase: **Settings (gear) → Admin settings → Databases → Add database**.

- **Database type:** PostgreSQL
- **Host:** `host.docker.internal`  ← reaches the Day 1 Postgres from inside the Metabase container
- **Port:** `5432`
- **Database name:** `pixelquest`
- **Username:** `trainer`
- **Password:** `trainer`

Save. Metabase scans the schema and finds the `players` and `purchases` tables (from Day 1).

> On plain Linux, if `host.docker.internal` doesn't resolve, add `extra_hosts: ["host.docker.internal:host-gateway"]` to the `metabase` service in `docker-compose.day4.yml`, or put both stacks on a shared Docker network.

![Metabase admin database connection form filled in for PostgreSQL](images/01-connection.png)

*The connection form (Admin → Databases): **Host** `host.docker.internal`, **Port** `5432`, **Database name** `pixelquest`, **Username** `trainer`. After saving, Metabase scans the schema.*

---

## Step 3 — first look at the data

- Click **Browse data → Pixel Quest → Players**. Metabase shows the table.
- Use the **Summarize** button to get instant aggregates (e.g. count of rows, average score) — no SQL.
- Click **Filter** to narrow rows (e.g. `country = PK`).

![Metabase browsing the public schema tables, including Players and Purchases](images/01-browse-tables.png)

*After the scan, **Browse data → PostgreSQL → public** lists the tables Metabase found — including `Players` and `Purchases` from Day 1.*

![The Players table opened in Metabase showing 12 rows](images/01-players-table.png)

*Opening **Players** shows the rows with **Filter** and **Summarize** at the top — point-and-click exploration, no SQL needed.*

This point-and-click exploration is the heart of Metabase: business users answer questions without writing queries. Next we build proper **questions** (saved queries that become charts).

➡️ Next: **[02-questions-and-visuals.md](02-questions-and-visuals.md)**

---

## ⭐ Must-learn from this topic

- **Metabase** — open-source, self-hosted BI; point-and-click over a database.
- **Connect** — PostgreSQL via `host.docker.internal:5432`, db `pixelquest`.
- **Browse / Summarize / Filter** — explore data with no SQL.
- **BI vs app** — business questions/dashboards vs the live user UI.

### 📚 Official docs
- [Metabase docs](https://www.metabase.com/docs/latest/) — start here.
- [Adding a database](https://www.metabase.com/docs/latest/databases/connecting) — connection setup.
- [Running Metabase on Docker](https://www.metabase.com/docs/latest/installation-and-operation/running-metabase-on-docker).
