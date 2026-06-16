# State — Step 1: Redux Toolkit (app-wide state)

## The problem `useState` doesn't solve

`useState` is great for one component. But when **many** components need the **same** data — the leaderboard, a header showing the logged-in player, a sidebar — passing props down through every level ("prop drilling") gets painful. A **store** holds shared state in one place that any component can read.

**Redux** is the classic store. **Redux Toolkit (RTK)** is the modern, much simpler way to use it (far less boilerplate). RTK also includes **RTK Query** for fetching API data (next lesson).

---

## The pieces

- **Store** — the single object holding all shared state.
- **Slice** — a piece of the store for one feature (e.g. UI settings), with its state + the functions that change it (**reducers**).
- **Provider** — wraps your app so components can reach the store.
- **Hooks** — `useSelector` (read state) and `useDispatch` (change it).

---

## A tiny slice (UI settings)

`src/store/uiSlice.ts` — remembers how many leaderboard rows to show:

```ts
import { createSlice } from "@reduxjs/toolkit";

const uiSlice = createSlice({
  name: "ui",
  initialState: { topN: 5 },
  reducers: {
    setTopN: (state, action: { payload: number }) => {
      state.topN = action.payload;   // RTK lets you "mutate" safely (uses Immer)
    },
  },
});

export const { setTopN } = uiSlice.actions;
export default uiSlice.reducer;
```

> In plain Redux you must never mutate state; RTK uses **Immer** under the hood, so writing `state.topN = …` is safe and turns into an immutable update for you.

---

## The store

`src/store/index.ts`:

```ts
import { configureStore } from "@reduxjs/toolkit";
import uiReducer from "./uiSlice";

export const store = configureStore({
  reducer: { ui: uiReducer },
});

// types for typed hooks (TypeScript)
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

Wrap the app once, in `src/main.tsx`:

```tsx
import { Provider } from "react-redux";
import { store } from "./store";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <Provider store={store}><App /></Provider>
);
```

---

## Read and change state from a component

```tsx
import { useSelector, useDispatch } from "react-redux";
import type { RootState } from "../store";
import { setTopN } from "../store/uiSlice";

export function TopNPicker() {
  const topN = useSelector((s: RootState) => s.ui.topN);   // read
  const dispatch = useDispatch();                          // get the dispatcher
  return (
    <label>
      Show top:
      <select value={topN} onChange={(e) => dispatch(setTopN(Number(e.target.value)))}>
        <option value={3}>3</option>
        <option value={5}>5</option>
        <option value={10}>10</option>
      </select>
    </label>
  );
}
```

- `useSelector` subscribes to a slice of state — the component re-renders when it changes.
- `dispatch(setTopN(10))` sends an action; the reducer updates the store; everyone reading `topN` updates.

That's Redux Toolkit: **slice → store → provider → useSelector/useDispatch.** Next we use its data-fetching half, RTK Query.

➡️ Next: **[02-rtk-query.md](02-rtk-query.md)**

---

## ⭐ Must-learn from this topic

- **Why a store** — shared state without prop-drilling.
- **Slice** — `createSlice` (state + reducers); Immer lets you "mutate" safely.
- **Wiring** — `configureStore`, `<Provider>`.
- **Hooks** — `useSelector` to read, `useDispatch` to change.

### 📚 Official docs
- [Redux Toolkit — Quick Start](https://redux-toolkit.js.org/tutorials/quick-start) — store & slices.
- [createSlice](https://redux-toolkit.js.org/api/createSlice) — reducers & actions.
- [React Redux hooks](https://react-redux.js.org/api/hooks) — `useSelector` / `useDispatch`.
