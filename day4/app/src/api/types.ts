// Shared TypeScript types describing the shapes the Day 3 API returns.
// Typing API data once, here, means every component gets autocomplete and
// the compiler catches typos like `player.scor`.

export interface Player {
  player_id: number;
  username: string;
  country: string;
  score: number;
}

export interface LeaderboardRow {
  rank: number;
  player: string;
  score: number;
}

export interface PlayerSummary {
  username: string;
  score: number;
  rank: number | null;
}
