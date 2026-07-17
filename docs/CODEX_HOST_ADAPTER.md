# Codex host adapter

## Session layout (production)

```text
~/.codex/sessions/YYYY/MM/rollout-<iso>-<session_id>.jsonl
```

First records often:

```json
{"type":"session_meta","payload":{"session_id":"...","cwd":"/home/kingb/aim-codex",...}}
```

Dialogue:

- `response_item` / `payload.type=message` / `role=user|assistant`
- `event_msg` / `user_message` | `agent_message`

## Code map

| Concern | Module |
|---------|--------|
| Discovery | `aim-agy_os/.aim_core/vessel_paths.py` |
| Signal extract | `extract_signal.extract_signal_from_codex_rollout` |
| Pulse | `handoff_pulse_generator` → vessel_paths auto |
| Teleport | `reincarnation/teleport_engine.py` (`AIM_VESSEL_CLI=codex`) |
| Session names | `session_naming.vessel_cli_id` → `codex_*` |

## Operator commands

```bash
cd /home/kingb/aim-codex
./aim doctor
./aim pulse
# exclusive:
aim-agy_os/venv/bin/python3 aim-agy_os/.aim_core/handoff_pulse_generator.py \
  --session-id <uuid-from-rollout-filename>

AIM_REINCARNATE_NO_TELEPORT=1 AIM_VESSEL_CLI=codex ./aim reincarnate
```

## Communicate

Submit to Codex/Grok: **Enter only**.  
Orchestrator this campaign: **`aim-grok`**.
