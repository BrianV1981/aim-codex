# aim-codex Status Report

Date: 2026-03-24
Branch: `master`

## Summary
- cleaned the active repo surface and removed stale Gemini-era artifacts
- standardized the operator-facing command name around `aim-codex`
- made `AGENTS.md` Codex-first and added an explicit retrieval-first planning rule
- rewrote the lean doc set so it matches the current runtime shape
- added explicit TDD and GitHub workflow rules to the handbook

## Current Source Of Truth
- `AGENTS.md`
- `core/USER.md`
- `core/MEMORY.md`
- `docs/A_I_M_HANDBOOK.md`
- `hooks/HOOKS_INDEX.md`

## Runtime Shape
- host runtime: `~/.codex`
- CLI alias: `aim-codex`
- root instruction file: `AGENTS.md`
- retrieval store: `archive/engram.db`
- continuity artifacts: `continuity/CURRENT_PULSE.md`, `continuity/FALLBACK_TAIL.md`

## Repo Cleanup
- removed `GEMINI.md`
- removed dead docs and hook stubs
- removed migration-only references from the active doc set
- removed generated cache artifacts from the repo tree

## Protocol Changes
- planning now explicitly starts with `aim-codex search` when project context matters
- handbook now defines a lightweight TDD protocol
- handbook now defines a lightweight GitHub protocol

## Remaining Work
- audit the command set for stale or partial commands
- validate transcript ingress and rebuild paths end to end
- keep runtime docs synchronized as command behavior changes
