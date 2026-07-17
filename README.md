# A.I.M. for Codex

This is the greenfield Codex vessel for A.I.M. It vendors the shared nested A.I.M. engine in `aim-agy_os/` and carries only Codex-specific host policy and integration overlays.

The current shared-engine source is recorded in [SOURCE.md](SOURCE.md). The legacy remote `master` branch is not an architectural source for this reboot.

## Quick checks

```bash
./aim doctor
./aim map
```

Read [AGENTS.md](AGENTS.md) before working in this repository. Codex session adapter design is documented in [docs/CODEX_HOST_ADAPTER.md](docs/CODEX_HOST_ADAPTER.md).
