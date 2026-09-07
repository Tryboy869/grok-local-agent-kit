"""Tiny recipe runner — TOML/JSON multi-step automations without an LLM."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


@dataclass
class RecipeStep:
    name: str
    tool: str
    args: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Recipe:
    name: str
    description: str = ""
    steps: List[RecipeStep] = field(default_factory=list)


def _load_raw(path: str | Path) -> dict:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() in {".json"}:
        data = json.loads(text)
    else:
        try:
            import tomllib
        except ImportError:  # pragma: no cover
            import tomli as tomllib  # type: ignore
        data = tomllib.loads(text)
    if not isinstance(data, dict):
        raise ValueError("recipe root must be a table/object")
    return data


def load_recipe(path: str | Path) -> Recipe:
    data = _load_raw(path)
    steps_raw = data.get("steps") or data.get("step") or []
    steps: List[RecipeStep] = []
    for i, item in enumerate(steps_raw):
        if not isinstance(item, dict):
            raise ValueError(f"step {i} is not a table")
        tool = item.get("tool") or item.get("name")
        if not tool:
            raise ValueError(f"step {i} missing tool")
        args = item.get("args") or {k: v for k, v in item.items() if k not in {"tool", "name", "args"}}
        steps.append(RecipeStep(name=str(item.get("name") or tool), tool=str(tool), args=dict(args)))
    return Recipe(
        name=str(data.get("name") or Path(path).stem),
        description=str(data.get("description") or ""),
        steps=steps,
    )


def run_recipe(
    recipe: Recipe,
    registry: Optional[Dict[str, Callable[..., str]]] = None,
) -> List[dict]:
    from .tools import TOOL_FUNCS, execute_tool

    funcs = registry or dict(TOOL_FUNCS)
    results = []
    for step in recipe.steps:
        out = execute_tool(step.tool, step.args, funcs)
        results.append({"name": step.name, "tool": step.tool, "output": out})
    return results


def format_results(results: List[dict]) -> str:
    chunks = []
    for i, row in enumerate(results, 1):
        chunks.append(f"## {i}. {row['name']} ({row['tool']})\n{row['output']}")
    return "\n\n".join(chunks) if chunks else "(empty recipe)"
