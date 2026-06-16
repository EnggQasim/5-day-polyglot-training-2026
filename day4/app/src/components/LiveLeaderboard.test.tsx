import { render, screen } from "@testing-library/react";
import { Provider } from "react-redux";
import { http, HttpResponse } from "msw";
import { store } from "../store";
import { server } from "../test/server";
import { LiveLeaderboard } from "./LiveLeaderboard";

function renderWithStore() {
  return render(
    <Provider store={store}>
      <LiveLeaderboard />
    </Provider>
  );
}

describe("LiveLeaderboard", () => {
  it("renders players returned by the (mocked) API", async () => {
    renderWithStore();
    expect(screen.getByText("Loading…")).toBeInTheDocument();
    expect(await screen.findByText("test_hero")).toBeInTheDocument();
    expect(screen.getByText("test_mage")).toBeInTheDocument();
  });

  it("shows an error message if the API fails", async () => {
    server.use(
      http.get("http://localhost:8000/leaderboard", () =>
        HttpResponse.json({ detail: "boom" }, { status: 500 })
      )
    );
    renderWithStore();
    expect(await screen.findByText(/could not reach the api/i)).toBeInTheDocument();
  });
});
