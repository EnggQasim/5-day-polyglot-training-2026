import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

// A small slice of shared UI state: how many leaderboard rows to show.
const uiSlice = createSlice({
  name: "ui",
  initialState: { topN: 5 },
  reducers: {
    setTopN: (state, action: PayloadAction<number>) => {
      state.topN = action.payload; // safe "mutation" thanks to Immer (built into RTK)
    },
  },
});

export const { setTopN } = uiSlice.actions;
export default uiSlice.reducer;
