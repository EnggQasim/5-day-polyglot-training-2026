# Claude Code — Step 4: LAB (Blender & Unity MCP)

Connect Claude Code to two 3D tools from your stack and drive them by chat: **Blender** (3D content) and **Unity** (the engine). These produce the assets and scenes your CesiumJS/simulation world needs.

> These run on a workstation with Blender / Unity installed. They are **community** servers — review them and run in a safe project first.

---

## Part A — Blender MCP

**Prerequisites:** Blender 3.0+, Python 3.10+, and `uv` (`brew install uv` on macOS; `winget install astral-sh.uv` on Windows).

**1. Install the Blender add-on**
- Download `addon.py` from the [Blender MCP repo](https://github.com/ahujasid/blender-mcp).
- Blender → **Edit → Preferences → Add-ons → Install…**, pick `addon.py`, enable **"Interface: Blender MCP"**.
- In the 3D view sidebar (press **N**), open the **BlenderMCP** tab and click **Start MCP server**.

**2. Add the server to Claude Code**
```bash
claude mcp add blender -- uvx blender-mcp
claude mcp list        # confirm "blender" is connected
```

**3. Drive Blender from chat**
In a Claude Code session, try:
- *"Using the Blender MCP, create a low-poly watchtower: a 4-sided tapered tower with a railing on top, and apply a stone-grey material."*
- *"Add a ground plane and a sun light, then describe the scene hierarchy."*
- *"Export the selection as glTF to ./assets/watchtower.glb."*

Watch Blender build it live. Claude is calling Blender's Python through the MCP server.

---

## Part B — Unity MCP

**Prerequisites:** Unity (with a project open), Python, and `uv`.

**1. Install the Unity package**
- Follow [MCP for Unity](https://github.com/CoplayDev/unity-mcp): add the package via Unity Package Manager (Git URL), which installs the in-editor bridge.

**2. Add the server to Claude Code**
```bash
claude mcp add unity -- uvx unity-mcp-server     # exact command per the repo's README
claude mcp list
```

**3. Drive Unity from chat**
- *"Using the Unity MCP, list the GameObjects in the active scene."*
- *"Create an empty GameObject 'Drones', and under it spawn 10 cubes in a grid on the terrain."*
- *"Add a C# script `Patrol.cs` that moves an object between two waypoints, and attach it."*
- *"Show me the latest console errors."*

The editor responds in real time — scene changes, new assets, script edits — without you leaving Claude Code.

---

## Tie-in to your world

A typical loop for your platform:
1. **Blender MCP** models/export an asset (watchtower, vehicle) → glTF.
2. **Unity/Unreal MCP** places it in the scene and wires behaviour (Chaos physics, patrol scripts).
3. The same glTF/3D-tiles can feed **CesiumJS** for the web globe.
4. Claude Code ties it together and commits via the **GitHub MCP**.

---

## What you achieved

- Connected Claude Code to **Blender** and **Unity** via MCP.
- Created 3D content and scene objects **by chat**, hands-on.
- Saw the asset → engine → web pipeline your stack uses.

### Deliverable for this track
In `notes.md`: *Which engine MCP (Unity or Unreal) fits your team, and what 3 editor tasks would you automate first? Note any access/safety limits you'd set.*

➡️ Next: **[../speckit/01-what-is-speckit.md](../speckit/01-what-is-speckit.md)**

---

## ⭐ Must-learn from this topic

- **Blender MCP** — add-on + `uvx blender-mcp`; model/export by chat.
- **Unity MCP** — in-editor package + server; control scenes/scripts/console.
- **Add via `claude mcp add`**, confirm with `claude mcp list` / `/mcp`.
- **Pipeline** — Blender → Unity/Unreal → Cesium, orchestrated from Claude Code.

### 📚 Official docs
- [Blender MCP](https://github.com/ahujasid/blender-mcp) — add-on & config.
- [MCP for Unity (CoplayDev)](https://github.com/CoplayDev/unity-mcp) and [Unity's MCP guide](https://unity.com/blog/unity-ai-mcp-how-to-get-started).
- [MCP in Claude Code](https://docs.claude.com/en/docs/claude-code/mcp) — managing servers.
