import type { LeaderboardRow } from "../api/types";

// One leaderboard row. Props are the LeaderboardRow shape (rank, player, score).
export function PlayerRow({ rank, player, score }: LeaderboardRow) {
  return (
    <tr>
      <td>{rank}</td>
      <td>{player}</td>
      <td style={{ textAlign: "right" }}>{score}</td>
    </tr>
  );
}
