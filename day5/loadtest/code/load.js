// A staged load test with thresholds (pass/fail criteria).
// Run:  k6 run day5/loadtest/code/load.js
import http from "k6/http";
import { check } from "k6";

export const options = {
  // ramp virtual users up, hold, then down
  stages: [
    { duration: "30s", target: 50 },   // ramp to 50 VUs
    { duration: "1m", target: 50 },    // hold at 50
    { duration: "30s", target: 0 },    // ramp down
  ],
  // the test FAILS if these aren't met
  thresholds: {
    http_req_duration: ["p(95)<500"],   // 95% of requests under 500ms
    http_req_failed: ["rate<0.01"],     // less than 1% errors
  },
};

const BASE = __ENV.BASE_URL || "http://localhost:8080";

export default function () {
  // hit /work so CPU rises and the HPA reacts
  const res = http.get(`${BASE}/work?n=20000`);
  check(res, { "status is 200": (r) => r.status === 200 });
}
