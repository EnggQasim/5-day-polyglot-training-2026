import { useState } from "react";
import { useGetPlayerSummaryQuery } from "../store/api";

// Loads one player's summary when you type an id.
// `skip` means RTK Query won't fetch until an id is chosen.
export function PlayerDetail() {
  const [id, setId] = useState<number | null>(null);
  const { data, isFetching } = useGetPlayerSummaryQuery(id!, { skip: id === null });

  return (
    <section>
      <h2>Player detail</h2>
      <label>
        Player id:{" "}
        <input
          type="number"
          onChange={(e) => setId(e.target.value ? Number(e.target.value) : null)}
        />
      </label>
      {isFetching && <p>Loading…</p>}
      {data && (
        <p>
          <strong>{data.username}</strong> — score {data.score}, rank {data.rank ?? "—"}
        </p>
      )}
    </section>
  );
}
