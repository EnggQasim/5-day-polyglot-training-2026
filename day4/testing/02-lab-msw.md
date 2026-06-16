# Testing — Step 2: LAB (mock the API with MSW)

Test a component that **fetches from the API** — without running the real backend — using **MSW (Mock Service Worker)**. MSW intercepts network requests and returns fake responses you control, so tests are fast, offline, and predictable.

Files: [`app/src/test/server.ts`](../app/src/test/server.ts), [`app/src/components/LeaderboardTable.test.tsx`](../app/src/components/LeaderboardTable.test.tsx), [`app/src/components/LiveLeaderboard.test.tsx`](../app/src/components/LiveLeaderboard.test.tsx).

---

## Why MSW

`LiveLeaderboard` calls `GET http://localhost:8000/leaderboard`. In a test we don't want a real server. MSW lets you say "when that URL is called, return *this* JSON" — so you test the component's behaviour against known data.

## Step 1 — a mock server

`src/test/server.ts`:

```ts
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";

export const server = setupServer(
  http.get("http://localhost:8000/leaderboard", () =>
    HttpResponse.json([
      { rank: 1, player: "test_hero", score: 9000 },
      { rank: 2, player: "test_mage", score: 8000 },
    ])
  )
);
```

Wire it into the test setup so it runs for all tests. `src/test/setup.ts`:

```ts
import "@testing-library/jest-dom";
import { server } from "./server";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

## Step 2 — test the live component

`LiveLeaderboard` uses RTK Query, so render it inside the store `Provider`. `src/components/LiveLeaderboard.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { store } from "../store";
import { LiveLeaderboard } from "./LiveLeaderboard";

it("renders players returned by the (mocked) API", async () => {
  render(
    <Provider store={store}>
      <LiveLeaderboard />
    </Provider>
  );

  // it starts on "Loading…", then the mocked data appears
  expect(screen.getByText("Loading…")).toBeInTheDocument();
  expect(await screen.findByText("test_hero")).toBeInTheDocument();
  expect(screen.getByText("test_mage")).toBeInTheDocument();
});
```

`findByText` **waits** for the data to load (the fetch resolves with the mock), then asserts it rendered. No real API needed.

## Step 3 — test an error path

Override the handler for one test to return an error and check the fallback UI:

```tsx
import { http, HttpResponse } from "msw";
import { server } from "../test/server";

it("shows an error message if the API fails", async () => {
  server.use(
    http.get("http://localhost:8000/leaderboard", () =>
      HttpResponse.json({ detail: "boom" }, { status: 500 })
    )
  );
  render(<Provider store={store}><LiveLeaderboard /></Provider>);
  expect(await screen.findByText(/could not reach the api/i)).toBeInTheDocument();
});
```

`server.use(...)` swaps the handler just for this test; `afterEach` resets it.

## Run

```bash
cd day4/app
npm test
```

---

## What you achieved

- **RTL** render + interaction tests.
- **MSW** to mock the API — fast, offline, deterministic tests.
- Tested **loading, success, and error** paths without a real backend.

### Deliverable for this track
Commit the test files and `server.ts`. In your notes: *Why mock the network instead of calling the real API in tests? What's the difference between `getByText`, `queryByText`, and `findByText`?*

➡️ Next: **[../bi/01-connect-metabase.md](../bi/01-connect-metabase.md)**

---

## ⭐ Must-learn from this topic

- **MSW** — intercept network calls; return controlled fake responses.
- **Server lifecycle** — `listen` / `resetHandlers` / `close`.
- **Per-test overrides** — `server.use(...)` for error paths.
- **Provider in tests** — wrap RTK Query components in the store.

### 📚 Official docs
- [MSW — Getting started](https://mswjs.io/docs/getting-started) — set up mocking.
- [MSW request handlers](https://mswjs.io/docs/concepts/request-handler) — `http.get`, `HttpResponse`.
- [Testing RTK Query](https://redux-toolkit.js.org/rtk-query/usage/testing) — with MSW.
