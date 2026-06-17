import { useState } from "react";

// A tiny stateful component: clicking the button updates state and re-renders.
export function Counter() {
  const [count, setCount] = useState(0); // [value, setter], starts at 0

  return (
    <button onClick={() => setCount(count + 1)}>
      Clicked {count} times
    </button>
  );
}
