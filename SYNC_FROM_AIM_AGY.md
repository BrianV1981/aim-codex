# Syncing engine code from aim-agy → aim-codex

aim-agy is the **soul** for shared engine. aim-codex vendors `aim-agy_os/` and keeps **Codex host overlays**.

## Four-vessel drift check

```bash
python3 /home/kingb/aim-agy/scripts/vessel_core_diff.py --pair agy,codex --report-only
python3 /home/kingb/aim-agy/scripts/vessel_core_diff.py --report-only
```

## Overlay denylist (do not clobber blindly)

| Path | Owner |
|------|--------|
| `AGENTS.md`, `README.md`, `SOURCE.md`, `./aim` | aim-codex |
| `.codex/` skills + hooks sample | aim-codex |
| `vessel_paths.py` | aim-codex |
| `handoff_pulse_generator.py` | aim-codex (vessel_paths) |
| `reincarnation/teleport_engine.py` | aim-codex spawn |
| `session_naming.py` | aim-codex default `codex` |

## Safe rsync (engine only)

```bash
AGY=/home/kingb/aim-agy
CODEX=/home/kingb/aim-codex

rsync -anc \
  --exclude venv --exclude memory --exclude memory_lance \
  --exclude workspace --exclude archive --exclude continuity \
  --exclude memory-wiki --exclude planning-artifacts \
  --exclude '__pycache__' --exclude '*.pyc' --exclude temp \
  --exclude '.aim_core/vessel_paths.py' \
  --exclude '.aim_core/handoff_pulse_generator.py' \
  --exclude '.aim_core/reincarnation/teleport_engine.py' \
  --exclude '.aim_core/session_naming.py' \
  "$AGY/aim-agy_os/" "$CODEX/aim-agy_os/"

# Real sync after dry-run review:
# rsync -a  (same excludes)
```

After sync:

1. Re-check overlays with `git diff`
2. Bump `SOURCE.md` pin to aim-agy HEAD
3. `./aim doctor` + `pytest aim-agy_os/tests/test_codex_vessel_parity.py`
