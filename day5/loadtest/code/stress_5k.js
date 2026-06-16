// Stress test toward 5,000 concurrent virtual users.
// Run:  k6 run day5/loadtest/code/stress_5k.js
//
// NOTE: 5,000 VUs from one laptop is heavy on the CLIENT too. If your machine
// struggles, lower the target (e.g. 1000) — the point is to SEE the system
// scale and read the metrics, not to win a benchmark. In production you'd run
// k6 distributed / in the cloud.
import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    ramp_to_5k: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "1m", target: 1000 },   // warm up
        { duration: "2m", target: 5000 },   // climb to 5,000 concurrent VUs
        { duration: "2m", target: 5000 },   // hold at 5,000
        { duration: "1m", target: 0 },      // ramp down
      ],
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.05"],       // tolerate <5% errors under extreme load
    http_req_duration: ["p(95)<2000"],    // 95% under 2s at peak
  },
};

const BASE = __ENV.BASE_URL || "http://localhost:8080";

export default function () {
  const res = http.get(`${BASE}/work?n=20000`);
  check(res, { "status is 200": (r) => r.status === 200 });
}
