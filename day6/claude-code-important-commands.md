# Claude Code & OpenCode — Important Commands

Source: [Agentic Coding Crash Course — Part 1: Foundations](https://agentfactory.panaversity.org/docs/agentic-coding-crash-course#part-1-foundations)

## Installation

### Claude Code
```bash
curl -fsSL https://claude.ai/install.sh | bash      # macOS / Linux
irm https://claude.ai/install.ps1 | iex             # Windows PowerShell
brew install --cask claude-code                     # macOS Homebrew
npm install -g @anthropic-ai/claude-code            # via npm
```

### OpenCode
```bash
curl -fsSL https://opencode.ai/install | bash
brew install opencode                               # macOS Homebrew
npm install -g opencode-ai                          # via npm
```

## Starting & Resuming Sessions

| Command | Function |
|---------|----------|
| `claude` / `opencode` | Start a new session in the terminal |
| `claude --resume` | Resume previous conversation (Claude Code) |
| `/sessions` or `/resume` | View saved conversations (OpenCode) |
| `/clear` or `/new` | Wipe the conversation and start fresh |
| `/compact` | Shrink conversation while keeping essentials |
| `/undo` | Reverse last AI action (OpenCode) |
| `/rewind` | Roll back to a specific prompt (Claude Code) |

## Monitoring & Configuration

| Command | Function |
|---------|----------|
| `/status` | Current model and context usage (Claude Code) |
| `/model` / `/models` | Switch or view models (Claude Code / OpenCode) |
| `/context` | Token breakdown by category (Claude Code) |
| `/init` | Auto-generate the project rules file (`CLAUDE.md` / `AGENTS.md`) |
| `/hooks` | Confirm hook registration (Claude Code) |

## Agents & Skills

| Command | Function |
|---------|----------|
| `/agents` | Create a custom subagent via guided prompt (Claude Code) |
| `opencode agent create` | Scaffold a new agent (OpenCode) |
| `@explore` | Manually invoke the exploration subagent (OpenCode) |
| `/[skill-name]` | Trigger a saved skill or command |

## Mode Switching (keyboard)

| Action | Function |
|--------|----------|
| `Shift+Tab` | Cycle permission modes (Claude Code) |
| `Tab` | Switch between Build and Plan modes (OpenCode) |

## Key Files Both Tools Read Automatically

- `.claude/settings.json` / `opencode.json` — configuration
- `CLAUDE.md` / `AGENTS.md` — project rules file
- `.claude/skills/` / `.opencode/skills/` — reusable prompts
- `.claude/agents/` / `.opencode/agents/` — custom subagents
