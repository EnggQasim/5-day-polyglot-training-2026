# Spec Kit — Step 2: The workflow

Let's install Spec Kit and walk the commands. Spec Kit uses the `specify` CLI (run via `uv`), then the slash commands run **inside Claude Code**.

---

## Install & initialize

Prerequisite: **`uv`** (`brew install uv` on macOS; `winget install astral-sh.uv` on Windows) and Python 3.11+.

```bash
# initialize Spec Kit in a project, choosing Claude as the agent
uvx --from git+https://github.com/github/spec-kit.git specify init geosim-feature --ai claude
cd geosim-feature
# (or `specify init --here --ai claude` to set up the current folder)
```

This creates a `.specify/` folder with templates and registers the slash commands for Claude Code. Open the project in Claude Code.

---

## Step 1 — `/constitution` (once per project)

Set the rules everything must follow:

```
/constitution Our principles: Python type hints everywhere; every feature ships
with tests; spatial queries must use PostGIS indexes; APIs are FastAPI with
Pydantic; no writes to production data in examples.
```

Spec Kit writes these to `.specify/memory/constitution.md` and applies them in later steps.

## Step 2 — `/specify` (the WHAT and WHY)

Describe the feature in plain language — **no tech choices**:

```
/specify A "nearby assets" feature: given a map point and a radius, return the
game assets within that radius, sorted by distance, with name and category.
Users are mission planners who need this in under a second.
```

The agent generates a **spec** (`spec.md`) describing requirements, user stories, and acceptance criteria. Review and edit it — this is the contract.

> Tip: run **`/clarify`** (if available) to have the agent ask about anything ambiguous before planning.

## Step 3 — `/plan` (the HOW — your stack)

Now give technical direction:

```
/plan Use PostGIS (ST_DWithin on a GiST index) via FastAPI + asyncpg for the
endpoint, Redis to cache hot queries, and expose GET /assets/nearby. React
calls it with RTK Query.
```

The agent writes a detailed **plan** (`plan.md`) — data model, endpoints, files to change — that respects the constitution.

## Step 4 — `/tasks`

```
/tasks
```

It breaks the plan into an ordered, checkable **task list** (`tasks.md`): "add migration", "write query", "add endpoint", "write tests", "wire React". Each is small and reviewable.

## Step 5 — `/implement`

```
/implement
```

The agent works through the tasks, writing code and tests. Because the spec/plan/tasks were reviewed, the output matches intent — and the artifacts stay in the repo for the next engineer.

> Newer Spec Kit adds **`/analyze`** to cross-check spec ↔ plan ↔ tasks for gaps before you implement.

---

## The artifacts you get

```
.specify/memory/constitution.md   # your principles
specs/<feature>/spec.md           # what & why  (reviewed)
specs/<feature>/plan.md           # technical how (reviewed)
specs/<feature>/tasks.md          # the checklist
+ the implemented code & tests
```

All version-controlled — so a feature's *intent* lives next to its code.

---

## ⭐ Must-learn from this topic

- **`specify init --ai claude`** — set up Spec Kit for Claude Code.
- **The order** — constitution → specify → plan → tasks → implement.
- **Separation** — `/specify` = what/why (no tech); `/plan` = the tech.
- **Artifacts in git** — spec/plan/tasks live with the code.

### 📚 Official docs
- [Spec Kit quickstart](https://github.github.com/spec-kit/quickstart.html) — install & first run.
- [Spec Kit repo](https://github.com/github/spec-kit) — commands & templates.
- [Microsoft: Diving into SDD with Spec Kit](https://developer.microsoft.com/blog/spec-driven-development-spec-kit) — a worked walkthrough.

➡️ Next: the lab — **[03-lab-speckit.md](03-lab-speckit.md)**
