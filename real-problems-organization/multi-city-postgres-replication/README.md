# Multi-City PostgreSQL — Active-Active Replication with Local HA

A runnable, 3-city PostgreSQL cluster where **every city can accept writes**, all
data **syncs to every other city**, and **each city has its own local backup**
that can take over if the city's primary fails.

Built with plain `postgres:16` + Docker Compose — no custom images to build.

---

## 1. Problem statement

We run a database in **three cities** (Rawalpindi, Lahore, Karachi). Each city:

- has its **own PostgreSQL database** that the local application reads/writes, and
- has its **own backup server** for that city.

Requirements:

1. **Active-active across cities** — whatever data is inserted in *any* city must
   appear in *all* cities (bidirectional sync). All cities use the **same table
   name and schema**.
2. **Local High Availability** — each city's primary has a local backup standby;
   if the primary dies the city keeps working (and, for a limited time, the app
   may even point at another city's database).
3. **The hard part — ID collisions.** While a city is disconnected it keeps
   inserting locally. Two cities can independently generate the **same primary
   key** for two *different* real-world records. When they reconnect we must
   **keep BOTH rows**, not overwrite one with the other.

```
City1: DB1 (Rawalpindi) ──┐
        └─ backup standby │
City2: DB2 (Lahore)    ───┼──▶ all DBs share data (bidirectional, active-active)
        └─ backup standby │
City3: DB3 (Karachi)   ───┘
        └─ backup standby
```

---

## 2. Our purpose

Stand up a realistic, reproducible model of the above so we can **see** it work:
insert in three places at once, watch every node converge, then kill a primary
and confirm the local backup still holds the data.

---

## 3. The solution

Two independent layers — don't confuse them, you need both:

| Layer | Purpose | How |
|-------|---------|-----|
| **A. Cross-city sync** | Data written anywhere appears everywhere | PostgreSQL **logical replication**, full mesh, `WITH (origin = none)` (PG16 bidirectional) |
| **B. Local HA** | Each city survives losing its primary | PostgreSQL **physical streaming replication** to a local **backup standby** |

### Why a UUID primary key solves the "keep both rows" problem

A primary key is **unique by definition** — Postgres physically cannot store two
rows with the same key in one table. So "two rows with the same id" can never be
kept; the merge would reject one. The fix is to **prevent the collision** so the
two different records get **different keys** and both survive naturally.

We use a **UUID** primary key (`gen_random_uuid()`):

- Globally unique with **zero coordination** between cities — even while
  disconnected, City1 and City2 can never mint the same id.
- Both rows are therefore **always kept** after sync. ✅

> Alternatives if you must keep integer ids: a composite key `(city_id, id)`, or
> per-city offset sequences (City1: 1,4,7… / City2: 2,5,8… / City3: 3,6,9…).
> UUID is the lowest-friction choice and is what this project uses.

### What about two cities editing the *same* row?

UUID keys solve duplicate **inserts**. If two cities **update the same existing
row** at the same time, that's a true write-write conflict. Native PG logical
replication does **last-write-wins by commit timestamp** and will log conflicts.
For production-grade automatic conflict resolution across many masters, use
**[pgEdge / Spock](https://www.pgedge.com/)** — it's purpose-built for distributed
multi-master Postgres and manages sequences + conflicts for you. This demo uses
native replication to keep it dependency-free and transparent.

---

## 4. What's in this folder

```
docker-compose.city1.yml     Rawalpindi : primary (5433) + backup (5443)
docker-compose.city2.yml     Lahore     : primary (5434) + backup (5444)
docker-compose.city3.yml     Karachi    : primary (5435) + backup (5445)
init/primary/
  00-setup.sql               'replicator' role + open replication in pg_hba
  01-schema.sql              shared schema (UUID PK) + publication
scripts/
  standby-entrypoint.sh      turns a container into a streaming backup standby
  up.sh                      create network + start all 3 cities
  setup-replication.sh       wire the active-active mesh (run once)
  demo.sh                    prove sync + show HA copies
  teardown.sh                stop everything + delete volumes
```

All three cities join one shared external Docker network (`citynet`) so the
containers can reach each other by name (`pg-city1`, `pg-city2`, `pg-city3`).

---

## 5. Step-by-step: run it

Prerequisites: Docker Desktop (or Docker Engine) with Compose v2, and a free
local TCP range 5433–5445.

```bash
cd multi-city-postgres-replication
chmod +x scripts/*.sh        # first time only

# 1) Create the shared network and start all three cities (6 containers).
./scripts/up.sh

# 2) Wait until all containers are healthy (each primary + its backup).
docker ps

# 3) Wire the active-active mesh (run ONCE, before inserting data).
./scripts/setup-replication.sh

# 4) Prove it: insert on every city, watch all nodes converge, see backups.
./scripts/demo.sh
```

Expected: after `demo.sh`, **every primary shows all three rows**
(`rawalpindi-widget`, `lahore-gadget`, `karachi-gizmo`) and each backup mirrors
its own city.

### Connect manually

```bash
# Rawalpindi primary from your host:
psql "host=localhost port=5433 user=admin password=adminpass dbname=citydb"
```

---

## 6. Failover test (the HA layer)

Simulate Rawalpindi's primary dying and confirm the local backup kept the data:

```bash
# kill the city1 primary
docker compose -f docker-compose.city1.yml stop pg-city1

# the backup is read-only but already has every row:
docker exec -it pg-city1-backup psql -U admin -d citydb -c \
  "SELECT node_origin, item, qty FROM orders ORDER BY created_at;"

# promote the backup to a writable primary:
docker exec -it pg-city1-backup su postgres -c "pg_ctl promote -D /var/lib/postgresql/data"

# bring the old primary back later:
docker compose -f docker-compose.city1.yml start pg-city1
```

In production this promotion + connection rerouting is automated with
**Patroni + HAProxy** (see below) so the app fails over without manual steps.

---

## 7. Useful inspection queries

```bash
# subscriptions on a node + their state
docker exec -it pg-city1 psql -U admin -d citydb -c \
 "SELECT subname, subenabled FROM pg_subscription;"

# replication slots being consumed on a node
docker exec -it pg-city1 psql -U admin -d citydb -c \
 "SELECT slot_name, slot_type, active FROM pg_replication_slots;"

# is the backup caught up? (run against the primary)
docker exec -it pg-city1 psql -U admin -d citydb -c \
 "SELECT client_addr, state, sync_state FROM pg_stat_replication;"
```

---

## 8. From demo to production

This project intentionally favours clarity over hardening. For real deployments:

- **Conflict resolution / multi-master at scale** → **pgEdge (Spock)** instead of
  hand-rolled native subscriptions. It manages distributed sequences and
  automatic conflict resolution.
- **Automatic local failover** → **Patroni** (+ etcd) to auto-promote the backup,
  and **HAProxy/PgBouncer** so the app reconnects automatically (and can be
  routed to another city "for a limited time" when both local nodes are down).
- **Secrets** → move passwords out of compose into a secrets manager / `.env`.
- **TLS** between nodes, tightened `pg_hba.conf` (specific subnets, not
  `0.0.0.0/0`), and tuned `wal_keep_size` / replication slots.
- **Synchronous replication** to the local backup if zero data loss is required
  (`synchronous_standby_names`), at the cost of some write latency.

---

## 9. Reset

```bash
./scripts/teardown.sh     # stops all cities and deletes their volumes
```
