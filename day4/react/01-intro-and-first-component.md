# React — Step 1: What it is, and your first component

## What is React?

**React** is a JavaScript library for building **user interfaces** out of small, reusable pieces called **components**. Instead of manually changing the page when data changes, you describe *what the UI should look like for some data*, and React updates the screen for you.

We pair it with **TypeScript** (typed JavaScript) so the editor catches mistakes — like using a field that doesn't exist — before you ever run the code.

We build and run with **Vite**, a fast dev server: save a file and the browser updates instantly.

We use React when:
- The UI has **changing data** (a leaderboard that updates).
- We want **reusable pieces** (one `PlayerRow` used many times).
- Many people work on the same front-end and need structure.

## A component is just a function

A React component is a function that returns markup (called **JSX** — it looks like HTML inside JavaScript).

Open `day4/app/src/App.tsx` (created in setup):

```tsx
export function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>Pixel Quest UI</h1>
      <p>Day 4 starter.</p>
    </main>
  );
}
```

- The function **returns JSX**. `<h1>` and `<main>` look like HTML but are JavaScript.
- `style={{ ... }}` passes a JS object (note the double braces).
- The component is **exported** so other files can use it.

`src/main.tsx` mounts it into the page:

```tsx
ReactDOM.createRoot(document.getElementById("root")!).render(<App />);
```

`<App />` is how you *use* a component — like a custom HTML tag.

## Run it

```bash
cd day4/app
npm install      # first time only
npm run dev
```

Open **http://localhost:5173**. Edit the `<h1>` text, save, and watch the browser update instantly (hot reload).

## Make your own component

Create `src/components/Hello.tsx`:

```tsx
export function Hello() {
  return <p>Welcome, hero!</p>;
}
```

Use it inside `App.tsx`:

```tsx
import { Hello } from "./components/Hello";

export function App() {
  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>Pixel Quest UI</h1>
      <Hello />
    </main>
  );
}
```

That is the core loop of React: **write a function that returns JSX, then use it as a tag.** Everything else builds on this.

![The Pixel Quest UI in the browser showing the heading and the Hello component](images/01-hello.png)

*The browser at **http://localhost:5173** — `<App />` renders the `<h1>` heading and the `<Hello />` component you just wrote.*

> **JSX rules to remember:** return a single top-level element (wrap siblings in one parent or `<>…</>`), use `className` instead of `class`, and close every tag (`<img />`).

➡️ Next: **[02-props-state-lists.md](02-props-state-lists.md)** — pass data in, and render a list.

---

## ⭐ Must-learn from this topic

- **Component = function returning JSX** — used as `<App />`.
- **JSX rules** — one root element, `className`, close every tag, `{}` for JS.
- **Vite** — `npm run dev`, hot reload at `:5173`.
- **Import/export** — split UI into files.

### 📚 Official docs
- [React — Quick Start](https://react.dev/learn) — components & JSX.
- [Describing the UI](https://react.dev/learn/describing-the-ui) — JSX in depth.
- [Vite guide](https://vitejs.dev/guide/) — the dev server & build.
