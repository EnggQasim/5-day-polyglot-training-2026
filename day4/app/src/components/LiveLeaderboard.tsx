import { useGetLeaderboardQuery } from "../store/api";
import { PlayerRow } from "./PlayerRow";

// Live leaderboard from the Day 3 API, refreshed every 3 seconds.
export function LiveLeaderboard() {
  const { data, isLoading, error } = useGetLeaderboardQuery(5, { pollingInterval: 3000 });

  if (isLoading) return <p>Loading…</p>;
  if (error) return <p>Could not reach the API. Is it running on :8000 (and CORS enabled)?</p>;

  return (
    <section>
      <h2>Live leaderboard</h2>
      <table>
        <thead><tr><th>#</th><th>Player</th><th>Score</th></tr></thead>
        <tbody>{data!.map((r) => <PlayerRow key={r.player} {...r} />)}</tbody>
      </table>
    </section>
  );
}
