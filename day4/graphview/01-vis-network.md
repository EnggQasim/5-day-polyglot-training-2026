# Graph View — Step 1: Drawing a network with Vis.js

## Why a graph view

Some data *is* a graph — the Neo4j **friendships** from Day 1. A table can't show "who is connected to whom" at a glance, but a **network diagram** can: dots (nodes) joined by lines (edges). **Vis.js** (`vis-network`) draws interactive networks in the browser — drag nodes, zoom, click them.

---

## The two inputs Vis.js needs

1. **nodes** — `{ id, label }` for each dot.
2. **edges** — `{ from, to }` for each line.

```ts
const nodes = [
  { id: 1, label: "hero_07" },
  { id: 2, label: "mage_lily" },
  { id: 3, label: "elf_mona" },
];
const edges = [
  { from: 1, to: 2 },   // hero_07 — mage_lily
  { from: 2, to: 3 },   // mage_lily — elf_mona
];
```

---

## Drawing it inside React

Vis.js draws into a real DOM element, so we use a **`ref`** (a handle to a div) plus a `useEffect` to create the network after render.

`src/components/GraphView.tsx`:

```tsx
import { useEffect, useRef } from "react";
import { Network } from "vis-network";
import { DataSet } from "vis-data";

export function GraphView() {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const nodes = new DataSet([
      { id: 1, label: "hero_07" },
      { id: 2, label: "mage_lily" },
      { id: 3, label: "elf_mona" },
    ]);
    const edges = new DataSet([
      { from: 1, to: 2 },
      { from: 2, to: 3 },
    ]);

    const network = new Network(containerRef.current, { nodes, edges }, {
      nodes: { shape: "dot", size: 16 },
      physics: { stabilization: true },
    });

    return () => network.destroy();   // clean up when the component unmounts
  }, []);

  return <div ref={containerRef} style={{ height: 400, border: "1px solid #ccc" }} />;
}
```

![A three-node Vis.js network: hero_07 — mage_lily — elf_mona](images/01-network.png)

*Vis.js draws the three nodes and two edges into the `<div>`, then its physics engine lays them out automatically. You can drag the dots and zoom with the wheel.*

Key points:
- **`ref`** gives Vis.js the `<div>` to draw into.
- The `useEffect` runs once (`[]`); we build the network there.
- **`return () => network.destroy()`** is cleanup — React calls it when the component goes away, so we don't leak networks.
- The third argument is **options** (node shape/size, physics for the auto-layout).

## Make it interactive

Vis.js emits events. Log clicks on a node:

```tsx
network.on("click", (params) => {
  if (params.nodes.length > 0) {
    console.log("clicked node id:", params.nodes[0]);
  }
});
```

In the lab we use this to show the clicked player's details.

➡️ Next: the lab — **[02-lab-friendships.md](02-lab-friendships.md)**

---

## ⭐ Must-learn from this topic

- **nodes + edges** — `{id,label}` and `{from,to}` feed the network.
- **`ref` + `useEffect`** — the pattern for using a non-React DOM library.
- **Cleanup** — `return () => network.destroy()` to avoid leaks.
- **Events** — `network.on("click", …)` to react to clicks.

### 📚 Official docs
- [vis-network docs](https://visjs.github.io/vis-network/docs/network/) — options & methods.
- [vis-network examples](https://visjs.github.io/vis-network/examples/) — recipes.
- [React refs (`useRef`)](https://react.dev/reference/react/useRef) — DOM access.
