# Claude Code — Step 3: MCP servers for OUR stack

This is the heart of the day: **for each part of your stack, which MCP server helps, and how.** Status is marked honestly — **Official** (vendor-maintained), **Community** (third-party, review before use), or **None yet** (use a general tool / your own server).

> Always confirm the exact repo on the [MCP registry](https://modelcontextprotocol.io/) or [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) before adding — names and owners change. Give each server least-privilege access.

---

## The mapping

| Stack item | MCP server to use | Status | What it lets Claude do |
|------------|-------------------|--------|------------------------|
| **GeoServer** | *No dedicated MCP yet* → use a **Postgres/PostGIS MCP** for the data, and drive GeoServer's **REST API** via a generic HTTP/`fetch` MCP or a small custom server | None yet | inspect layers/styles, automate config through REST |
| **PostgreSQL / PostGIS** | **Postgres MCP** (official reference server; `crystaldba/postgres-mcp` "Postgres MCP Pro" is a popular community option with EXPLAIN/health tools) | Official + Community | run SQL & PostGIS queries, inspect schema, analyze slow queries |
| **Redis** | **Redis MCP** (`redis/mcp-redis`) | Official | get/set keys, inspect data structures, run commands |
| **Neo4j** | **Neo4j MCP** (`neo4j-contrib/mcp-neo4j` — `mcp-neo4j-cypher`) | Official | run Cypher, read schema, query the graph |
| **Milvus** | **Milvus MCP** (`zilliztech/mcp-server-milvus`) | Official | manage collections, vector search from chat |
| **Unity** | **MCP for Unity** (`CoplayDev/unity-mcp`) | Community (Unity-endorsed) | control the editor: scenes, GameObjects, assets, scripts, console |
| **Unreal** | **Unreal MCP** (community, e.g. `chongdashu/unreal-mcp`) | Community | drive the Unreal editor / Blueprints / actors via Python remote |
| **Chaos physics** (Unreal) | via the **Unreal MCP** + code editing | Community | tweak physics actors/Blueprints through the editor bridge |
| **Blender** (3D content) | **Blender MCP** (`ahujasid/blender-mcp`) | Community | create/edit 3D objects, materials, run Blender Python |
| **CesiumJS** | *No dedicated MCP* → **Playwright/Chrome MCP** to test the viewer + **filesystem**/native editing; Cesium ion via REST | None yet | edit globe code, then drive a browser to verify the 3D scene |
| **React** | *No special MCP needed* (native code editing). **Playwright MCP** to test the UI; **Figma MCP** for design-to-code | Official (Playwright, Figma) | run/inspect the UI in a real browser; turn designs into components |
| **AI Engine** (your service) | **Write your own MCP server** wrapping its API | Build it | expose your engine's actions as Claude tools, in-network |
| **Docker** | **Docker MCP** (Docker's MCP Toolkit / community `QuantGeekDev/docker-mcp`) | Official + Community | build/run/inspect containers, read logs |
| **Kubernetes** | **Kubernetes MCP** (`Flux159/mcp-server-kubernetes`; also a Red Hat/`containers` one) | Community | list/describe pods, apply manifests, read logs, scale |
| **CI/CD** | **GitHub MCP** (`github/github-mcp-server`) for Actions/PRs; GitLab MCP if you use GitLab | Official | open PRs, read workflow runs, manage issues |

---

## How a few of these help, concretely

- **PostGIS MCP:** *"find parcels within 500m of this point and return area"* — Claude writes and runs the spatial SQL, shows results, no copy-paste into psql.
- **Neo4j MCP:** *"shortest route between substation A and B in the network graph"* — Cypher written and executed for you.
- **Milvus MCP:** *"search the 10 most similar terrain tiles to this embedding"* — vector search from chat.
- **Unity/Unreal MCP:** *"spawn 50 drone agents on the terrain and set their speed"* — the editor is driven directly; you watch it happen.
- **Blender MCP:** *"model a low-poly watchtower and export glTF"* — for 3D assets feeding Cesium/Unity.
- **Kubernetes MCP:** *"why is the simulation pod crash-looping?"* — Claude reads the pod events and logs and explains.
- **GitHub MCP:** *"open a PR for this branch with a summary and link the issue"* — CI/CD chores automated.

---

## A sensible rollout for your team

1. **Start with data MCPs** you'll use daily: PostGIS, Redis, Neo4j, Milvus (all official, low risk, read-only users).
2. **Add platform MCPs:** Docker, Kubernetes, GitHub — huge for ops/CI.
3. **Add 3D/engine MCPs** for the people doing world-building: Blender, Unity/Unreal.
4. **Build one custom MCP** for your **AI Engine** so Claude can call it like any other tool.

Each is added with `claude mcp add ...` (lesson 2) and shared via `.mcp.json`.

---

## ⭐ Must-learn from this topic

- **There's an MCP for most of your stack** — official ones for Postgres, Redis, Neo4j, Milvus, GitHub.
- **3D/engines** — Blender, Unity (CoplayDev), Unreal (community) MCPs drive the editors.
- **Gaps (GeoServer, Cesium)** — use Postgres/REST + browser MCPs, or build your own.
- **Your AI Engine** — wrap it as a custom MCP to make it a first-class tool.

### 📚 Official docs
- [Redis MCP](https://github.com/redis/mcp-redis), [Neo4j MCP](https://github.com/neo4j-contrib/mcp-neo4j), [Milvus MCP](https://github.com/zilliztech/mcp-server-milvus).
- [MCP for Unity](https://github.com/CoplayDev/unity-mcp), [Blender MCP](https://github.com/ahujasid/blender-mcp), [GitHub MCP](https://github.com/github/github-mcp-server).
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) — find & vet more.

➡️ Next: the lab — **[04-lab-blender-unity-mcp.md](04-lab-blender-unity-mcp.md)**
