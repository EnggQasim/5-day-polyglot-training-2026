import React from "react";
import ReactDOM from "react-dom/client";
import { App } from "./App";

// The entry point: mount the <App /> into the #root div from index.html.
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
