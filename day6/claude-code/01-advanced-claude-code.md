# Claude Code — Step 1: Advanced use

You've used Claude Code to ask questions and edit files. These features make it dramatically more useful on a real project like yours.

---

## 1. `CLAUDE.md` — give Claude your project's rulebook

Claude Code automatically reads a file named **`CLAUDE.md`** at the repo root (and in subfolders) as standing context. Put the things you'd tell a new teammate:

```markdown
# Project: GeoSim Platform
- Stack: GeoServer, PostGIS, Redis, Neo4j, Milvus, Unity, CesiumJS, React, FastAPI.
- Run tests: `pytest -q` (backend), `npm test` (frontend).
- Style: type hints everywhere; no print() — use the logger.
- DB: never write to prod; use the `trainer` read-only role for queries.
- Conventions: feature branches `feat/<name>`, PRs require a passing CI.
```

Now every session already knows your commands, style, and guardrails — you stop repeating yourself. Generate a first draft with the **`/init`** command.

---

## 2. Custom slash commands — save repeatable prompts

A slash command is a reusable prompt stored as a Markdown file in **`.claude/commands/`**. Example — `.claude/commands/review.md`:

```markdown
Review the staged changes for: security issues, missing tests, and PostGIS
query performance. List problems as a checklist, most important first.
```

Now typing **`/review`** in Claude Code runs that prompt. Commands can take arguments with `$ARGUMENTS`. Great for team-standard tasks (review, write-tests, draft-migration).

---

## 3. Subagents — delegate focused work

Claude Code can spawn **subagents** for parallel or specialized work (e.g. "explore the codebase and find every place we call GeoServer", or a dedicated "test-writer"). You define reusable agents in `.claude/agents/`. Use them to keep the main conversation focused and to fan out searches across a big repo.

---

## 4. Plan mode — think before touching code

**Plan mode** makes Claude research and propose a plan **without editing** until you approve. Ideal for risky changes (a PostGIS migration, refactoring the simulation loop). You review the plan, then let it execute. (Enter it from the Claude Code UI / shortcut.)

---

## 5. Hooks — run your commands automatically

**Hooks** are shell commands Claude Code runs at lifecycle points — e.g. auto-run `prettier`/`ruff` after every file edit, or block a tool call that touches a protected path. Configured in settings (`.claude/settings.json`). This enforces standards without relying on memory.

---

## 6. Headless / CI use

Claude Code can run **non-interactively** for automation:

```bash
claude -p "summarize today's changes and update CHANGELOG.md"
```

`-p` (print) runs one prompt and exits — useful in **CI/CD** pipelines (e.g. auto-label PRs, generate release notes, triage failures).

---

## Why this matters for your team

On a large geospatial/simulation codebase, these features turn Claude Code from a chat box into a **project-aware teammate**: it knows your stack (`CLAUDE.md`), runs your standard tasks (`/commands`), works safely (plan mode, hooks), and fits into automation (headless). The next lessons connect it to your *tools* via MCP.

---

## ⭐ Must-learn from this topic

- **`CLAUDE.md`** — persistent project context; generate with `/init`.
- **Slash commands** — reusable prompts in `.claude/commands/`.
- **Subagents & plan mode** — delegate, and review before editing.
- **Hooks & headless** — enforce standards; run in CI with `claude -p`.

### 📚 Official docs
- [Claude Code overview](https://docs.claude.com/en/docs/claude-code/overview) — features & setup.
- [CLAUDE.md / memory](https://docs.claude.com/en/docs/claude-code/memory) — project context.
- [Slash commands](https://docs.claude.com/en/docs/claude-code/slash-commands), [Subagents](https://docs.claude.com/en/docs/claude-code/sub-agents), [Hooks](https://docs.claude.com/en/docs/claude-code/hooks).

➡️ Next: **[02-mcp-explained.md](02-mcp-explained.md)**
