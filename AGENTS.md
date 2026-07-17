# A.I.M. Codex Vessel

## Mission and boundaries

This repository is the **Codex host vessel** for A.I.M. The nested `aim-agy_os/` is the shared A.I.M. engine; its upstream source of truth is `/home/kingb/aim-agy` and the active pin is recorded in `SOURCE.md`.

Implement shared-engine changes on `aim-agy` first. In this vessel, change only Codex host overlays: Codex configuration and skills, Codex transcript discovery, Codex process spawning, root documentation, and the `./aim` wrapper.

## Working loop

1. Search the Engram database before changing engine behavior: `./aim search "<topic>"`.
2. Write or update `PLANS.md` before implementation.
3. Add tests with implementation and run the narrowest relevant checks.

Use `./aim` as the A.I.M. entry point. Do not run `./setup.sh` autonomously because it may require interactive system privileges.

## GitOps

- For normal work: `./aim bug` → `./aim fix <id>` → tests → `./aim push`.
- Never work on or push `main` directly. Verify with `git branch --show-current` before release.
- Stage paths surgically; never use `git add .`.
- `aim promote` and `aim merge-batch` require explicit human HITL confirmation.
- `origin/master` is legacy pre-reboot content. Do not merge it into the vessel foundation.

The current greenfield foundation is the authorized exception: branch `chore/codex-vessel-foundation` may bootstrap the first commit without an issue/worktree, then must return to normal GitOps.

## Fleet communication

Use `.codex/skills/aim-communicate/` for every tmux message. Discover your live tmux session first. In this campaign, reply only to `aim-grok` and include:

`[FROM:aim-codex] [REPLY_TO:aim-grok]`

Codex and Grok submit with Enter only—never send Escape first. Read the fleet playbook in `aim-agy_os/aim-agy_os_docs/FLEET_ORCHESTRATION.md` before cross-vessel work.

## Codex host boundary

- Durable repository guidance: this `AGENTS.md`.
- Repository configuration and integrations: `.codex/config.toml` when needed.
- Reusable workflows: `.codex/skills/`.
- Local Codex session storage observed on this host: `~/.codex/sessions/`.

Session parsing, pulse discovery, and reincarnation are deliberately **TBD** until a Codex-native adapter is designed and tested. Do not use AGY/Grok transcript paths as a fallback.
