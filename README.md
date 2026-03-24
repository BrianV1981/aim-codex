# aim-codex

`aim-codex` is the Codex-native A.I.M. repository and CLI workspace.

The repo is organized around four things:
- `AGENTS.md` as the root instruction file
- `~/.codex` as the host runtime surface
- `archive/engram.db` as the retrieval store
- continuity artifacts in `continuity/`

## Source Of Truth
- [`AGENTS.md`](./AGENTS.md)
- [`core/USER.md`](./core/USER.md)
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
