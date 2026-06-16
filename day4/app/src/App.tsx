// import { Hello } from "./components/Hello";
// The starter app. Each Day 4 lesson swaps in the component it teaches.
// Right now it just shows a welcome heading so `npm run dev` shows something.

import { LeaderboardTable } from "./components/LeaderboardTable";

export function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>Pixel Quest UI</h1>
      <LeaderboardTable />
      <p>
        Day 4 starter. Follow the lessons to build the leaderboard, player
        detail, and friendships graph.
      </p>
    </main>
  );
}
