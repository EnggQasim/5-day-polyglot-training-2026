# Graph View — Step 2: LAB (the friendships explorer)

Build an interactive **friendships network** for Pixel Quest. Nodes are players, edges are friendships, and clicking a node shows who it is. Component: [`app/src/components/FriendshipsGraph.tsx`](../app/src/components/FriendshipsGraph.tsx).

We use the Day 1 friendships (the same pairs from `day1/neo4j/data/friendships.csv`). For the lab we include them inline so it runs without the API; the "next step" note shows how to load them live.

---

## The component

```tsx
import { useEffect, useRef, useState } from "react";
import { Network } from "vis-network";
import { DataSet } from "vis-data";

// the Day 1 friendship pairs
const PAIRS: [string, string][] = [
  ["hero_07", "mage_lily"], ["hero_07", "tank_omar"], ["mage_lily", "ninja_sara"],
  ["ninja_sara", "archer_zoe"], ["archer_zoe", "knight_max"], ["knight_max", "giant_sam"],
  ["giant_sam", "elf_mona"], ["tank_omar", "ninja_sara"], ["hero_07", "archer_zoe"],
];

export function FriendshipsGraph() {
  const ref = useRef<HTMLDivElement>(null);
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    if (!ref.current) return;

    // build a unique node id per player name
    const names = Array.from(new Set(PAIRS.flat()));
    const idOf = new Map(names.map((n, i) => [n, i + 1]));
    const nodes = new DataSet(names.map((n) => ({ id: idOf.get(n)!, label: n })));
    const edges = new DataSet(PAIRS.map(([a, b]) => ({ from: idOf.get(a)!, to: idOf.get(b)! })));

    const network = new Network(ref.current, { nodes, edges }, {
      nodes: { shape: "dot", size: 16 },
      physics: { stabilization: true },
    });

    network.on("click", (params) => {
      const id = params.nodes[0];
      setSelected(id ? (nodes.get(id) as any).label : null);
    });

    return () => network.destroy();
  }, []);

  return (
    <section>
      <h2>Friendships</h2>
      <div ref={ref} style={{ height: 420, border: "1px solid #ccc" }} />
      <p>{selected ? `Selected: ${selected}` : "Click a player to select."}</p>
    </section>
  );
}
```

## Show it

`src/App.tsx`:

```tsx
import { FriendshipsGraph } from "./components/FriendshipsGraph";
// ... <FriendshipsGraph /> inside <main>
```

Run `npm run dev`: drag the dots, zoom with the wheel, and click a player to see their name below the graph.

![The friendships network: eight players connected by friendship edges](images/02-friendships.png)

*The nine Day 1 friendship pairs become a network of eight players. The physics layout pulls connected players together — `ninja_sara` and `archer_zoe` sit central because they have the most friends. Clicking a node sets the "Selected:" line below.*

---

## Next step — load friendships from the API (optional)

To make it live, add a `/friends` endpoint to the Day 3 API that returns `[["hero_07","mage_lily"], …]` (query Neo4j or Postgres), expose it in `api.ts` as an RTK Query endpoint, and replace the inline `PAIRS` with the fetched data. The drawing code stays the same.

---

## What you achieved

- An **interactive network** built with Vis.js inside React.
- Correct **ref + useEffect + cleanup** pattern for a non-React library.
- **Click events** wired to React state (selected player).

### Deliverable for this track
Commit `FriendshipsGraph.tsx`. In your notes: *Why did we need a `ref` and a cleanup function here, unlike the leaderboard table? When is a graph view clearer than a table?*

➡️ Next: **[../testing/01-jest-rtl.md](../testing/01-jest-rtl.md)**

---

## ⭐ Must-learn from this topic

- **Graph from pairs** — derive unique nodes, map names→ids, build edges.
- **Interaction → state** — click event sets React state.
- **Library + React** — ref to draw, cleanup to tear down.
- **Going live** — swap inline data for an API/RTK Query feed.

### 📚 Official docs
- [vis-network — nodes](https://visjs.github.io/vis-network/docs/network/nodes.html) and [edges](https://visjs.github.io/vis-network/docs/network/edges.html).
- [vis-data DataSet](https://visjs.github.io/vis-data/data/dataset.html) — the data containers.
- [Manipulating the DOM with refs](https://react.dev/learn/manipulating-the-dom-with-refs).
