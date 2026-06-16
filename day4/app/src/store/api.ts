import { createApi, fetchBaseQuery } from "@reduxjs/toolkit/query/react";
import type { Player, LeaderboardRow, PlayerSummary } from "../api/types";

// One place that describes the Day 3 FastAPI endpoints.
// RTK Query generates a typed hook for each one, with caching built in.
export const pqApi = createApi({
  reducerPath: "pqApi",
  baseQuery: fetchBaseQuery({ baseUrl: "http://localhost:8000" }),
  endpoints: (build) => ({
    getPlayers: build.query<Player[], void>({
      query: () => "/players",
    }),
    getLeaderboard: build.query<LeaderboardRow[], number>({
      query: (top) => `/leaderboard?top=${top}`,
    }),
    getPlayerSummary: build.query<PlayerSummary, number>({
      query: (id) => `/players/${id}/summary`,
    }),
  }),
});

export const {
  useGetPlayersQuery,
  useGetLeaderboardQuery,
  useGetPlayerSummaryQuery,
} = pqApi;
