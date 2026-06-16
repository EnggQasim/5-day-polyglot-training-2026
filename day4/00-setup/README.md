# Day 4 — Step 0: Setup (about 30 minutes)

Today you build a **React + TypeScript** app (runs on your laptop with Vite) and a **Metabase** dashboard (runs in Docker). Both read Pixel Quest data: the app from the Day 3 API, Metabase from the Day 1 PostgreSQL.

---

## 1. Check Node

```bash
node --version    # should be 20 or higher
npm --version
```

If Node is missing, install Node.js LTS 20+ (via `nvm` or the installer).

---

## 2. Use the prepared app, or scaffold your own

We ship a ready React + TypeScript project in **`day4/app/`**. From there:

```bash
cd day4/app
npm install
npm run dev
```

Open **http://localhost:5173** — you should see the Pixel Quest starter page.

> Prefer to scaffold from scratch? `npm create vite@latest pixelquest-ui -- --template react-ts` makes the same kind of project; then copy our `src/` lesson files into it.

The packages we use (already in `app/package.json`):
- `react`, `react-dom`, `typescript`, `vite` — the core app.
- `@reduxjs/toolkit`, `react-redux` — state + RTK Query (section 2).
- `vis-network`, `vis-data` — the graph view (section 3).
- `jest`/`vitest`, `@testing-library/react`, `msw` — testing (section 4).

---

## 3. Start Metabase (for the BI section)

```bash
docker compose -f day4/docker-compose.day4.yml up -d
```

Open **http://localhost:3001** and create an admin account on first run. We connect it to PostgreSQL in the BI lessons.

---

## 4. Let the browser app call the API (CORS)

Browsers block a page on `localhost:5173` from calling an API on `localhost:8000` unless the API allows it (this is **CORS**). Add this to the Day 3 FastAPI app (e.g. near the top of `day3/observability/code/app_observed.py`) and restart it:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],   # the Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Restart uvicorn after adding it. (We point this out again in the RTK Query lesson, where it first matters.)

---

## 5. Quick check

With the app running (`npm run dev`) and the API running:

- **http://localhost:5173** → the app loads.
- **http://localhost:8000/players** → returns JSON (the API works).
- **http://localhost:3001** → Metabase loads.

If all three open, you are ready.

---

## Ports today

| Thing | URL |
|-------|-----|
| React app (Vite) | http://localhost:5173 |
| Day 3 API | http://localhost:8000 (`/docs`) |
| Metabase | http://localhost:3001 |

When everything is up, open **[`../README.md`](../README.md)** and start with React.
