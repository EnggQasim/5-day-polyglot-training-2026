# Spec Kit — Step 3: LAB (build a real feature with Spec Kit)

Take one real feature from your platform through the full Spec-Driven flow with Claude Code. We use **"nearby assets"** (a PostGIS spatial query exposed as an API and shown in React) — it touches your actual stack.

**Prerequisites:** `uv` installed, Claude Code, and (ideally) the Day 1 Postgres/PostGIS running so `/implement` can be tested.

---

## Step 1 — initialize

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init geosim-nearby --ai claude
cd geosim-nearby
```
Open the folder in Claude Code.

## Step 2 — constitution

```
/constitution Type hints everywhere; every feature ships with tests; spatial
queries must use a GiST index and ST_DWithin; backend is FastAPI + asyncpg;
frontend is React + RTK Query; no writes to production data.
```

## Step 3 — specify (review the output!)

```
/specify "Nearby assets": given a longitude, latitude, and radius in metres,
return assets within the radius sorted by distance (nearest first), each with
id, name, category, and distance_m. Target: under 1 second for 1M assets.
Users: mission planners.
```
Open the generated `spec.md`. **Read it.** Fix anything that doesn't match what you meant. (Optionally run `/clarify`.)

## Step 4 — plan

```
/plan PostGIS table assets(id, name, category, geom geography). Use
ST_DWithin(geom, point, radius) with a GiST index on geom. Endpoint:
GET /assets/nearby?lon=&lat=&radius= via FastAPI + asyncpg. Cache repeated
queries in Redis (60s TTL). React page calls it with RTK Query and lists results.
```
Review `plan.md` — check the data model, the index, and the endpoint shape.

## Step 5 — tasks, then implement

```
/tasks
```
Skim `tasks.md` — it should include: migration + GiST index, the spatial query, the FastAPI endpoint, the Redis cache, tests, and the React list. Then:

```
/implement
```
The agent builds it. Because spec → plan → tasks were reviewed, the result should match intent. Run the tests it wrote.

## Step 6 — verify the artifacts

```
specs/nearby-assets/spec.md     # the WHAT (reviewed)
specs/nearby-assets/plan.md     # the HOW (reviewed)
specs/nearby-assets/tasks.md    # the checklist
+ the code & tests
```

Commit them (use the **GitHub MCP** from the morning to open the PR). The next engineer can read the *intent*, not just guess from the code.

---

## What you achieved

- Ran a complete **Spec-Driven** build on a realistic stack feature.
- Saw **review gates** (spec, plan, tasks) catch issues before code.
- Produced **version-controlled intent** alongside working code + tests.

### Deliverable for this track
Commit the `specs/` artifacts and paste your `spec.md` into `notes.md`. Reflect: *Where did reviewing the spec/plan change the outcome vs a one-line prompt? Which of your real features would you run through Spec Kit next?*

➡️ Back to the day plan: **[../README.md](../README.md)** · Course overview: **[../../README.md](../../README.md)**

---

## ⭐ Must-learn from this topic

- **End-to-end SDD** — one feature from constitution to implementation.
- **Review gates** — approve spec & plan before any code is written.
- **Stack-real** — PostGIS + FastAPI + Redis + React, the way you actually build.
- **Intent in git** — spec/plan/tasks committed with the code.

### 📚 Official docs
- [Spec Kit repo](https://github.com/github/spec-kit) and [docs](https://github.github.com/spec-kit/).
- [GitHub blog: spec-driven development](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/).
- [Claude Code + MCP](https://docs.claude.com/en/docs/claude-code/mcp) — to wire the GitHub MCP for PRs.
