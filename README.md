# aim-codex

**A.I.M. for [OpenAI Codex CLI](https://developers.openai.com/codex/)** — the Codex vessel of [Actual Intelligent Memory](https://github.com/BrianV1981/aim-agy).

<!-- AIM_ECOSYSTEM_START -->
### 🧬 The A.I.M. Ecosystem

Modular A.I.M. (Actual Intelligent Memory) repositories. **Flagship engine: [aim-agy](https://github.com/BrianV1981/aim-agy).**

**Active vessels (CLI hosts):**
- **[aim-agy](https://github.com/BrianV1981/aim-agy)** — Core engine / *soul* (Antigravity CLI). *Flagship.* Shared nested `aim-agy_os/` ships here first.
- **[aim-grok](https://github.com/BrianV1981/aim-grok)** — Grok CLI vessel (hybrid memory, GitOps, wiki, fleet orchestration tooling).
- **[aim-opencode](https://github.com/BrianV1981/aim-opencode)** — OpenCode CLI vessel.
- **[aim-codex](https://github.com/BrianV1981/aim-codex)** — OpenAI Codex CLI vessel (greenfield nested soul + Codex overlays; primary `main`).

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
- **aim-claude / Anthropic-line vessels** — **Done.** Operator does not develop against Anthropic. Use **aim-agy / aim-grok / aim-opencode / aim-codex**.

Full map: see **aim-skills** `docs/AIM_ECOSYSTEM_MAP.md` or Operator artifact `AIM_ECOSYSTEM_MAP.md`.
<!-- AIM_ECOSYSTEM_END -->

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Status](https://img.shields.io/badge/status-codex%20vessel-green.svg)](#status)

aim-codex wraps the shared A.I.M. engine around **Codex CLI** so long-running coding agents get:

- **Hybrid RAG memory** (LanceDB + FTS via nested `aim-agy_os/`)
- **Persistent memory wiki** (Stage 0 multi-page + schema v2)
- **GitOps discipline** (`./aim bug` → `./aim fix` → `./aim push`)
- **Session pulse / handoff** from Codex rollouts under `~/.codex/sessions/`
- **Reincarnation** spawn via tmux (`AIM_VESSEL_CLI=codex`)
- **Inter-agent comms** skill: `.codex/skills/aim-communicate/`

Upstream engine source of truth: **[aim-agy](https://github.com/BrianV1981/aim-agy)**.  
Soul pin for this checkout: **[`SOURCE.md`](SOURCE.md)**.

## Status

This is the **primary Codex vessel** (greenfield reboot). The legacy remote `master` branch is **not** an architectural source — do not merge it into `main`.

| Capability | State |
|------------|--------|
| Nested `aim-agy_os/` from soul | Done |
| `./aim doctor` | Done |
| Codex `vessel_paths` + pulse | Done |
| Codex rollout `extract_signal` | Done |
| Codex teleport spawn | Done |
| Full multi-day wiki Stage 1 polish | Evolving |
| Blackbox vault (fleet) | On hold |

See [`docs/PARITY_STATUS.md`](docs/PARITY_STATUS.md) and [`docs/CODEX_HOST_ADAPTER.md`](docs/CODEX_HOST_ADAPTER.md).

## Quick start

```bash
git clone https://github.com/BrianV1981/aim-codex.git
cd aim-codex
# ensure nested engine venv exists (setup / sync from soul as needed)
./aim doctor
./aim map
```

Codex host sessions (observed):

```text
~/.codex/sessions/YYYY/MM/DD/rollout-<iso>-<session_id>.jsonl
```

Pulse:

```bash
./aim pulse
# exclusive:
aim-agy_os/venv/bin/python3 aim-agy_os/.aim_core/handoff_pulse_generator.py \
  --session-id <uuid-from-rollout-filename>
```

Fleet communication: always tag messages with your tmux session and the orchestrator `REPLY_TO` (see aim-communicate skill).

## Relation to the fleet

| Repo | Role |
|------|------|
| [**aim-agy**](https://github.com/BrianV1981/aim-agy) | Soul / shared engine |
| [**aim-grok**](https://github.com/BrianV1981/aim-grok) | Grok vessel + fleet orchestration docs/tools |
| [**aim-opencode**](https://github.com/BrianV1981/aim-opencode) | OpenCode vessel |
| **aim-codex** (this repo) | Codex vessel + overlays |

Host-agnostic engine changes land on **aim-agy first**, then pin-sync. Codex-only overlays: `vessel_paths.py`, extract/handoff/teleport/session naming.

## License

MIT — Copyright (c) 2026 Brian Vasquez
