# React — Step 4: LAB (the leaderboard table)

Build a reusable, typed **leaderboard table** from React fundamentals only (props, lists, state) — no Redux yet. We use static data here; the next section makes it live from the API.

Files (in `day4/app/src/components/`): [`PlayerRow.tsx`](../app/src/components/PlayerRow.tsx) and [`LeaderboardTable.tsx`](../app/src/components/LeaderboardTable.tsx).

---

## Step 1 — a row component

`PlayerRow.tsx` renders one `<tr>` from typed props:

```tsx
import type { LeaderboardRow } from "../api/types";

export function PlayerRow({ rank, player, score }: LeaderboardRow) {
  return (
    <tr>
      <td>{rank}</td>
      <td>{player}</td>
      <td style={{ textAlign: "right" }}>{score}</td>
    </tr>
  );
}
```

## Step 2 — the table with a top-N toggle (state)

`LeaderboardTable.tsx` maps rows and uses **state** for a "show 3 / show all" toggle:

```tsx
import { useState } from "react";
import type { LeaderboardRow } from "../api/types";
import { PlayerRow } from "./PlayerRow";

const DATA: LeaderboardRow[] = [
  { rank: 1, player: "elf_mona", score: 7300 },
  { rank: 2, player: "ninja_sara", score: 6700 },
  { rank: 3, player: "giant_sam", score: 6200 },
  { rank: 4, player: "knight_max", score: 5600 },
  { rank: 5, player: "mage_lily", score: 5100 },
];

export function LeaderboardTable() {
  const [showAll, setShowAll] = useState(false);
  const rows = showAll ? DATA : DATA.slice(0, 3);

  return (
    <section>
      <h2>Leaderboard</h2>
      <table>
        <thead><tr><th>#</th><th>Player</th><th>Score</th></tr></thead>
        <tbody>
          {rows.map((r) => <PlayerRow key={r.player} {...r} />)}
        </tbody>
      </table>
      <button onClick={() => setShowAll(!showAll)}>
        {showAll ? "Show top 3" : "Show all"}
      </button>
    </section>
  );
}
```

`{...r}` spreads the row object into props (so `rank`, `player`, `score` all pass through). The button flips `showAll` state, and React re-renders with more/fewer rows.

## Step 3 — show it

In `src/App.tsx`:

```tsx
import { LeaderboardTable } from "./components/LeaderboardTable";

export function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>Pixel Quest UI</h1>
      <LeaderboardTable />
    </main>
  );
}
```

Run `npm run dev`, open http://localhost:5173, and click the toggle.

| Initial (top 3) | After clicking **Show all** |
|---|---|
| ![Leaderboard table showing the top three players](images/04-leaderboard-top3.png) | ![Leaderboard table expanded to show all five players](images/04-leaderboard-all.png) |

*The button flips the `showAll` **state**; React re-renders the table with three rows or all five, and the label switches between "Show all" and "Show top 3".*

---

## What you achieved

- A **reusable, typed** row component used via `.map()` with keys.
- **State** driving the UI (the show-all toggle).
- A clean parent/child split (`LeaderboardTable` → `PlayerRow`).

### Deliverable for this track
Commit the two components. In your notes: *What is a `key` for, and what goes wrong without one? Which data here is props and which is state?*

➡️ Next: **[../state/01-redux-toolkit.md](../state/01-redux-toolkit.md)** — manage app-wide state and fetch real data.

---

## ⭐ Must-learn from this topic

- **Composition** — a parent table renders many typed row components.
- **`{...r}` spread** — pass an object's fields as props.
- **State-driven UI** — a toggle changes what renders.
- **Keys** — stable keys on mapped lists.

### 📚 Official docs
- [Your First Component](https://react.dev/learn/your-first-component) and [Rendering lists](https://react.dev/learn/rendering-lists).
- [Responding to events](https://react.dev/learn/responding-to-events) — `onClick`.
- [Sharing state](https://react.dev/learn/sharing-state-between-components) — lifting state up.
