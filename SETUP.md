# Toolkit setup — Motion · UI UX Pro Max · 21st.dev

This project is pre-wired for the "vibe-coding" toolkit. Below is **what is
automatic** and **what only you can do once** (with the honest reasons why).

> The assistant (Claude) cannot install Claude Code plugins into your client —
> verified against the official docs: `/plugin install` is an interactive,
> user-typed command, there is no tool/API for the assistant to run it, and a
> plugin cannot be auto-installed via committed config. Marketplaces and MCP
> servers *can* be committed, which is what the files in this repo do.

---

## 1. Motion (animations) — ✅ already done, nothing to install

Motion is a **library**, not a plugin. It is loaded per-site from the CDN via a
dynamic `import()` in `js/main.js` (spring scroll reveals, stat counters, hero
parallax) with a no-dependency fallback. For a React/Next project instead, run
`npm install motion` and `import { motion } from "motion/react"`.

## 2. 21st.dev "Magic" MCP — ✅ configured here, just add your key

`.mcp.json` in this repo registers the Magic MCP server. Claude Code (web or
local) reads it automatically when you work in this repo. To activate it:

1. Get an API key: https://21st.dev/magic/console
2. Set it as an environment variable named `MAGIC_API_KEY` (the `.mcp.json`
   reads `${MAGIC_API_KEY}` so the key is **never committed**).
3. Reopen the project in Claude Code — the `magic` MCP tools appear.

> Alternative one-shot installer: `npx @21st-dev/cli@latest install claude --api-key <YOUR_KEY>`

## 3. UI UX Pro Max (Claude Code plugin) — one-time, in YOUR Claude Code

`.claude/settings.json` in this repo already registers the marketplace, so you
only run the install command once in your Claude Code client (desktop or CLI):

```
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

If the marketplace isn't picked up from the committed settings, add it manually
first:

```
/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill
/plugin install ui-ux-pro-max@ui-ux-pro-max-skill
```

CLI alternative: `npm install -g ui-ux-pro-max-cli` then `uipro init --ai claude`.

---

### Why some steps are "yours, not mine"

- Plugin **install** and the **API key** are tied to *your* Claude Code account
  and *your* machine — they live there, not in the assistant. This web session
  is a temporary, sandboxed container and is separate from your desktop client.
- Everything that *can* be baked into the repo (Motion wiring, the MCP server
  config, the marketplace registration) already is — so the toolkit travels
  with the project.
