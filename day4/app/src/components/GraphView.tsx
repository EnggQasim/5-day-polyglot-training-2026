import { useEffect, useRef } from "react";
import { Network } from "vis-network";
import { DataSet } from "vis-data";

// A minimal Vis.js network: three players, two friendships.
// Shows the ref + useEffect + cleanup pattern for a non-React DOM library.
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

    const network = new Network(
      containerRef.current,
      { nodes, edges },
      { nodes: { shape: "dot", size: 16 }, physics: { stabilization: true } }
    );

    return () => network.destroy(); // clean up when the component unmounts
  }, []);

  return <div ref={containerRef} style={{ height: 400, border: "1px solid #ccc" }} />;
}
