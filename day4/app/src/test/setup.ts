// Vitest setup: jest-dom matchers + the MSW mock server lifecycle.
import "@testing-library/jest-dom";
import { server } from "./server";

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
