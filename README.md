# aim-codex

`aim-codex` is the Codex-native A.I.M. repository and CLI workspace.

The repo is organized around four things:
- `AGENTS.md` as the root instruction file
- `~/.codex` as the host runtime surface
- `archive/engram.db` as the retrieval store
- continuity artifacts in `continuity/`

## Source Of Truth
- [`AGENTS.md`](./AGENTS.md)
- [`core/OPERATOR.md`](./core/OPERATOR.md)
- [`core/MEMORY.md`](./core/MEMORY.md)
- [`docs/A_I_M_HANDBOOK.md`](./docs/A_I_M_HANDBOOK.md)

## Core Runtime
- setup: [`setup.sh`](./setup.sh)
- CLI: [`scripts/aim_cli.py`](./scripts/aim_cli.py) exposed as `aim-codex`
- config and path repair: [`src/config_utils.py`](./src/config_utils.py)
- foundation bootstrap: [`src/bootstrap_brain.py`](./src/bootstrap_brain.py)
- retrieval: [`src/retriever.py`](./src/retriever.py)
- MCP: [`src/mcp_server.py`](./src/mcp_server.py)
- hook reference: [`hooks/HOOKS_INDEX.md`](./hooks/HOOKS_INDEX.md)

## Naming Rule
- repo name: `aim-codex`
- CLI alias: `aim-codex`
- root instruction file: `AGENTS.md`

## Basic Use
```bash
cd /home/kingb/aim-codex
./setup.sh
source ~/.bashrc
aim-codex init
```

## Read Order
1. [`AGENTS.md`](./AGENTS.md)
2. [`docs/A_I_M_HANDBOOK.md`](./docs/A_I_M_HANDBOOK.md)
3. [`docs/GETTING_STARTED.md`](./docs/GETTING_STARTED.md)
4. [`hooks/HOOKS_INDEX.md`](./hooks/HOOKS_INDEX.md)

"I believe I've made my point." — **A.I.M.**

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

Modular A.I.M. (Actual Intelligent Memory) repositories. **Flagship engine: [aim-agy](https://github.com/BrianV1981/aim-agy).**

**Active vessels (CLI hosts):**
- **[aim-agy](https://github.com/BrianV1981/aim-agy)** — Core engine (Antigravity / post–Gemini-CLI line). *Flagship.*
- **[aim-grok](https://github.com/BrianV1981/aim-grok)** — Grok CLI vessel (hybrid memory, GitOps, wiki).
- **[aim-opencode](https://github.com/BrianV1981/aim-opencode)** — OpenCode CLI vessel.
- **[aim-codex](https://github.com/BrianV1981/aim-codex)** — Codex-native vessel (**on the horizon** — not deprecated).

**Tools & workspaces:**
- **[aim-connect](https://github.com/BrianV1981/aim-connect)** — Self-hosted remote workspace web UI.
- **[aim-tmux-dashboard](https://github.com/BrianV1981/aim-tmux-dashboard)** — Terminal multi-session monitor.
- **[aim-browser](https://github.com/BrianV1981/aim-browser)** — Headed Chromium CDP engine + browser **skill suite**.
- **[aim-google](https://github.com/BrianV1981/aim-google)** — Google Workspace CLI (Gmail, Drive, Calendar, …).
- **[aim-flight-recorder](https://github.com/BrianV1981/aim-flight-recorder)** — Forensic Markdown session extractor.
- **[aim-boardroom](https://github.com/BrianV1981/aim-boardroom)** — Multi-agent orchestration room (OS multiplexing + artifacts).
- **[aim-skills](https://github.com/BrianV1981/aim-skills)** — **Skills index / multi-CLI install registry** (agy, grok, opencode, codex).

**DNA, comms & lore:**
- **[aim-coagents](https://github.com/BrianV1981/aim-coagents)** — DNA bank for sovereign co-agent blueprints.
- **[aim-knowledge](https://github.com/BrianV1981/aim-knowledge)** — Public Obsidian vault / deep-lore archive.
- **[aim-chalkboard](https://github.com/BrianV1981/aim-chalkboard)** — Optional cross-host async git mailbox (PoC; default same-host comms = **aim-communicate** skill).

**Deprecated / not maintained:**
- **[aim](https://github.com/BrianV1981/aim)** — Original **Gemini CLI** framework. Deprecated after loss of practical subscription access; **Great Migration → aim-agy**.
- **[aim-swarm](https://github.com/BrianV1981/aim-swarm)** — Legacy Python swarm factory → use **aim-coagents** + aim-agy spawn.
- **aim-claude / Anthropic-line vessels** — **Done.** Operator does not develop against Anthropic. Use aim-agy / aim-grok / aim-opencode (or aim-codex when ready).

Full map: see **aim-skills** `docs/AIM_ECOSYSTEM_MAP.md` or Operator artifact `AIM_ECOSYSTEM_MAP.md`.
<!-- AIM_ECOSYSTEM_END -->

