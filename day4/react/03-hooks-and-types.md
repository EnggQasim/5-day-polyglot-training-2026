# React — Step 3: Hooks and TypeScript types

## What is a hook?

A **hook** is a function starting with `use…` that lets a component "hook into" React features — state, side effects, context, etc. You met `useState`. The other everyday one is **`useEffect`**.

**Rules of hooks (important):** only call hooks at the **top level** of a component (not inside loops, conditions, or nested functions), and only from React components or other hooks.

---

## `useEffect` — run code after render (e.g. fetch data)

`useEffect` runs a function *after* the component renders. It's where you do side effects like fetching from an API. Here we fetch the leaderboard from the Day 3 API directly with `fetch` (tomorrow's RTK Query lesson does this more cleanly):

```tsx
import { useState, useEffect } from "react";
import type { LeaderboardRow } from "../api/types";

export function LiveLeaderboard() {
  const [rows, setRows] = useState<LeaderboardRow[]>([]);   // typed state
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/leaderboard?top=5")
      .then((res) => res.json())
      .then((data: LeaderboardRow[]) => {
        setRows(data);
        setLoading(false);
      });
  }, []);   // empty [] = run once, after the first render

  if (loading) return <p>Loading…</p>;
  return <ul>{rows.map((r) => <li key={r.player}>{r.rank}. {r.player} — {r.score}</li>)}</ul>;
}
```

![The live leaderboard list fetched from the Day 3 API with useEffect](images/03-useeffect-live.png)

*After the first render, `useEffect` fetches `GET /leaderboard?top=5` from the Day 3 API and the list appears (the brief "Loading…" is replaced by the data).*

Key points:
- The **dependency array** `[]` controls when the effect runs. `[]` = once. `[playerId]` = whenever `playerId` changes.
- We set `loading` state so the UI shows "Loading…" then the data.

---

## Typing things with TypeScript

TypeScript types make components safer. Common patterns:

**Typed state** — tell `useState` what it holds:
```tsx
const [rows, setRows] = useState<LeaderboardRow[]>([]);   // array of LeaderboardRow
const [player, setPlayer] = useState<Player | null>(null); // a Player or nothing yet
```

**Typed props** — an interface (from lesson 2):
```tsx
interface PlayerRowProps { rank: number; username: string; score: number; }
```

**Reusing API types** — we defined `Player`, `LeaderboardRow`, `PlayerSummary` once in `src/api/types.ts`. Import them everywhere instead of redefining:
```tsx
import type { Player } from "../api/types";
```

**Why bother:** if the API field is `score` and you type `row.scor`, the editor flags it immediately — you fix bugs while typing, not at runtime.

---

## Putting it together

A typical data component combines all of it: typed state for the data + a loading flag, a `useEffect` to fetch, and a `.map()` to render the list — exactly the shape of `LiveLeaderboard` above. In the next lesson we replace the manual `fetch`/`useEffect`/loading dance with **RTK Query**, which does it for you.

➡️ Next: the lab — **[04-lab-leaderboard-table.md](04-lab-leaderboard-table.md)**

---

## ⭐ Must-learn from this topic

- **Hooks rules** — top level only, from components/hooks.
- **`useEffect`** — run after render; the dependency array controls when.
- **Typed state** — `useState<Player | null>(null)`, `useState<Row[]>([])`.
- **Shared API types** — define once in `api/types.ts`, import everywhere.

### 📚 Official docs
- [Synchronizing with Effects](https://react.dev/learn/synchronizing-with-effects) — `useEffect`.
- [Built-in Hooks](https://react.dev/reference/react/hooks) — the full list.
- [TypeScript with React](https://react.dev/learn/typescript) — typing hooks.
