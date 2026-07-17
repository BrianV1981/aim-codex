# Upstream source pin

| Field | Value |
|---|---|
| Upstream | https://github.com/BrianV1981/aim-agy |
| Commit | `d461d3bdbe3a656bb00872e8ebaeca12edc222e9` (`d461d3b`) |
| Previous | `62242c2f1375d81836e8e6ab68c4c4795d8b5310` (Codex foundation) |
| Note | Lockstep re-pin 2026-07-17. Shared engine aligned; Codex overlays kept (vessel_paths, handoff, teleport, session_naming). `extract_signal` codex_rollout promoted **to soul** so all vessels share one extractor. |
| Sync date | 2026-07-17 |
| Phase | Codex vessel lockstep restore |

## Intentional overlays (do not clobber from soul)

| Path | Why |
|------|-----|
| `vessel_paths.py` | Codex rollout discovery under `~/.codex/sessions/` |
| `handoff_pulse_generator.py` | vessel_paths-first transcript resolution |
| `reincarnation/teleport_engine.py` | `AIM_VESSEL_CLI=codex` spawn |
| `session_naming.py` | default vessel id `codex` |

## Host hooks (this machine)

`~/.codex/hooks.json` → turn-done alert via `~/.aim/bin/aim_turn_chime.sh`  
Sample checked in: `.codex/hooks.sample.json`
