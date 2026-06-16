import { useState } from "react";
import type { LeaderboardRow } from "../api/types";
import { PlayerRow } from "./PlayerRow";

// Static sample data for the React-fundamentals lab.
// (The state/ section replaces this with live API data via RTK Query.)
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
        <thead>
          <tr><th>#</th><th>Player</th><th>Score</th></tr>
        </thead>
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
