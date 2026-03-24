# Agent Workflow

This file describes how an agent should orient itself inside `aim-codex`.

## Startup Order
1. Read `AGENTS.md`
2. Read `core/USER.md`
3. Read `core/MEMORY.md`
4. Read `docs/A_I_M_HANDBOOK.md`
5. Read `hooks/HOOKS_INDEX.md`

## Working Context
- Durable memory: `core/MEMORY.md`
- Operator profile: `core/USER.md`
- Current edge: `continuity/CURRENT_PULSE.md`
- Recent tactical tail: `continuity/FALLBACK_TAIL.md`

## Repo Intent
This repository is the Codex-hosted A.I.M. workspace. Treat it as the live Codex runtime for this project, not as a historical archive.

## Rules
- Prefer current repo files over historical assumptions
- Use the hook index as the lifecycle source of truth
- Use the tools manifest when you need the runtime surface quickly
- Use retrieval before guessing when the Engram DB contains relevant context

## Handoff
- `aim-codex handoff` updates short-term continuity
- `CURRENT_PULSE.md` and `FALLBACK_TAIL.md` are the active continuity artifacts

"I believe I've made my point." — **A.I.M.**
