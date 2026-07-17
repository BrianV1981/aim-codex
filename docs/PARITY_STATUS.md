# aim-codex fleet parity status

**Date:** 2026-07-17 (lockstep restore)  
**Soul pin:** `d461d3b` — see `SOURCE.md`  
**Branch:** `main`

## Tickets / gates

| Gate | Status |
|------|--------|
| Nested soul + Codex overlays | **PASS** |
| `vessel_paths` + rollout discovery | **PASS** |
| `extract_signal` codex_rollout | **PASS** (promoted to soul / all vessels) |
| Pulse exclusive session | **PASS** (wiki E2E earlier) |
| Blackbox seal on reincarnate | **PASS** (fleet vault) |
| `--session-id` / `--no-teleport` CLI | **PASS** |
| Teleport spawn code | **PASS** |
| Live teleport E2E on this host | **PENDING** (needs Codex session / quota) |
| Turn-done desktop notify hook | **WIRED** host `~/.codex/hooks.json` → `aim_turn_chime.sh` |
| `vessel_core_diff` includes codex | **PASS** (4-pillar) |
| SOURCE.md pin current | **PASS** (`d461d3b`) |
| aim-communicate skill | **PASS** (`.codex/skills/`) |

## Intentional non-parity (overlays)

- `vessel_paths.py`, handoff, teleport, session_naming default `codex`
- Not byte-identical to AGY/Grok host spawn paths
- Codex does not use AGY brain or Grok `updates.jsonl` as primary

## Operator prove (when quota allows)

```bash
cd /home/kingb/aim-codex
./aim doctor
aim-agy_os/venv/bin/python3 -m pytest aim-agy_os/tests/test_codex_vessel_parity.py -q

# Wiki pulse (no live Codex agent required if fixture harness used):
AIM_WIKI_SKIP_LANCE=1 aim-agy_os/venv/bin/python3 \
  aim-agy_os/scripts/operator_reincarnate_wiki_e2e_codex.py

# Live agent smoke (minimal tokens): open aim-codex tmux, one short prompt,
# confirm desktop/popup notify fires on turn end.
```
