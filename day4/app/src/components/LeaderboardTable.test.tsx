import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LeaderboardTable } from "./LeaderboardTable";

describe("LeaderboardTable", () => {
  it("shows the heading and top players", () => {
    render(<LeaderboardTable />);
    expect(screen.getByText("Leaderboard")).toBeInTheDocument();
    expect(screen.getByText("elf_mona")).toBeInTheDocument();
  });

  it("toggles between top 3 and all", async () => {
    const user = userEvent.setup();
    render(<LeaderboardTable />);

    // only 3 rows at first -> the 4th player is hidden
    expect(screen.queryByText("knight_max")).not.toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: /show all/i }));

    expect(screen.getByText("knight_max")).toBeInTheDocument();
  });
});
