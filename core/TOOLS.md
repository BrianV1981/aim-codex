# A.I.M. Tools Manifest

This manifest describes the active internal surfaces that matter in `aim-codex`.

## 1. Root Soul
- File: `AGENTS.md`
- Role: root instruction file for this repository

## 2. Retrieval
- Entry: `src/retriever.py`
- CLI: `aim-codex search "<query>"`
- Purpose: retrieve historical technical context from `archive/engram.db`

## 3. Indexing
- Entry: `src/indexer.py`
- CLI: `aim-codex index`
- Purpose: convert archived transcripts and indexed material into searchable fragments

## 4. Foundation Bootstrap
- Entry: `src/bootstrap_brain.py`
- Purpose: synchronize foundation knowledge into the Engram DB

## 5. Continuity
- Pulse generation: `src/handoff_pulse_generator.py`
- Snapshot and tail maintenance: `hooks/failsafe_context_snapshot.py`
- Startup injection: `hooks/context_injector.py`

## 6. MCP
- Entry: `src/mcp_server.py`
- Purpose: expose retrieval and project context externally

## 7. Docs
- Overview: `README.md`
- Architecture: `docs/A_I_M_HANDBOOK.md`
- Startup: `docs/GETTING_STARTED.md`
- Hook lifecycle: `hooks/HOOKS_INDEX.md`

## Usage Rule
When working in this repo, prefer the current runtime files and the lean doc set over any older assumptions.
