# Day 6 (Advanced) — Claude Code, MCP & Spec-Driven Development

**Goal:** Work *faster and more reliably* with AI by mastering **Claude Code** at an advanced level, wiring it to your tools through **MCP servers** (including 3D tools like **Blender** and **Unity**), and building features the disciplined way with **Spec-Driven Development (GitHub Spec Kit)**.

> **How we teach here (same as Days 1–5):** easy English, one idea at a time, a concrete example, the exact command to run, and what to expect. A **⭐ Must-learn + 📚 Official docs** box ends every lesson.

> **This is an advanced/bonus day.** It assumes you've used Claude Code a little already. It is tailored to **your stack** (below) and shows *which MCP server helps with each part*.

---

## Your technology stack (and where AI fits)

This day is mapped to the stack you actually use:

| Layer | Tech | How AI/Claude Code helps today |
|-------|------|--------------------------------|
| Geospatial server | **GeoServer** | drive its REST API / config via Claude Code |
| Spatial database | **PostgreSQL / PostGIS** | a Postgres MCP queries & inspects spatial data |
| Data stores | **Redis, Neo4j, Milvus** | official MCP servers for each (query from chat) |
| Game/sim engine | **Unity** or **Unreal** | Unity/Unreal MCP to control the editor & scenes |
| 3D globe | **CesiumJS** | code with Claude Code; browser MCP to test the viewer |
| Front-end | **React** | native code editing; Playwright/Figma MCP |
| Physics | **Chaos** (Unreal) | through the Unreal MCP / code |
| AI Engine | your service | wrap it as your own MCP server |
| Platform | **Docker, Kubernetes, CI/CD** | Docker / Kubernetes / GitHub MCP servers |

The full mapping — **which MCP server to use for each** — is lesson **[claude-code/03](claude-code/03-mcp-for-our-stack.md)**.

---

## What you will learn

| Topic | What it gives you |
|-------|-------------------|
| **Advanced Claude Code** | `CLAUDE.md`, custom slash commands, subagents, hooks, plan mode, headless/CI use |
| **MCP servers** | connect Claude to live tools & data (databases, Blender, Unity, Docker, k8s…) |
| **MCP for our stack** | the exact server to use for each layer above |
| **Spec-Driven Development** | GitHub Spec Kit: `specify → plan → tasks → implement` for reliable, reviewable AI builds |

---

## Lessons in order

### 1. Claude Code & MCP
1. [Advanced Claude Code](claude-code/01-advanced-claude-code.md)
2. [MCP explained — and how to add a server](claude-code/02-mcp-explained.md)
3. [MCP servers for OUR stack](claude-code/03-mcp-for-our-stack.md) ← the mapping you asked for
4. [LAB: Blender & Unity MCP](claude-code/04-lab-blender-unity-mcp.md)
5. [Project-level MCP setup (`.mcp.json` for our stack)](claude-code/05-project-mcp-setup.md) ← ready-to-use config

### 2. Spec-Driven Development (Spec Kit)
1. [What is Spec-Driven Development?](speckit/01-what-is-speckit.md)
2. [The Spec Kit workflow](speckit/02-workflow.md)
3. [LAB: build a feature with Spec Kit](speckit/03-lab-speckit.md)

---

## A note on safety in a closed environment

MCP servers run **locally** and connect Claude to your own tools — nothing leaves your network unless you point a server at the internet. For a closed/secure setup: only add servers you've reviewed, prefer official ones, give each the **least access** it needs (read-only DB users where possible), and keep credentials in environment variables, not in chat.

---

## End-of-day result (deliverable)

A short `notes.md`: *Which 3 MCP servers would most speed up your team this month, and why? Write one `/specify` spec for a real feature and paste the generated plan.*
