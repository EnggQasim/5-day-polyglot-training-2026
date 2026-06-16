import { useEffect, useRef, useState } from "react";
import { Network } from "vis-network";
import { DataSet } from "vis-data";

// The Day 1 friendship pairs (same as day1/neo4j/data/friendships.csv).
// Inline so the lab runs without the API; see the lesson for loading them live.
const PAIRS: [string, string][] = [
  ["hero_07", "mage_lily"],
  ["hero_07", "tank_omar"],
  ["mage_lily", "ninja_sara"],
  ["ninja_sara", "archer_zoe"],
  ["archer_zoe", "knight_max"],
  ["knight_max", "giant_sam"],
  ["giant_sam", "elf_mona"],
  ["tank_omar", "ninja_sara"],
  ["hero_07", "archer_zoe"],
];

export function FriendshipsGraph() {
  const ref = useRef<HTMLDivElement>(null);
  const [selected, setSelected] = useState<string | null>(null);

  useEffect(() => {
    if (!ref.current) return;

    const names = Array.from(new Set(PAIRS.flat()));
    const idOf = new Map(names.map((n, i) => [n, i + 1]));
    const nodes = new DataSet(names.map((n) => ({ id: idOf.get(n)!, label: n })));
    const edges = new DataSet(PAIRS.map(([a, b]) => ({ from: idOf.get(a)!, to: idOf.get(b)! })));

    const network = new Network(
      ref.current,
      { nodes, edges },
      { nodes: { shape: "dot", size: 16 }, physics: { stabilization: true } }
    );

    network.on("click", (params: { nodes: number[] }) => {
      const id = params.nodes[0];
      setSelected(id ? (nodes.get(id) as { label: string }).label : null);
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
