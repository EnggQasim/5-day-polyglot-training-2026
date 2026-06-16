// Smoke test: a tiny load to confirm the script + target work before going big.
// Run:  k6 run day5/loadtest/code/smoke.js
import http from "k6/http";
import { check, sleep } from "k6";

export const options = {
  vus: 1,            // 1 virtual user
  duration: "30s",   // for 30 seconds
};

const BASE = __ENV.BASE_URL || "http://localhost:8080";

export default function () {
  const res = http.get(`${BASE}/players`);
  check(res, {
    "status is 200": (r) => r.status === 200,
    "has leaderboard": (r) => r.body.includes("leaderboard"),
  });
  sleep(1);
}
