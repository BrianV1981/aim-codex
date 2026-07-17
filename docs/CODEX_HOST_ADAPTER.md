# Codex host adapter boundary

## Observed local session layout

On this host, Codex stores session data beneath:

```text
~/.codex/sessions/YYYY/MM/
```

This is an observed filesystem location, not yet a stable A.I.M. parser contract. The format, conversation identity mapping, and retention behavior must be inspected with fixture-based tests before any production pulse or reincarnation reader is implemented.

## Foundation decision

The shared `aim-agy_os/.aim_core/` engine remains aligned to the soul pin in `SOURCE.md`. Codex-specific transcript discovery and tmux spawning will be an overlay, ideally behind a small `vessel_paths`/adapter interface. They are intentionally not implemented during vessel onboarding.

## Next adapter ticket

1. Capture a sanitized Codex session fixture from `~/.codex/sessions/`.
2. Define a Codex session resolver with no AGY or Grok fallback paths.
3. Add unit tests for discovery and signal extraction.
4. Implement gameplan-only pulse/reincarnation first; add tmux `codex` teleport only after the resolver passes.
