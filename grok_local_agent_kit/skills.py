"""Skill manifests: JSON files that register extra tools on an agent."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

DEFAULT_SKILL_DIR = Path(".grok") / "skills"


def _make_template_tool(template: str) -> Callable[..., str]:
    def _fn(**kwargs: Any) -> str:
        try:
            return template.format(**kwargs)
        except Exception as e:
            return f"skill template error: {e}"

    return _fn


def _make_python_tool(expr: str) -> Callable[..., str]:
    def _fn(**kwargs: Any) -> str:
        try:
            return str(eval(expr, {"__builtins__": {}}, dict(kwargs)))
        except Exception as e:
            return f"skill python error: {e}"

    return _fn


def load_skill_file(path: Path) -> List[Dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    tools = data.get("tools") or []
    registered: List[Dict[str, Any]] = []
    for spec in tools:
        name = spec.get("name")
        if not name:
            continue
        kind = (spec.get("kind") or "template").lower()
        if kind == "python":
            func = _make_python_tool(spec.get("expr") or "''")
        else:
            func = _make_template_tool(spec.get("template") or "{msg}")
        registered.append(
            {
                "name": name,
                "func": func,
                "description": spec.get("description") or f"Skill tool {name}",
                "parameters": spec.get("parameters")
                or {"type": "object", "properties": {}},
            }
        )
    return registered


def discover_skill_files(directory: Optional[str] = None) -> List[Path]:
    root = Path(directory) if directory else DEFAULT_SKILL_DIR
    if not root.exists():
        return []
    return sorted(p for p in root.glob("*.json") if p.is_file())


def load_skills(agent: Any, directory: Optional[str] = None) -> List[str]:
    added: List[str] = []
    for path in discover_skill_files(directory):
        try:
            tools = load_skill_file(path)
        except Exception:
            continue
        for t in tools:
            if t["name"] in getattr(agent, "tool_funcs", {}):
                continue
            agent.register_tool(t["name"], t["func"], t["description"], t["parameters"])
            added.append(t["name"])
    return added
