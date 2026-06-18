# Spec Kit — Step 1: What is Spec-Driven Development?

## The problem with "just prompt it"

Throwing a one-line prompt at an AI ("build me a parcel-search API") often gives messy, hard-to-review code that drifts from what you actually wanted. On a serious platform like yours, you need the AI to follow a **clear specification** that the team can review *before* code is written.

## Spec-Driven Development (SDD)

**Spec-Driven Development** flips the usual order: instead of code first and docs later, you write an **executable specification** first, and the AI builds *from the spec*. The spec is the source of truth; the code is generated to satisfy it.

**GitHub Spec Kit** is the open-source toolkit that makes this a repeatable workflow. It works with many AI coding agents (including **Claude Code**) and gives you a sequence of slash commands.

## The workflow in one line

```
 /constitution → /specify → /plan → /tasks → /implement
   (principles)    (WHAT)     (HOW)   (steps)   (build)
```

- **`/constitution`** — set the project's non-negotiable principles (style, testing, constraints) once.
- **`/specify`** — describe **what** and **why** (the feature, the users, the outcomes) — *no tech details*.
- **`/plan`** — give the **technical how** (your stack: PostGIS, FastAPI, React…); the agent writes a detailed plan.
- **`/tasks`** — break the plan into a checklist of concrete, reviewable tasks.
- **`/implement`** — the agent executes the tasks to produce the code.

(Newer Spec Kit also adds `/clarify` and `/analyze` to tighten the spec before building.)

## Why your team will benefit

- **Reviewable intent.** The spec and plan are read and approved *before* code — fewer wrong turns on a complex geospatial/simulation system.
- **Consistency.** The `constitution` enforces your standards across every feature and every engineer.
- **Better AI output.** Clear intent → the agent builds the right thing the first time, and the artifacts (spec, plan, tasks) live in the repo for the next person.
- **Big-system friendly.** Splitting *what* from *how* keeps changes to GeoServer/PostGIS/Unity/React coordinated and traceable.

It's the discipline that makes AI coding trustworthy on a real product, not just a demo.

---

## ⭐ Must-learn from this topic

- **SDD** — write an executable **spec first**; generate code from it.
- **Spec Kit** — GitHub's toolkit; works with Claude Code.
- **The commands** — `/constitution → /specify → /plan → /tasks → /implement`.
- **What vs how** — `/specify` is the *what/why*; `/plan` is the *tech how*.

### 📚 Official docs
- [GitHub Spec Kit (repo)](https://github.com/github/spec-kit) — the toolkit.
- [Spec Kit docs](https://github.github.com/spec-kit/) — quickstart & commands.
- [GitHub blog: Spec-driven development](https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/) — the why.

➡️ Next: **[02-workflow.md](02-workflow.md)**
