import http from "k6/http";
import { check } from "k6";

export const options = {
  scenarios: {
    steady: {
      executor: "constant-arrival-rate",
      rate: 1000,
      timeUnit: "1s",
      duration: "60s",
      preAllocatedVUs: 50,
      maxVUs: 500,
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.001"],
    http_req_duration: ["p(95)<250"],
  },
};

const baseUrl = __ENV.BASE_URL || "http://127.0.0.1:8080";

export default function () {
  const response = http.get(`${baseUrl}/healthz`, {
    tags: { endpoint: "healthz" },
  });
  check(response, {
    "status is 200": (result) => result.status === 200,
    "contract is ok": (result) => result.json("status") === "ok",
  });
}
