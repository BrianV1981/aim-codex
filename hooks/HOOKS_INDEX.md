# Hooks Index

This file tracks the current hook surface in `aim-codex`.

## Registered Codex Hooks
- `UserPromptSubmit` -> `context_injector.py`
- `agent-turn-complete` -> `failsafe_context_snapshot.py`
- `Stop` -> `src/handoff_pulse_generator.py`

## Support Modules In Repo
- `tier1_hourly_summarizer.py`: memory pipeline entry
- `safety_sentinel.py`: shell safety logic
- `secret_shield.py`: secret and write protection logic
- `workspace_guardrail.py`: workspace boundary checks

## Rule
Only the registered Codex hooks should be described as active lifecycle hooks. Everything else is supporting runtime code.

## Related Docs
- `docs/A_I_M_HANDBOOK.md`
- `docs/CODEX_ROADMAP.md`
