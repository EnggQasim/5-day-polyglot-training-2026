# React — Step 2: Props, state, and rendering lists

Three everyday skills: pass data into a component (**props**), let a component remember changing data (**state**), and turn an array into UI (**lists**).

---

## Props — passing data in

**Props** are the inputs to a component, like function arguments. With TypeScript we describe their shape so misuse is caught immediately.

`src/components/PlayerRow.tsx`:

```tsx
interface PlayerRowProps {
  rank: number;
  username: string;
  score: number;
}

export function PlayerRow({ rank, username, score }: PlayerRowProps) {
  return (
    <tr>
      <td>{rank}</td>
      <td>{username}</td>
      <td>{score}</td>
    </tr>
  );
}
```

- `PlayerRowProps` says exactly what this component needs.
- We pass props like HTML attributes: `<PlayerRow rank={1} username="elf_mona" score={7300} />`.
- If you forget `score` or pass a string, TypeScript complains.

---

## Rendering a list with `.map()`

To show many rows, map an array to components. Each item needs a unique **`key`** so React can track it.

```tsx
const players = [
  { username: "elf_mona", score: 7300 },
  { username: "ninja_sara", score: 6700 },
  { username: "giant_sam", score: 6200 },
];

export function Leaderboard() {
  return (
    <table>
      <thead>
        <tr><th>#</th><th>Player</th><th>Score</th></tr>
      </thead>
      <tbody>
        {players.map((p, i) => (
          <PlayerRow key={p.username} rank={i + 1} username={p.username} score={p.score} />
        ))}
      </tbody>
    </table>
  );
}
```

`{players.map(...)}` produces an array of `<PlayerRow>` elements. The `key={p.username}` helps React update efficiently — always give list items a stable key.

---

## State — data that changes

**State** is data a component remembers between renders. When state changes, React re-renders the component. You create it with the **`useState`** hook.

`src/components/Counter.tsx`:

```tsx
import { useState } from "react";

export function Counter() {
  const [count, setCount] = useState(0);   // [value, setter], starts at 0

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
```

- `useState(0)` returns the current value and a setter.
- Calling `setCount(...)` updates the value **and** re-renders — you never touch the DOM yourself.
- Never assign `count = ...` directly; always use the setter.

---

![The leaderboard list rendered from props, and the Counter button after three clicks](images/02-props-state-lists.png)

*Left to right in the browser: the `players` array mapped to `<PlayerRow>` items (props + lists), and the `<Counter>` showing **state** after three clicks.*

## Props vs state (remember this)

- **Props** come **from the parent** and are read-only inside the component.
- **State** is **owned by the component** and changes over time.

A leaderboard's data might arrive as props; a "show top 5 / top 10" toggle would be state.

➡️ Next: **[03-hooks-and-types.md](03-hooks-and-types.md)** — more hooks and how to type them.

---

## ⭐ Must-learn from this topic

- **Props** — typed inputs from the parent; read-only.
- **Rendering lists** — `.map()` + a stable **`key`**.
- **State** — `useState`; update via the setter, never mutate directly.
- **Props vs state** — from-parent vs owned-and-changing.

### 📚 Official docs
- [Passing props](https://react.dev/learn/passing-props-to-a-component) and [Rendering lists](https://react.dev/learn/rendering-lists).
- [State: a component's memory](https://react.dev/learn/state-a-components-memory) — `useState`.
- [TypeScript with React](https://react.dev/learn/typescript) — typing props & state.
