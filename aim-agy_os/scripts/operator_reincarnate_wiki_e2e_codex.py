#!/usr/bin/env python3
"""Codex-native operator reincarnation → memory-wiki E2E."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

VESSEL = Path(os.environ.get("AIM_VESSEL", os.getcwd())).resolve()
AIM = VESSEL / "aim-agy_os"
if not (AIM / ".aim_core").is_dir():
    AIM = VESSEL
PY3 = sys.executable
if (AIM / "venv" / "bin" / "python3").is_file():
    PY3 = str(AIM / "venv" / "bin" / "python3")
WIKI = AIM / "memory-wiki"
REPORT = AIM / "planning-artifacts" / "OPERATOR_E2E_REINCARNATE_WIKI_CODEX_LATEST.md"
MARKER = os.environ.get(
    "MARKER", f"OP_WIKI_CODEX_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
)
DIRECTIVES = [
    f"OPERATOR_DIRECTIVE_1: Codename SILVER_KEEL for Codex. Marker={MARKER}",
    f"OPERATOR_DIRECTIVE_2: Prefer exclusive Codex rollout pulse. Marker={MARKER}",
    f"OPERATOR_DIRECTIVE_3: Never claim Codex wiki works without grepping {MARKER}.",
]


def log(m: str) -> None:
    print(m, flush=True)


def _msg_row(role: str, text: str, ts: str) -> dict:
    return {
        "timestamp": ts,
        "type": "response_item",
        "payload": {
            "type": "message",
            "role": role,
            "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}],
        },
    }


def write_codex_rollout(path: Path, session_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    rows = [
        {
            "timestamp": now,
            "type": "session_meta",
            "payload": {"id": session_id, "cwd": str(VESSEL)},
        }
    ]
    turns = [
        "Wake up. Codex reincarnation memory test.",
        DIRECTIVES[0],
        DIRECTIVES[1],
        DIRECTIVES[2],
        "ok, reincarnate so memory-wiki keeps these directives.",
    ]
    for t in turns:
        rows.append(_msg_row("user", t, now))
        rows.append(_msg_row("assistant", f"Acknowledged: {t[:100]}", now))
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main() -> int:
    sid = "019fe2e1-cdx-4e2e-8e2e-" + hashlib.sha1(MARKER.encode()).hexdigest()[:12]
    day = datetime.now().strftime("%Y/%m/%d")
    stamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    rollout = (
        Path.home()
        / ".codex"
        / "sessions"
        / day
        / f"rollout-{stamp}-{sid}.jsonl"
    )
    write_codex_rollout(rollout, sid)
    log(f"=== CODEX E2E marker={MARKER} session={sid} file={rollout} ===")

    env = os.environ.copy()
    env["PYTHONPATH"] = str(AIM / ".aim_core") + os.pathsep + env.get("PYTHONPATH", "")
    env["AIM_WIKI_SKIP_LANCE"] = "1"
    daemon = WIKI / "daemon.log"
    WIKI.mkdir(parents=True, exist_ok=True)
    (WIKI / "pages").mkdir(parents=True, exist_ok=True)
    off = daemon.stat().st_size if daemon.exists() else 0
    cmd = [
        PY3,
        str(AIM / ".aim_core" / "handoff_pulse_generator.py"),
        "--session-id",
        sid,
    ]
    p = subprocess.run(
        cmd, cwd=str(VESSEL), env=env, capture_output=True, text=True, timeout=180
    )
    log(p.stdout or "")
    log(p.stderr or "")
    log(f"pulse exit={p.returncode}")

    daemon_new = ""
    deadline = time.time() + 60
    while time.time() < deadline:
        if daemon.exists():
            daemon_new = daemon.read_bytes()[off:].decode("utf-8", "replace")
            if "[SUCCESS] Deterministic" in daemon_new or "[FATAL]" in daemon_new:
                time.sleep(0.5)
                break
        time.sleep(0.4)
    log("--- daemon ---\n" + (daemon_new[-2000:] if daemon_new else "(empty)"))

    archives = list((AIM / "archive" / "history").glob(f"*_{sid}.md"))
    arch_ok = any(MARKER in a.read_text(errors="replace") for a in archives)
    pages = []
    for pg in (WIKI / "pages").glob("*.md") if (WIKI / "pages").is_dir() else []:
        if MARKER in pg.read_text(errors="replace"):
            pages.append(str(pg))
    fr = AIM / ".aim_core" / "temp" / "LAST_SESSION_FLIGHT_RECORDER.md"
    fr_ok = fr.exists() and MARKER in fr.read_text(errors="replace")
    gates = {
        "pulse_exit_0": p.returncode == 0,
        "exclusive_in_stdout": sid in (p.stdout or ""),
        "archive_marker": arch_ok,
        "flight_marker": fr_ok,
        "daemon_success": "[SUCCESS] Deterministic wiki reincarnation sequence complete."
        in daemon_new,
        "wiki_pages_marker": len(pages) > 0,
    }
    hard = all(gates.values())
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(
        f"# Codex Operator E2E\n\n**VERDICT: {'PASS' if hard else 'FAIL'}**\n\n"
        f"marker={MARKER}\nsession={sid}\n\n"
        + "\n".join(f"- {k}: {v}" for k, v in gates.items())
        + "\n\npages:\n"
        + "\n".join(pages)
        + f"\n\nstdout:\n{(p.stdout or '')[-1500:]}\n",
        encoding="utf-8",
    )
    log(f"=== VERDICT {'PASS' if hard else 'FAIL'} {gates} ===")
    try:
        rollout.unlink()
    except Exception:
        pass
    return 0 if hard else 2


if __name__ == "__main__":
    sys.exit(main())
