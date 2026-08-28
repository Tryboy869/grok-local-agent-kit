"""Named session histories stored under .grok/sessions/ (cwd-safe)."""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


HISTORY_VERSION = "0.9.1"
_SAFE_NAME = re.compile(r"[^a-zA-Z0-9._-]+")


def session_root() -> Path:
    root = Path.cwd().resolve() / ".grok" / "sessions"
    root.mkdir(parents=True, exist_ok=True)
    return root


def sanitize_session_name(name: str) -> str:
    cleaned = _SAFE_NAME.sub("-", (name or "default").strip())[:64].strip("-.")
    return cleaned or "default"


def session_path(name: str) -> Path:
    return session_root() / f"{sanitize_session_name(name)}.json"


def list_sessions() -> List[str]:
    root = session_root()
    return sorted(p.stem for p in root.glob("*.json") if p.is_file())


def save_session(
    name: str,
    history: List[Dict[str, Any]],
    extra: Optional[Dict[str, Any]] = None,
) -> str:
    p = session_path(name)
    payload: Dict[str, Any] = {
        "history": history,
        "version": HISTORY_VERSION,
        "name": sanitize_session_name(name),
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        payload.update(extra)
    p.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    return (
        f"Saved session '{sanitize_session_name(name)}' "
        f"({len(history)} messages) to {p}"
    )


def load_session(name: str) -> Dict[str, Any]:
    p = session_path(name)
    if not p.is_file():
        raise FileNotFoundError(
            f"Session '{sanitize_session_name(name)}' not found at {p}"
        )
    data = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Invalid session file")
    data.setdefault("history", [])
    return data
