# Testing — Step 1: React Testing Library

## Why test the UI

Tests catch breakage automatically: rename a field or break a component and a test fails *before* users do. For React we use **React Testing Library (RTL)** with a test runner. (The original curriculum names **Jest**; our Vite project uses **Vitest**, which has the *same* API — `describe`, `it`, `expect` — so everything you learn applies to both. We note Jest equivalents where relevant.)

RTL's philosophy: **test what the user sees and does**, not internal implementation. You find elements by their visible text/role and simulate real interactions.

---

## A first render test

Test the static `LeaderboardTable` from the React lab. `src/components/LeaderboardTable.test.tsx`:

```tsx
import { render, screen } from "@testing-library/react";
import { LeaderboardTable } from "./LeaderboardTable";

describe("LeaderboardTable", () => {
  it("shows the heading and top players", () => {
    render(<LeaderboardTable />);
    expect(screen.getByText("Leaderboard")).toBeInTheDocument();
    expect(screen.getByText("elf_mona")).toBeInTheDocument();
  });
});
```

- **`render(...)`** draws the component into a virtual DOM (jsdom).
- **`screen.getByText(...)`** finds an element by its visible text.
- **`expect(...).toBeInTheDocument()`** is the assertion (from `@testing-library/jest-dom`, wired in `src/test/setup.ts`).

Run the tests:

```bash
cd day4/app
npm test
```

---

## Testing interaction

Simulate a click and check the result, using `user-event`:

```tsx
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LeaderboardTable } from "./LeaderboardTable";

it("toggles between top 3 and all", async () => {
  const user = userEvent.setup();
  render(<LeaderboardTable />);

  // initially only 3 rows -> the 4th player is not shown
  expect(screen.queryByText("knight_max")).not.toBeInTheDocument();

  await user.click(screen.getByRole("button", { name: /show all/i }));

  // after clicking, the 4th player appears
  expect(screen.getByText("knight_max")).toBeInTheDocument();
});
```

- **`userEvent`** simulates real user actions (clicks, typing).
- **`getByRole("button", { name: /show all/i })`** finds the button by its role + accessible name — robust and accessibility-friendly.
- **`queryBy…`** returns `null` if not found (use it to assert absence); **`getBy…`** throws if missing.

---

## Query cheat-sheet

- `getByText` / `getByRole` — must exist (throws otherwise).
- `queryByText` — may not exist (returns `null`; for "should NOT be there").
- `findByText` — async; waits for it to appear (for data that loads).

Next we test a component that fetches from the API — without a real backend — using **MSW**.

➡️ Next: the lab — **[02-lab-msw.md](02-lab-msw.md)**

---

## ⭐ Must-learn from this topic

- **RTL philosophy** — test what the user sees (text/role), not internals.
- **`render` + `screen`** — draw a component, then query it.
- **`userEvent`** — simulate real clicks/typing.
- **getBy / queryBy / findBy** — must-exist / may-be-absent / async-wait.

### 📚 Official docs
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) — core API.
- [Queries](https://testing-library.com/docs/queries/about/) — getBy/queryBy/findBy.
- [Vitest](https://vitest.dev/) (Jest-compatible API) / [Jest](https://jestjs.io/docs/getting-started).
