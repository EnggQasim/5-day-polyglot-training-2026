import { useSelector, useDispatch } from "react-redux";
import type { RootState } from "../store";
import { setTopN } from "../store/uiSlice";

// Reads shared UI state (topN) from the store and changes it via dispatch.
export function TopNPicker() {
  const topN = useSelector((s: RootState) => s.ui.topN); // read
  const dispatch = useDispatch(); // get the dispatcher
  return (
    <label>
      Show top:{" "}
      <select
        value={topN}
        onChange={(e) => dispatch(setTopN(Number(e.target.value)))}
      >
        <option value={3}>3</option>
        <option value={5}>5</option>
        <option value={10}>10</option>
      </select>
      <span style={{ marginLeft: 12 }}>Current topN in store: <strong>{topN}</strong></span>
    </label>
  );
}
