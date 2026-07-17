# aim-codex fleet parity status

**Date:** 2026-07-17  
**Soul pin:** see `SOURCE.md`  
**Branch:** greenfield foundation → promoted to default `main`

## Tickets

| Issue | Title | Status |
|-------|--------|--------|
| #2 | Codex vessel_paths + pulse discovery | Implemented |
| #3 | Codex rollout signal extractor | Implemented |
| #4 | Codex teleport spawn | Implemented |
| #5 | Promote foundation to main | GitOps |
| #6 | Fleet lockstep docs | Implemented |

## Gates

| Gate | Status |
|------|--------|
| `./aim doctor` | Required PASS |
| Unit tests (codex + inherited) | Required PASS |
| Pulse can find Codex rollout by cwd | Required |
| extract_signal on rollout | Required |
| reincarnate spawn uses codex | Required (`AIM_REINCARNATE_NO_TELEPORT=1` dry-run) |
| SOURCE.md soul pin | Required |
| aim-communicate | Required |
| Full multi-day Operator E2E wiki markers | Best-effort (Codex format differs) |

## Intentional non-parity

- Not byte-identical to Grok/AGY overlays
- Codex does not use AGY brain or Grok sessions as primary
- Blackbox vault headless keys still fleet-wide hold (#12 family)
