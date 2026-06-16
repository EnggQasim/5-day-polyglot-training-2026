import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite config for the Pixel Quest UI.
// The `test` block lets Vitest run with a browser-like (jsdom) environment.
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: "./src/test/setup.ts",
  },
});
