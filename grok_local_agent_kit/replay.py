"""Replay an exported ReAct trace without calling a live LLM.

Useful for debugging tool sequences and writing regression tests.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


def load_trace(path: str | Path) -> List[dict]:
    raw = Path(path).read_text(encoding="utf-8")
    data = json.loads(raw)
    if isinstance(data, dict) and "trace" in data:
        data = data["trace"]
    if not isinstance(data, list):
        raise ValueError('trace must be a list or {"trace": [...]}')
    return data


def summarize_trace(trace: List[dict]) -> str:
    lines: List[str] = []
    for i, ev in enumerate(trace):
        kind = ev.get("type") or ev.get("kind") or ev.get("event") or "event"
        extra = ev.get("name") or ev.get("tool") or ev.get("thought") or ev.get("text") or ""
        if isinstance(extra, str) and len(extra) > 80:
            extra = extra[:77] + "..."
        lines.append(f"{i:03d}  {kind}  {extra}")
    return "\n".join(lines) if lines else "(empty trace)"


def replay_tools(
    trace: List[dict],
    registry: Optional[Dict[str, Callable[..., str]]] = None,
    dry_run: bool = False,
) -> List[dict]:
    if registry is None:
        from .tools import TOOL_FUNCS

        registry = TOOL_FUNCS

    results: List[dict] = []
    for ev in trace:
        name = ev.get("name") or ev.get("tool")
        kind = (ev.get("type") or ev.get("kind") or ev.get("event") or "").lower()
        if not name:
            continue
        if kind and kind not in {"tool", "tool_call", "tool_result", "call"}:
            if "arguments" not in ev and "args" not in ev:
                continue
        args = ev.get("arguments") or ev.get("args") or {}
        if not isinstance(args, dict):
            args = {}
        if dry_run or name not in registry:
            results.append({"name": name, "ok": name in registry, "dry_run": True, "args": args})
            continue
        try:
            out = registry[name](**args)
            results.append({"name": name, "ok": True, "output": out})
        except Exception as e:
            results.append({"name": name, "ok": False, "error": str(e)})
    return results


def replay_file(path: str | Path, dry_run: bool = True) -> dict[str, Any]:
    trace = load_trace(path)
    return {
        "events": len(trace),
        "summary": summarize_trace(trace),
        "tools": replay_tools(trace, dry_run=dry_run),
    }
