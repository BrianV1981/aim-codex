import os
import sys
import subprocess
import signal
import time
import shutil


def get_current_tmux_session():
    current_session = None
    if os.environ.get("TMUX"):
        try:
            result = subprocess.run(
                ["tmux", "display-message", "-p", "#S"],
                capture_output=True,
                text=True,
            )
            current_session = result.stdout.strip()
        except Exception:
            pass
    return current_session


def _resolve_vessel_cli(workspace: str) -> list:
    """
    Choose host CLI for the new vessel on aim-codex.
    AIM_VESSEL_CLI=codex|grok|agy overrides.
    Default: codex when cwd looks like aim-codex; else codex if available.
    """
    override = (os.environ.get("AIM_VESSEL_CLI") or "").strip().lower()
    ws = os.path.abspath(workspace)
    base = os.path.basename(ws)

    if override in ("codex", "grok", "agy"):
        kind = override
    elif "aim-codex" in ws or base.startswith("aim-codex") or base.startswith("test_aim_codex"):
        kind = "codex"
    elif shutil.which("codex"):
        kind = "codex"
    elif shutil.which("grok"):
        kind = "grok"
    elif shutil.which("agy"):
        kind = "agy"
    else:
        kind = "codex"

    if kind == "codex":
        codex = (
            os.environ.get("CODEX_BIN")
            or shutil.which("codex")
            or os.path.expanduser("~/.npm-global/bin/codex")
        )
        # Interactive session in workspace; wake prompt as initial message when supported
        return [codex]
    if kind == "grok":
        grok = shutil.which("grok") or os.path.expanduser("~/.local/bin/grok")
        return [grok, "--always-approve", "--cwd", workspace]
    agy = shutil.which("agy") or os.path.expanduser("~/.local/bin/agy")
    return [agy, "--dangerously-skip-permissions"]


def spawn_new_agent(workspace, session_name, wake_up_prompt):
    print("[2/4] Spawning new host vessel (tmux session) with Ephemeral Context Injection...")
    cli = _resolve_vessel_cli(workspace)
    kind = "codex"
    if cli and "grok" in os.path.basename(cli[0]):
        kind = "grok"
    elif cli and "agy" in os.path.basename(cli[0]):
        kind = "agy"
    print(f"      Vessel CLI: {kind} ({cli[0]})")

    try:
        if kind == "codex":
            # Start codex TUI in workspace; inject wake prompt after spawn
            cmd = [
                "tmux",
                "new-session",
                "-d",
                "-s",
                session_name,
                "-c",
                workspace,
            ] + cli
            subprocess.run(cmd, check=True)
            time.sleep(1.0)
            # Paste wake prompt as first user turn (Enter-only submit)
            subprocess.run(
                ["tmux", "set-buffer", "-b", "aim_wake", wake_up_prompt],
                check=False,
            )
            subprocess.run(
                ["tmux", "paste-buffer", "-b", "aim_wake", "-p", "-t", session_name],
                check=False,
            )
            time.sleep(0.4)
            subprocess.run(
                ["tmux", "send-keys", "-t", session_name, "Enter"],
                check=False,
            )
        elif kind == "grok":
            cmd = [
                "tmux",
                "new-session",
                "-d",
                "-s",
                session_name,
                "-c",
                workspace,
            ] + cli + [wake_up_prompt]
            subprocess.run(cmd, check=True)
        else:
            try:
                from agy_workspace_trust import prepare_agy_spawn, dismiss_trust_prompt_tmux

                workspace = prepare_agy_spawn(workspace)
            except Exception as te:
                print(f"      [TRUST] WARN pre-register failed: {te}")
                dismiss_trust_prompt_tmux = None  # type: ignore
            cmd = [
                "tmux",
                "new-session",
                "-d",
                "-s",
                session_name,
                "-c",
                workspace,
            ] + cli + ["-i", wake_up_prompt]
            subprocess.run(cmd, check=True)
            if dismiss_trust_prompt_tmux:
                dismiss_trust_prompt_tmux(session_name)

        print(f"      [Success] New agent is awake in tmux session: {session_name}")
    except FileNotFoundError:
        print("[ERROR] 'tmux' is not installed. The Reincarnation Protocol requires tmux.")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to spawn tmux session: {e}")
        sys.exit(1)

    print(f"[3/4] Wake-up prompt handled for {kind} vessel...")


def execute_teleport(current_session, session_name):
    print("[4/4] Executing Teleport Sequence...")

    if os.environ.get("AIM_REINCARNATE_NO_TELEPORT", "").lower() in (
        "1",
        "true",
        "yes",
    ):
        print(
            f"      [NO_TELEPORT] Leaving current session intact. "
            f"New vessel: tmux attach -t {session_name}"
        )
        return

    time.sleep(2)

    if os.environ.get("TMUX") and current_session:
        print(
            f"      [Teleport] TMUX detected. Switching clients from {current_session} to {session_name}..."
        )
        try:
            clients_result = subprocess.run(
                [
                    "tmux",
                    "list-clients",
                    "-t",
                    current_session,
                    "-F",
                    "#{client_name}",
                ],
                capture_output=True,
                text=True,
            )
            clients = clients_result.stdout.strip().split("\n")

            for client in clients:
                client = client.strip()
                if client:
                    subprocess.run(
                        ["tmux", "switch-client", "-c", client, "-t", session_name],
                        check=True,
                    )

            subprocess.run(["tmux", "kill-session", "-t", current_session])
        except Exception as e:
            print(f"[ERROR] Teleport failed: {e}")
            sys.exit(1)
    else:
        print(
            f"\n[!] You are not in tmux. To view the new agent, run:\n"
            f"    tmux attach-session -t {session_name}"
        )
        try:
            input(
                "\nPress Enter to safely exit this session and kill the current agent..."
            )
        except (EOFError, KeyboardInterrupt):
            pass
        parent_pid = os.getppid()
        try:
            os.kill(parent_pid, signal.SIGTERM)
        except Exception as e:
            print(f"[ERROR] Could not self-terminate: {e}")
