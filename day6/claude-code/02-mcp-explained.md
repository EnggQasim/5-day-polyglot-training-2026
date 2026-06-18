# Claude Code — Step 2: MCP explained (and how to add a server)

## What is MCP?

**MCP = Model Context Protocol.** It is an open standard that lets an AI assistant (Claude) talk to **external tools and data** through small adapter programs called **MCP servers**. Think of MCP as a **USB port for AI**: instead of Claude only seeing your chat, an MCP server gives it real *tools* — "query this database", "create this object in Blender", "list these Kubernetes pods".

```
 Claude Code  ──MCP──►  MCP server  ──►  a real tool/data
   (the client)          (adapter)        (Postgres, Blender, Unity, Docker, k8s…)
```

- An MCP server exposes **tools** (actions Claude can call), **resources** (data it can read), and sometimes **prompts**.
- Servers run **locally** (a command on your machine) or remotely (an HTTP endpoint). In a closed environment you mostly run local ones.

## Why it matters for your stack

Without MCP, Claude can only read/write files you show it. **With** MCP it can directly *act on your systems*: run a PostGIS query, push a 3D asset into Unity, check a pod's logs — all from one chat, with your guardrails. That's the leap from "AI that writes code" to "AI that operates your tools".

---

## Add an MCP server to Claude Code

The command is **`claude mcp add`**. Three transport types:

**1. A local command (most common):**
```bash
# generic shape: claude mcp add <name> -- <command> [args...]
claude mcp add blender -- uvx blender-mcp
```

**2. With environment variables (e.g. credentials):**
```bash
claude mcp add redis --env REDIS_URL=redis://localhost:6379 -- uvx --from redis-mcp redis-mcp
```

**3. A remote HTTP/SSE server:**
```bash
claude mcp add my-ai-engine --transport http https://ai.internal/mcp
```

Then manage them:
```bash
claude mcp list           # what's connected
claude mcp get blender    # details
claude mcp remove blender # remove
```

> Servers can also be added per-project in a checked-in `.mcp.json`, so the whole team shares the same tools. Scope matters: `local` (you), `project` (shared via `.mcp.json`), or `user` (all your projects).

## Use it

Once added, in a Claude Code session the server's tools appear automatically. You just ask in plain English — *"using the Postgres MCP, show the 5 largest parcels by area"* — and Claude calls the tool. Type `/mcp` to see connected servers and their status.

## Finding servers safely

Reputable indexes: the official MCP servers list, "Awesome MCP Servers", and vendors' own repos (Redis, Neo4j, Milvus, GitHub all ship official servers). **Review a server before adding it** — it runs with whatever access you give it. Prefer official servers; give DB servers a **read-only** user where you can.

---

## ⭐ Must-learn from this topic

- **MCP** — open standard; servers give Claude **tools/resources** for real systems.
- **`claude mcp add`** — local command, env vars, or remote HTTP.
- **Scopes** — local / project (`.mcp.json`) / user; `/mcp` to inspect.
- **Safety** — review servers; least-privilege credentials; official first.

### 📚 Official docs
- [MCP in Claude Code](https://docs.claude.com/en/docs/claude-code/mcp) — adding & using servers.
- [Model Context Protocol](https://modelcontextprotocol.io/) — the standard & concepts.
- [Example servers](https://modelcontextprotocol.io/examples) — official reference servers.

➡️ Next: **[03-mcp-for-our-stack.md](03-mcp-for-our-stack.md)**
