# Claude Code — Step 5: Project-level MCP setup for our stack

Instead of every engineer adding servers by hand, you commit **one `.mcp.json`** at the repo root. Anyone who opens the project in Claude Code gets the same tools. This lesson is a **ready-to-use config for our stack**, with official and community servers, wired through environment variables so **no secrets are committed**.

> Files in this lesson: [`config/.mcp.json.example`](config/.mcp.json.example) and [`config/.env.mcp.example`](config/.env.mcp.example).

---

## How project-scope MCP works

- Claude Code reads a **`.mcp.json`** at the project root and offers those servers to everyone on the team (it asks each user to approve them once, for safety).
- Values like `${POSTGRES_URI}` in `.mcp.json` are **expanded from environment variables**, so the file is safe to commit — the actual credentials live in your shell / a local `.env.mcp` that is **git-ignored**.

Set it up:

```bash
cp day6/claude-code/config/.mcp.json.example .mcp.json     # at the repo root
cp day6/claude-code/config/.env.mcp.example .env.mcp       # fill in real values
set -a; source .env.mcp; set +a                            # load secrets into the shell
claude                                                     # start Claude Code; approve the servers
/mcp                                                       # confirm they're connected
```

> Add `.env.mcp` and `.mcp.json` (if it holds anything sensitive) to `.gitignore`. Our root `.gitignore` already ignores `.env*` except `*.example`.

---

## The servers, one by one (status + config)

Each block below is what's in `.mcp.json.example`. **Status:** Official = vendor-maintained; Community = third-party (review before use).

### PostgreSQL / PostGIS — *Community (popular): `crystaldba/postgres-mcp`*
```json
"postgres": {
  "command": "uvx",
  "args": ["postgres-mcp", "--access-mode=restricted"],
  "env": { "DATABASE_URI": "${POSTGRES_URI}" }
}
```
`--access-mode=restricted` keeps it read-leaning (safe for exploring spatial data). PostGIS works because it's just PostgreSQL. *(There's also an official reference server: `npx -y @modelcontextprotocol/server-postgres <uri>` — simpler, read-only, now archived.)*

### Redis — *Official: `redis/mcp-redis`*
```json
"redis": {
  "command": "uvx",
  "args": ["--from", "git+https://github.com/redis/mcp-redis.git", "redis-mcp-server", "--url", "${REDIS_URL}"]
}
```

### Neo4j — *Official: `neo4j-contrib/mcp-neo4j` (Cypher server)*
```json
"neo4j": {
  "command": "uvx",
  "args": ["mcp-neo4j-cypher"],
  "env": { "NEO4J_URI": "${NEO4J_URI}", "NEO4J_USERNAME": "${NEO4J_USERNAME}", "NEO4J_PASSWORD": "${NEO4J_PASSWORD}" }
}
```

### Milvus — *Official: `zilliztech/mcp-server-milvus`*
```json
"milvus": {
  "command": "uvx",
  "args": ["mcp-server-milvus", "--milvus-uri", "${MILVUS_URI}"]
}
```

### Kubernetes — *Community: `Flux159/mcp-server-kubernetes`*
```json
"kubernetes": {
  "command": "npx",
  "args": ["-y", "mcp-server-kubernetes"]
}
```
Uses your current `kubectl` context. Point it at a non-prod context first.

### Docker — *Community: `QuantGeekDev/docker-mcp`*
```json
"docker": { "command": "uvx", "args": ["docker-mcp"] }
```

### GitHub (CI/CD, PRs) — *Official: `github/github-mcp-server`*
```json
"github": {
  "command": "docker",
  "args": ["run", "-i", "--rm", "-e", "GITHUB_PERSONAL_ACCESS_TOKEN", "ghcr.io/github/github-mcp-server"],
  "env": { "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_PAT}" }
}
```
*(GitHub also hosts a remote server at `https://api.githubcopilot.com/mcp/` you can add with `--transport http` + OAuth instead of a token.)*

### Filesystem — *Official reference*
```json
"filesystem": { "command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "./"] }
```

### Playwright (test the React app / CesiumJS viewer) — *Official (Microsoft)*
```json
"playwright": { "command": "npx", "args": ["-y", "@playwright/mcp@latest"] }
```

### Blender (3D content) — *Community: `ahujasid/blender-mcp`*
```json
"blender": { "command": "uvx", "args": ["blender-mcp"] }
```

---

## Add-ons not in the default file (paste in when needed)

**Unity** — *Community (Unity-endorsed): `CoplayDev/unity-mcp`.* It installs an in-editor package and runs a Python server; use the exact `command`/`args` from the repo's README (it ships an installer), e.g.:
```json
"unity": { "command": "uvx", "args": ["unity-mcp-server"] }
```

**Unreal / Chaos** — *Community (e.g. `chongdashu/unreal-mcp`).* Uses a Python remote-control bridge into the Unreal editor; follow that repo's README for the exact command.

> For these two, **verify the launch command in the current repo README** before adding — 3D-engine MCPs change quickly. GeoServer and CesiumJS have **no dedicated MCP**: drive GeoServer via the Postgres server + its REST API, and test the Cesium viewer with the Playwright server.

---

## Security checklist (important for a closed environment)

- **Least privilege:** give the Postgres server a **read-only** DB role; scope the GitHub PAT to only what's needed; point Kubernetes at a **non-prod** context.
- **No secrets in git:** keep them in `.env.mcp` (git-ignored); `.mcp.json` only references `${VARS}`.
- **Review community servers** before enabling; pin versions where you can.
- **Approve per user:** Claude Code asks each person to approve project servers — that's expected.

---

## ⭐ Must-learn from this topic

- **`.mcp.json` (project scope)** — one committed file shares tools with the whole team.
- **`${VAR}` expansion** — reference secrets from env; never commit them.
- **Official-first** — Redis, Neo4j, Milvus, GitHub, Playwright are official; Postgres/K8s/Docker/Blender/Unity are community.
- **Least privilege** — read-only DB users, scoped tokens, non-prod contexts.

### 📚 Official docs
- [MCP in Claude Code — project scope & `.mcp.json`](https://docs.claude.com/en/docs/claude-code/mcp) — config & env expansion.
- [Model Context Protocol](https://modelcontextprotocol.io/) — the standard.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) — verify each server's current command.

➡️ Back to: **[03-mcp-for-our-stack.md](03-mcp-for-our-stack.md)** · Day plan: **[../README.md](../README.md)**
