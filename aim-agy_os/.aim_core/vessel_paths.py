#!/usr/bin/env python3
"""
Vessel path resolution for multi-CLI A.I.M. on aim-codex (Codex primary).

Codex session layout (observed 2026-07):
  ~/.codex/sessions/YYYY/MM/rollout-<iso>-<session_id>.jsonl
  First line often session_meta with payload.cwd + payload.session_id

Also supports Grok / AGY discovery for cross-vessel tooling, but prefer=auto
on this vessel returns Codex first when any Codex rollouts exist for the cwd.
"""
from __future__ import annotations

import glob
import json
import os
import urllib.parse
from typing import List, Optional


def codex_sessions_root() -> str:
    return os.path.expanduser("~/.codex/sessions")


def grok_sessions_root() -> str:
    return os.path.expanduser("~/.grok/sessions")


def agy_brain_root() -> str:
    return os.path.expanduser("~/.gemini/antigravity-cli/brain")


def encode_workspace_cwd(cwd: str) -> str:
    abs_cwd = os.path.abspath(cwd)
    return urllib.parse.quote(abs_cwd, safe="")


def session_id_from_transcript_path(path: str) -> str:
    """
    Prefer UUID from Codex rollout filename or parent dir for known basenames.
    rollout-2026-07-17T01-10-19-019f6e7b-91cf-7db0-9ab7-86cf377f700b.jsonl
    """
    base = os.path.basename(path)
    if base.startswith("rollout-") and base.endswith(".jsonl"):
        # UUID is last 36 chars before .jsonl when hyphenated standard form
        stem = base[: -len(".jsonl")]
        # split after last timestamp segment: rollout-<date>T<time>-<uuid>
        parts = stem.split("-")
        # uuid has 5 hyphen groups at end: 8-4-4-4-12 → rejoin last 5
        if len(parts) >= 5:
            maybe = "-".join(parts[-5:])
            if len(maybe) >= 32:
                return maybe
        return stem
    if base in (
        "chat_history.jsonl",
        "updates.jsonl",
        "transcript.jsonl",
        "history.jsonl",
    ):
        return os.path.basename(os.path.dirname(path))
    stem = base.replace(".jsonl", "")
    return stem


def _read_session_meta_cwd(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            for _ in range(5):
                line = f.readline()
                if not line.strip():
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if not isinstance(msg, dict):
                    continue
                if msg.get("type") != "session_meta":
                    continue
                pl = msg.get("payload") or {}
                if isinstance(pl, dict) and pl.get("cwd"):
                    return os.path.abspath(str(pl["cwd"]))
    except OSError:
        pass
    return None


def find_codex_transcripts(
    project_root: str,
    explicit_session_id: Optional[str] = None,
) -> List[str]:
    """Return Codex rollout.jsonl paths for this workspace, newest first."""
    root = codex_sessions_root()
    if not os.path.isdir(root):
        return []
    project_dir = os.path.abspath(project_root)
    found: List[str] = []
    # Layout: ~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl (also tolerate shallower trees)
    patterns = (
        os.path.join(root, "*", "*", "*", "rollout-*.jsonl"),
        os.path.join(root, "*", "*", "rollout-*.jsonl"),
        os.path.join(root, "**", "rollout-*.jsonl"),
    )
    seen = set()
    candidates: List[str] = []
    for pattern in patterns:
        for path in glob.glob(pattern, recursive=True):
            if path not in seen and os.path.isfile(path):
                seen.add(path)
                candidates.append(path)
    for path in candidates:
        if explicit_session_id:
            if explicit_session_id in path:
                found.append(path)
            continue
        meta_cwd = _read_session_meta_cwd(path)
        if meta_cwd and os.path.abspath(meta_cwd) == project_dir:
            found.append(path)
    found.sort(key=os.path.getmtime, reverse=True)
    return found


def find_grok_transcripts(
    project_root: str,
    explicit_session_id: Optional[str] = None,
    prefer_durable: bool = True,
) -> List[str]:
    found: List[str] = []
    seen = set()
    ws_dir = os.path.join(grok_sessions_root(), encode_workspace_cwd(project_root))

    def _add(path: Optional[str]) -> None:
        if path and os.path.isfile(path) and path not in seen:
            seen.add(path)
            found.append(path)

    def _pick(session_dir: str) -> None:
        updates = os.path.join(session_dir, "updates.jsonl")
        chat = os.path.join(session_dir, "chat_history.jsonl")
        if prefer_durable and os.path.isfile(updates):
            _add(updates)
        elif os.path.isfile(chat):
            _add(chat)
        elif os.path.isfile(updates):
            _add(updates)

    if explicit_session_id:
        for session_dir in (
            os.path.join(ws_dir, explicit_session_id),
            *glob.glob(os.path.join(grok_sessions_root(), "*", explicit_session_id)),
        ):
            if os.path.isdir(session_dir):
                _pick(session_dir)
        found.sort(key=os.path.getmtime, reverse=True)
        return found

    if os.path.isdir(ws_dir):
        for entry in glob.glob(os.path.join(ws_dir, "*")):
            if os.path.isdir(entry):
                _pick(entry)
    found.sort(key=os.path.getmtime, reverse=True)
    return found


def find_agy_transcripts(
    project_root: str,
    explicit_session_id: Optional[str] = None,
) -> List[str]:
    found: List[str] = []
    brain = agy_brain_root()
    if explicit_session_id:
        path = os.path.join(
            brain, explicit_session_id, ".system_generated", "logs", "transcript.jsonl"
        )
        if os.path.isfile(path):
            found.append(path)
        return found
    history_file = os.path.expanduser("~/.gemini/antigravity-cli/history.jsonl")
    if os.path.isfile(history_file):
        try:
            project_dir = os.path.abspath(project_root)
            with open(history_file, "r", encoding="utf-8") as f:
                for line in f:
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if data.get("workspace") != project_dir:
                        continue
                    cid = data.get("conversationId")
                    if not cid:
                        continue
                    path = os.path.join(
                        brain, cid, ".system_generated", "logs", "transcript.jsonl"
                    )
                    if os.path.isfile(path) and path not in found:
                        found.append(path)
        except Exception:
            pass
    found.sort(key=os.path.getmtime, reverse=True)
    return found


def find_session_transcripts(
    project_root: str,
    explicit_session_id: Optional[str] = None,
    prefer: str = "auto",
    prefer_durable: bool = True,
) -> List[str]:
    """
    prefer: codex | grok | agy | auto
    auto on aim-codex: Codex first, then Grok, then AGY.
    """
    prefer = (prefer or "auto").lower()
    if prefer == "codex":
        return find_codex_transcripts(project_root, explicit_session_id)
    if prefer == "grok":
        return find_grok_transcripts(
            project_root, explicit_session_id, prefer_durable=prefer_durable
        )
    if prefer == "agy":
        return find_agy_transcripts(project_root, explicit_session_id)

    codex = find_codex_transcripts(project_root, explicit_session_id)
    if codex:
        return codex
    grok = find_grok_transcripts(
        project_root, explicit_session_id, prefer_durable=prefer_durable
    )
    if grok:
        return grok
    return find_agy_transcripts(project_root, explicit_session_id)


def default_tmp_chats_dir() -> str:
    return codex_sessions_root()
