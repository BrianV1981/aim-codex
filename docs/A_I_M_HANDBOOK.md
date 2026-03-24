# A.I.M. Handbook

This is the current architecture reference for `aim-codex`.

## Identity
- Root instruction file: `AGENTS.md`
- Operator profile: `core/USER.md`
- Durable memory: `core/MEMORY.md`
- Short-term continuity: `continuity/CURRENT_PULSE.md` and `continuity/FALLBACK_TAIL.md`

## Runtime
- Setup entrypoint: `setup.sh`
- CLI entrypoint: `scripts/aim_cli.py`
- Config file: `core/CONFIG.json`
- Path normalization: `src/config_utils.py`
- Codex transcript ingress: `~/.codex/memories`

## Retrieval
- Search store: `archive/engram.db`
- Bootstrap/index foundation docs: `src/bootstrap_brain.py`
- Search and recall: `src/retriever.py`
- Fragment indexing: `src/indexer.py`
- External context surface: `src/mcp_server.py`

## Memory Flow
1. Raw session material is mirrored into `archive/raw/`.
2. Signal extraction and indexing turn source material into searchable fragments.
3. Summarizers and handoff generation update continuity and memory artifacts.
4. Retrieval queries the Engram DB when project context is needed.

## TDD Protocol
1. Start with the failing test when behavior is changing or a bug is being fixed.
2. Make the smallest code change that turns the test green.
3. Refactor only after the behavior is covered and passing.
4. Keep the test close to the runtime surface it protects.
5. If no test is added, there should be a concrete reason.

## GitHub Protocol
1. Work from the current repo state, not assumptions.
2. Keep changes scoped and coherent enough to explain in one commit message.
3. Verify the affected code paths before committing.
4. Push clean, reviewable history to the active branch.
5. Keep docs aligned with the code in the same change when behavior or operator workflow changes.

## Hooks
The actual wired Codex lifecycle is documented in [`hooks/HOOKS_INDEX.md`](../hooks/HOOKS_INDEX.md). Treat that file as the source of truth for hook registration.

## Read First
1. `AGENTS.md`
2. `core/USER.md`
3. `core/MEMORY.md`
4. `docs/GETTING_STARTED.md`
5. `hooks/HOOKS_INDEX.md`

"I believe I've made my point." — **A.I.M.**
