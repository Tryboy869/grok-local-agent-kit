"""JSONL conversation transcripts stored locally."""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


def default_dir() -> Path:
    env = os.environ.get("GROK_AGENT_TRANSCRIPT_DIR", "").strip()
    if env:
        return Path(env).expanduser()
    return Path.home() / ".grok-agent" / "transcripts"


def _stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def new_path(session_id: str = "chat", directory: Optional[Path] = None) -> Path:
    d = directory or default_dir()
    d.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in session_id)[:40]
    return d / f"{_stamp()}-{safe}.jsonl"


def append_turn(path: Path, role: str, content: str, extra: Optional[Dict[str, Any]] = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    rec: Dict[str, Any] = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "role": role,
        "content": content,
    }
    if extra:
        rec.update(extra)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def read_transcript(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    rows: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def list_transcripts(directory: Optional[Path] = None) -> List[Path]:
    d = directory or default_dir()
    if not d.exists():
        return []
    return sorted(d.glob("*.jsonl"), reverse=True)


def summarize(path: Path) -> str:
    rows = read_transcript(path)
    users = sum(1 for r in rows if r.get("role") == "user")
    asst = sum(1 for r in rows if r.get("role") == "assistant")
    tools = sum(1 for r in rows if r.get("role") == "tool")
    return f"{path.name}: {len(rows)} turns (user={users} assistant={asst} tool={tools})"


def dump_messages(rows: Iterable[Dict[str, Any]]) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for r in rows:
        role = str(r.get("role") or "user")
        content = str(r.get("content") or "")
        if role in {"user", "assistant", "system", "tool"} and content:
            out.append({"role": role if role != "tool" else "assistant", "content": content})
    return out
