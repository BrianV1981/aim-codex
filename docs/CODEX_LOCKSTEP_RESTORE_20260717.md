# Codex lockstep restore (no agent)

Date: 2026-07-17  
Soul pin: d461d3b

## Done offline
- Promoted `extract_signal` codex_rollout → soul + grok + opencode (4-way SYNC)
- Sync'd `aim_cli.py` from soul → codex
- SOURCE.md pin → d461d3b
- SYNC_FROM_AIM_AGY.md for codex
- vessel_core_diff.py 4-pillar (agy/grok/opencode/codex)
- PARITY_STATUS refreshed
- Host hooks: ~/.codex/hooks.json → aim_turn_chime.sh (was broken paths)
- doctor PASS, test_codex_vessel_parity 5 PASS

## agy↔codex
identical=49, known overlays only: handoff, teleport, session_naming + vessel_paths only-codex

## Still needs live Codex agent (quota)
- Confirm agent-turn-complete fires desktop notify
- Live teleport E2E in real tmux pane
