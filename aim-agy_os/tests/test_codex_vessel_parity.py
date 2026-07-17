"""TDD: Codex vessel parity — paths, extract, naming, teleport resolve."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from unittest import mock

import pytest

CORE = Path(__file__).resolve().parents[1] / ".aim_core"
FIXTURE = Path(__file__).resolve().parent / "fixtures" / "codex_rollout_sample.jsonl"
sys.path.insert(0, str(CORE))


def test_detect_and_extract_codex_fixture():
    from extract_signal import (
        conversational_turn_count,
        detect_jsonl_kind,
        extract_signal,
    )

    assert FIXTURE.is_file()
    assert detect_jsonl_kind(str(FIXTURE)) == "codex_rollout"
    sig = extract_signal(str(FIXTURE))
    assert isinstance(sig, list)
    assert conversational_turn_count(sig) >= 2
    blob = " ".join((t.get("text") or "") for t in sig)
    assert "PHOENIX_CODEX" in blob
    assert "ALPHA" in blob


def test_session_id_from_codex_rollout_name():
    from vessel_paths import session_id_from_transcript_path

    p = (
        "/home/x/.codex/sessions/2026/07/17/"
        "rollout-2026-07-17T01-10-19-019f6e7b-91cf-7db0-9ab7-86cf377f700b.jsonl"
    )
    sid = session_id_from_transcript_path(p)
    assert "019f6e7b" in sid
    assert sid.endswith("86cf377f700b") or "91cf" in sid


def test_find_codex_transcripts_by_cwd(tmp_path, monkeypatch):
    from vessel_paths import find_codex_transcripts

    # Real layout: sessions/YYYY/MM/DD/rollout-*.jsonl
    root = tmp_path / "sessions" / "2026" / "07" / "17"
    root.mkdir(parents=True)
    proj = tmp_path / "aim-codex-proj"
    proj.mkdir()
    path = root / "rollout-2026-07-17T00-00-00-aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee.jsonl"
    meta = {
        "timestamp": "t",
        "type": "session_meta",
        "payload": {
            "session_id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
            "cwd": str(proj),
        },
    }
    path.write_text(json.dumps(meta) + "\n", encoding="utf-8")
    monkeypatch.setattr(
        "vessel_paths.codex_sessions_root", lambda: str(tmp_path / "sessions")
    )
    found = find_codex_transcripts(str(proj))
    assert any(str(path) == f or path.name in f for f in found)


def test_vessel_cli_id_defaults_codex():
    from session_naming import vessel_cli_id

    assert vessel_cli_id({"AIM_VESSEL_CLI": "codex"}) == "codex"
    assert vessel_cli_id({"AIM_VESSEL_CLI": ""}) in ("codex", "agy")  # cwd-dependent


def test_resolve_vessel_cli_codex(monkeypatch):
    from reincarnation import teleport_engine

    monkeypatch.setenv("AIM_VESSEL_CLI", "codex")
    monkeypatch.setenv("CODEX_BIN", "/usr/bin/codex-fake")
    cli = teleport_engine._resolve_vessel_cli("/home/kingb/aim-codex")
    assert "codex" in cli[0]
