# Day 4 — Front-End & Business Intelligence

**Goal:** Build the **user-facing layer**. A **React + TypeScript** web app that reads the Pixel Quest API (players, leaderboard, friendships graph), and **Metabase** dashboards for business reporting over the same data.

> **How we teach here (same as Days 1–3):** easy English, one idea at a time, explanation → a small example with our **Pixel Quest** data → the exact code/command → what to expect. Folder per topic, runnable code, and a **⭐ Must-learn + 📚 Official docs** box at the end of every lesson.

---

## The big picture

Day 1 stored the data, Day 2 streamed it, Day 3 put an **API** in front of it. Day 4 is what people actually *see*: a **web UI** and **dashboards**.

```
                         ┌─ React + TypeScript app (Vite, :5173)
 Day 3 FastAPI (:8000) ──┤    • leaderboard table   (RTK Query)
   /players              │    • player detail
   /leaderboard          │    • friendships graph   (Vis.js)
   /players/{id}/summary └─ tested with Jest + RTL + MSW

 Day 1 PostgreSQL (:5432) ── Metabase (:3001) ── business dashboards
```

- The **React app** calls the **Day 3 FastAPI** for live data.
- **Metabase** (open-source BI) connects straight to the **Day 1 PostgreSQL** for reporting.

> **Why Metabase, not Power BI?** Power BI is closed and Windows-only. For a closed/secure environment we use **Metabase** — open source, self-hosted in Docker, connects to PostgreSQL, and builds dashboards through a friendly UI. (Apache Superset is a heavier alternative.)

---

## What you will learn

| Section | Tooling | Pixel Quest example |
|---------|---------|---------------------|
| **React + TypeScript** | Vite, components, hooks, TS types | a leaderboard table |
| **State & data** | Redux Toolkit + RTK Query | live leaderboard + player detail from the API |
| **Graph view** | Vis.js (vis-network) | interactive friendships network |
| **Testing** | Jest + React Testing Library + MSW | test components against a mocked API |
| **Business Intelligence** | Metabase (open source) | dashboard: top players, scores by country, purchases |

---

## Before you start

Day 4 reuses the **Day 1 PostgreSQL** (for Metabase) and the **Day 3 FastAPI** (for the app's live data).

1. Day 1 databases up (repo top folder):
   ```bash
   docker compose up -d
   ```
2. Day 3 API running (so the app has data to read):
   ```bash
   cd day3/observability/code && uvicorn app_observed:app --reload --port 8000
   ```
3. Start Metabase:
   ```bash
   docker compose -f day4/docker-compose.day4.yml up -d
   ```
4. Follow **[`00-setup/README.md`](00-setup/README.md)** to create the React app and install packages.

> New to the terminal? The Day 1 guide still applies: **[../day1/00-setup/02-how-to-run-queries.md](../day1/00-setup/02-how-to-run-queries.md)**.

---

## Suggested schedule

**Setup (first 30 min)** — Node/Vite, scaffold the app, start Metabase, confirm the API is reachable (CORS).

**Morning — Concepts**
- React + TypeScript: components, props, state, hooks, typing.
- Redux Toolkit + RTK Query: a store and fetching API data with caching.
- Vis.js: drawing an interactive network graph.

**Afternoon — Labs**
- Build the Pixel Quest dashboard UI (leaderboard, player detail, friendships graph).
- Test it with Jest + RTL + MSW.
- Build a Metabase dashboard over the PostgreSQL data.

---

## Lessons in order

### 0. Setup
- [`00-setup/README.md`](00-setup/README.md) — Node/Vite, the app skeleton, start Metabase, CORS.

### 1. React + TypeScript
1. [Intro & your first component](react/01-intro-and-first-component.md)
2. [Props, state & rendering lists](react/02-props-state-lists.md)
3. [Hooks & TypeScript types](react/03-hooks-and-types.md)
4. [LAB: the leaderboard table](react/04-lab-leaderboard-table.md)

### 2. State & data fetching
1. [Redux Toolkit store & slices](state/01-redux-toolkit.md)
2. [RTK Query: data from the API](state/02-rtk-query.md)
3. [LAB: live leaderboard + player detail](state/03-lab-live-data.md)

### 3. Graph visualization (Vis.js)
1. [Drawing a network](graphview/01-vis-network.md)
2. [LAB: the friendships explorer](graphview/02-lab-friendships.md)

### 4. Testing
1. [Jest + React Testing Library](testing/01-jest-rtl.md)
2. [LAB: mock the API with MSW](testing/02-lab-msw.md)

### 5. Business Intelligence (Metabase)
1. [Connect Metabase to PostgreSQL](bi/01-connect-metabase.md)
2. [Build questions & visuals](bi/02-questions-and-visuals.md)
3. [LAB: the Pixel Quest dashboard](bi/03-lab-dashboard.md)

---

## The web UIs you will use today

| Tool | URL | Login |
|------|-----|-------|
| React app (Vite dev server) | http://localhost:5173 | — |
| Day 3 API docs | http://localhost:8000/docs | — |
| Metabase | http://localhost:3001 | set on first run |

> Metabase uses port **3001** here so it does not clash with Grafana (Day 3) on 3000.

---

## End-of-day result (deliverable)

Commit the React app and a short `notes.md`: *Why use RTK Query instead of calling `fetch` in every component? When is a graph view the right UI? What's one business question your Metabase dashboard answers that the app UI does not?*

## When you finish, stop Metabase

```bash
docker compose -f day4/docker-compose.day4.yml down
```
