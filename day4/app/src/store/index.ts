import { configureStore } from "@reduxjs/toolkit";
import uiReducer from "./uiSlice";
import { pqApi } from "./api";

// The single store: our UI slice + the RTK Query API.
export const store = configureStore({
  reducer: {
    ui: uiReducer,
    [pqApi.reducerPath]: pqApi.reducer,
  },
  // RTK Query's middleware enables caching, refetching, and polling.
  middleware: (getDefault) => getDefault().concat(pqApi.middleware),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
