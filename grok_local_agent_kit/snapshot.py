"""v0.39 — portable kit snapshot (no live LLM).

Collects version, available tools, optional health.json / roster / board
presence, and a short doctor-style report into one JSON document.
"""

from __future__ import annotations

import json
import os
import platform
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _cwd_safe(path: str | Path) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = Path.cwd() / p
    return p.resolve()


@dataclass
class Snapshot:
    version: str
    created_at: str
    python: str
    platform: str
    cwd: str
    tools: list[str] = field(default_factory=list)
    files: dict[str, bool] = field(default_factory=dict)
    health: dict[str, Any] = field(default_factory=dict)
    extras: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def dumps(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False) + "\n"


def _tool_names() -> list[str]:
    try:
        from .tools import get_default_tools

        tools = get_default_tools()
        names: list[str] = []
        for t in tools:
            if isinstance(t, dict):
                fn = t.get("function") or t
                names.append(str(fn.get("name") or t.get("name") or "?"))
            else:
                names.append(getattr(t, "name", str(t)))
        return sorted(set(names))
    except Exception as exc:  # pragma: no cover - defensive
        return [f"<tools-error:{exc}>"]


def _file_presence(paths: dict[str, str]) -> dict[str, bool]:
    out = {}
    for label, rel in paths.items():
        out[label] = _cwd_safe(rel).is_file()
    return out


def _health_summary(path: str = "health.json") -> dict[str, Any]:
    p = _cwd_safe(path)
    if not p.is_file():
        return {"present": False, "path": str(p)}
    try:
        from .health import load_board, format_board as format_health

        board = load_board(p)
        return {
            "present": True,
            "path": str(p),
            "text": format_health(board) if callable(format_health) else str(board),
        }
    except Exception as exc:
        return {"present": True, "path": str(p), "error": str(exc)}


def collect(
    *,
    health_path: str = "health.json",
    extra_files: dict[str, str] | None = None,
) -> Snapshot:
    from . import __version__

    files = {
        "health.json": health_path,
        "roster.json": "roster.json",
        "board.jsonl": "board.jsonl",
        "grok-agent.toml": "grok-agent.toml",
    }
    if extra_files:
        files.update(extra_files)
    return Snapshot(
        version=__version__,
        created_at=_now(),
        python=sys.version.split()[0],
        platform=f"{platform.system()} {platform.release()}",
        cwd=str(Path.cwd()),
        tools=_tool_names(),
        files=_file_presence(files),
        health=_health_summary(health_path),
        extras={"pid": os.getpid(), "argv0": sys.argv[0] if sys.argv else ""},
    )


def write_snapshot(path: str | Path = "kit-snapshot.json", **kwargs: Any) -> Path:
    dest = _cwd_safe(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    snap = collect(**kwargs)
    dest.write_text(snap.dumps(), encoding="utf-8")
    return dest


def load_snapshot(path: str | Path = "kit-snapshot.json") -> dict[str, Any]:
    p = _cwd_safe(path)
    return json.loads(p.read_text(encoding="utf-8"))


def format_snapshot(snap: Snapshot | dict[str, Any] | None = None) -> str:
    if snap is None:
        snap = collect()
    data = snap.to_dict() if isinstance(snap, Snapshot) else snap
    tools = data.get("tools") or []
    tool_preview = ", ".join(tools)
    if len(tool_preview) > 200:
        tool_preview = tool_preview[:197] + "..."
    lines = [
        f"kit-snapshot v{data.get('version')}",
        f"created={data.get('created_at')} python={data.get('python')} {data.get('platform')}",
        f"cwd={data.get('cwd')}",
        f"tools={len(tools)}: {tool_preview}",
    ]
    files = data.get("files") or {}
    for name, ok in files.items():
        lines.append(f"  file {name}: {'yes' if ok else 'no'}")
    health = data.get("health") or {}
    if health.get("present"):
        lines.append("  health: present")
        text = health.get("text")
        if text:
            for row in str(text).splitlines()[:8]:
                lines.append(f"    {row}")
    else:
        lines.append("  health: absent")
    return "\n".join(lines)


def demo_snapshot(path: str = "kit-snapshot.json") -> str:
    dest = write_snapshot(path)
    loaded = load_snapshot(dest)
    body = format_snapshot(loaded)
    return f"wrote={dest}\n{body}\n"
