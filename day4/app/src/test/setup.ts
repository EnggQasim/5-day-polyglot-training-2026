// Vitest setup: jest-dom matchers + the MSW mock server lifecycle.
import "@testing-library/jest-dom";
import { server } from "./server";
import { store } from "../store";
import { pqApi } from "../store/api";

// --- Node 18+/jsdom compatibility shim (not needed in a browser) ---
// RTK Query builds a `Request` carrying jsdom's AbortSignal, but Node's
// fetch (undici) only accepts its own AbortSignal and throws
// "Expected signal to be an instance of AbortSignal". We don't need request
// cancellation in tests, so drop the signal when a Request is constructed.
const RealRequest = globalThis.Request;
class PatchedRequest extends RealRequest {
  constructor(input: RequestInfo | URL, init?: RequestInit) {
    if (init && "signal" in init) {
      const { signal, ...rest } = init;
      super(input, rest);
    } else {
      super(input, init);
    }
  }
}
globalThis.Request = PatchedRequest as unknown as typeof Request;

beforeAll(() => server.listen());
afterEach(() => {
  server.resetHandlers();
  // Clear RTK Query's cache so each test starts fresh (the store is a singleton,
  // so a cached success would otherwise leak into the next test).
  store.dispatch(pqApi.util.resetApiState());
});
afterAll(() => server.close());
