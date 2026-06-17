# State — Step 3: LAB (live leaderboard + player detail)

Wire the UI to the **live Day 3 API** with RTK Query: a leaderboard that polls for updates, and a player-detail panel that loads on demand.

Files: [`app/src/store/api.ts`](../app/src/store/api.ts), [`app/src/store/index.ts`](../app/src/store/index.ts), and the components [`LiveLeaderboard.tsx`](../app/src/components/LiveLeaderboard.tsx) + [`PlayerDetail.tsx`](../app/src/components/PlayerDetail.tsx).

**Prerequisites:** Day 1 DBs up, Day 3 API running on `:8000`, and the CORS snippet added (see setup).

---

## Step 1 — Provider + store (one-time wiring)

`src/main.tsx`:

```tsx
import { Provider } from "react-redux";
import { store } from "./store";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <Provider store={store}><App /></Provider>
);
```

## Step 2 — live leaderboard (polls every 3s)

[`LiveLeaderboard.tsx`](../app/src/components/LiveLeaderboard.tsx):

```tsx
import { useGetLeaderboardQuery } from "../store/api";
import { PlayerRow } from "./PlayerRow";

export function LiveLeaderboard() {
  const { data, isLoading, error } = useGetLeaderboardQuery(5, { pollingInterval: 3000 });
  if (isLoading) return <p>Loading…</p>;
  if (error) return <p>Could not reach the API. Is it running on :8000?</p>;
  return (
    <table>
      <thead><tr><th>#</th><th>Player</th><th>Score</th></tr></thead>
      <tbody>{data!.map((r) => <PlayerRow key={r.player} {...r} />)}</tbody>
    </table>
  );
}
```

## Step 3 — player detail (loads when you pick an id)

[`PlayerDetail.tsx`](../app/src/components/PlayerDetail.tsx) uses local state for the selected id and an RTK Query hook with `skip` until one is chosen:

```tsx
import { useState } from "react";
import { useGetPlayerSummaryQuery } from "../store/api";

export function PlayerDetail() {
  const [id, setId] = useState<number | null>(null);
  const { data } = useGetPlayerSummaryQuery(id!, { skip: id === null });
  return (
    <div>
      <label>Player id: <input type="number" onChange={(e) => setId(Number(e.target.value))} /></label>
      {data && <p>{data.username} — score {data.score}, rank {data.rank}</p>}
    </div>
  );
}
```

`skip: id === null` tells RTK Query "don't fetch yet." Once you type an id, it fetches that player's summary.

## Step 4 — show both

`src/App.tsx`:

```tsx
import { LiveLeaderboard } from "./components/LiveLeaderboard";
import { PlayerDetail } from "./components/PlayerDetail";

export function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>Pixel Quest UI</h1>
      <LiveLeaderboard />
      <PlayerDetail />
    </main>
  );
}
```

## See it live

Run `npm run dev`. The leaderboard loads from the API and refreshes every 3 seconds. To watch it actually change, add a player via the API (or the Day 3 POST) and the polling leaderboard updates on its own:

```bash
curl -X POST http://localhost:8000/players \
  -H "Content-Type: application/json" \
  -d '{"username":"ui_star","country":"PK","score":9999}'
```

Within ~3s `ui_star` appears at the top — no page reload.

![The live leaderboard and the player-detail panel showing player id 1](images/03-live-data.png)

*The **Live leaderboard** polls the API every 3 seconds; typing an id into **Player detail** triggers the `skip`-gated `getPlayerSummary` query (here id `1` → `hero_07`, score 4200, rank 7).*

---

## What you achieved

- Live data via **RTK Query** hooks — no manual `fetch`/`useEffect`.
- **Polling** for near-real-time updates.
- **Conditional fetching** with `skip`.

### Deliverable for this track
Commit `api.ts`, the store, and both components. In your notes: *What did RTK Query remove compared with the manual `useEffect` fetch in React-3? What does `pollingInterval` cost on the server side?*

➡️ Next: **[../graphview/01-vis-network.md](../graphview/01-vis-network.md)**

---

## ⭐ Must-learn from this topic

- **Provider wiring** — store available app-wide.
- **Live data** — RTK Query hook replaces manual fetch/effect/loading.
- **Polling** — `pollingInterval` for auto-refresh.
- **Conditional fetch** — `skip` until input is ready.

### 📚 Official docs
- [RTK Query queries](https://redux-toolkit.js.org/rtk-query/usage/queries) — polling, skip, refetch.
- [Cache behavior](https://redux-toolkit.js.org/rtk-query/usage/cache-behavior) — sharing & invalidation.
- [FastAPI CORS](https://fastapi.tiangolo.com/tutorial/cors/) — allowing the browser to call the API.
