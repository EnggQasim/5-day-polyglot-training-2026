import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

// MSW mock server: intercepts API calls during tests and returns fake data,
// so tests run fast and offline (no real backend needed).
export const server = setupServer(
  http.get("http://localhost:8000/leaderboard", () =>
    HttpResponse.json([
      { rank: 1, player: "test_hero", score: 9000 },
      { rank: 2, player: "test_mage", score: 8000 },
    ])
  )
);
