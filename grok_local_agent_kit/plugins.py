"""Drop-in tool plugins loaded from JSON or Python files.

Search order (first match wins per tool name):
1. GROK_AGENT_PLUGIN_DIR
2. ./tools
3. ~/.grok-agent/tools

Python plugins are sandboxed: they are NOT imported unless explicitly allowed.
JSON plugins are always loaded (data only, no code execution).
"""

from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

_SKIPPED_PY: List[Path] = []


def plugin_dirs() -> List[Path]:
    dirs: List[Path] = []
    env = os.environ.get("GROK_AGENT_PLUGIN_DIR", "").strip()
    if env:
        dirs.append(Path(env).expanduser())
    dirs.append(Path.cwd() / "tools")
    dirs.append(Path.home() / ".grok-agent" / "tools")
    out: List[Path] = []
    seen = set()
    for d in dirs:
        key = str(d.resolve()) if d.exists() else str(d)
        if key in seen:
            continue
        seen.add(key)
        out.append(d)
    return out


def _truthy(value: str | None) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def py_plugins_allowed() -> bool:
    """Global opt-in: GROK_AGENT_ALLOW_PY_PLUGINS=1."""
    return _truthy(os.environ.get("GROK_AGENT_ALLOW_PY_PLUGINS"))


def py_plugin_allowlist() -> set[str]:
    raw = os.environ.get("GROK_AGENT_PY_PLUGIN_ALLOWLIST", "")
    return {part.strip() for part in raw.split(",") if part.strip()}


def skipped_py_plugins() -> List[Path]:
    return list(_SKIPPED_PY)


def _may_load_py(path: Path, allow_py: bool | None) -> bool:
    if allow_py is True:
        return True
    if allow_py is False:
        return False
    if py_plugins_allowed():
        return True
    allow = py_plugin_allowlist()
    return path.stem in allow or path.name in allow


def _spec_from_meta(meta: Dict[str, Any]) -> Dict[str, Any]:
    name = str(meta.get("name") or "").strip()
    if not name:
        raise ValueError("plugin missing name")
    desc = str(meta.get("description") or name)
    params = meta.get("parameters") or {
        "type": "object",
        "properties": {"input": {"type": "string"}},
    }
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": desc,
            "parameters": params,
        },
    }


def _handler_from_json(meta: Dict[str, Any]) -> Callable[..., str]:
    kind = str(meta.get("kind") or "template")
    template = str(meta.get("template") or "{input}")
    static = meta.get("returns")

    def handler(**kwargs: Any) -> str:
        if static is not None:
            return str(static)
        if kind == "json":
            return json.dumps(kwargs, ensure_ascii=False)
        text = template
        for k, v in kwargs.items():
            text = text.replace("{" + k + "}", str(v))
        if not kwargs and "{input}" in template:
            return template
        return text

    handler.__name__ = str(meta.get("name") or "plugin")
    return handler


def load_json_plugin(path: Path) -> Tuple[Dict[str, Any], Callable[..., str]]:
    meta = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(meta, dict):
        raise ValueError(f"plugin {path} must be a JSON object")
    return _spec_from_meta(meta), _handler_from_json(meta)


def load_py_plugin(path: Path) -> Tuple[Dict[str, Any], Callable[..., str]]:
    spec = importlib.util.spec_from_file_location(f"grok_plugin_{path.stem}", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot import {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if hasattr(mod, "register"):
        spec_obj, fn = mod.register()
        return spec_obj, fn
    name = getattr(mod, "NAME", path.stem)
    desc = getattr(mod, "DESCRIPTION", name)
    params = getattr(mod, "PARAMETERS", {"type": "object", "properties": {}})
    fn = getattr(mod, "handler", None)
    if not callable(fn):
        raise ValueError(f"{path} has no handler() or register()")
    spec_obj = _spec_from_meta({"name": name, "description": desc, "parameters": params})
    return spec_obj, fn


def discover_plugins(
    extra_dirs: List[Path] | None = None,
    allow_py: bool | None = None,
) -> List[Tuple[str, Dict[str, Any], Callable[..., str]]]:
    global _SKIPPED_PY
    _SKIPPED_PY = []
    found: List[Tuple[str, Dict[str, Any], Callable[..., str]]] = []
    seen_names: set[str] = set()
    dirs = list(extra_dirs or []) + plugin_dirs()
    for d in dirs:
        if not d.exists() or not d.is_dir():
            continue
        files = sorted(list(d.glob("*.json")) + list(d.glob("*.py")))
        for path in files:
            if path.name.startswith("_"):
                continue
            try:
                if path.suffix == ".json":
                    spec_obj, fn = load_json_plugin(path)
                else:
                    if not _may_load_py(path, allow_py):
                        _SKIPPED_PY.append(path)
                        continue
                    spec_obj, fn = load_py_plugin(path)
                name = spec_obj["function"]["name"]
                if name in seen_names:
                    continue
                seen_names.add(name)
                found.append((name, spec_obj, fn))
            except Exception:
                continue
    return found


def apply_plugins(
    specs: List[Dict[str, Any]],
    funcs: Dict[str, Callable[..., str]],
    extra_dirs: List[Path] | None = None,
    allow_py: bool | None = None,
) -> Tuple[List[Dict[str, Any]], Dict[str, Callable[..., str]]]:
    specs = list(specs)
    funcs = dict(funcs)
    existing = {s.get("function", {}).get("name") for s in specs}
    for name, spec_obj, fn in discover_plugins(extra_dirs, allow_py=allow_py):
        funcs[name] = fn
        if name not in existing:
            specs.append(spec_obj)
            existing.add(name)
    return specs, funcs
