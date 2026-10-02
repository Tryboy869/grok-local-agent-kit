"""Declarative offline workflows: file ops, web search, MCP echo.

No daemon required. Search and MCP handlers are injectable so CI never
hits the network or spawns a server.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


SearchFn = Callable[[str], str]
McpFn = Callable[[str, Dict[str, Any]], str]


def _safe(root: Path, rel: str) -> Path:
    root = root.resolve()
    target = (root / rel).resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"path escapes workspace: {rel}")
    return target


def _default_search(query: str) -> str:
    return (
        f"[offline-search] no live fetch for {query!r}. "
        "Pass search= to inject DuckDuckGo or a fixture."
    )


def _default_mcp(name: str, arguments: Dict[str, Any]) -> str:
    payload = {"server": "echo", "tool": name, "arguments": arguments}
    return json.dumps(payload, ensure_ascii=False)


@dataclass
class Workflow:
    name: str
    steps: List[Dict[str, Any]]
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "steps": self.steps, "meta": self.meta}


def load_workflow(path: str | Path) -> Workflow:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "steps" not in data:
        raise ValueError("workflow JSON needs a steps array")
    return Workflow(
        name=str(data.get("name") or Path(path).stem),
        steps=list(data["steps"]),
        meta=dict(data.get("meta") or {}),
    )


def run_workflow(
    workflow: Workflow | Dict[str, Any],
    workspace: str | Path,
    *,
    search: Optional[SearchFn] = None,
    mcp: Optional[McpFn] = None,
) -> Dict[str, Any]:
    if isinstance(workflow, dict):
        workflow = Workflow(
            name=str(workflow.get("name") or "inline"),
            steps=list(workflow.get("steps") or []),
            meta=dict(workflow.get("meta") or {}),
        )
    root = Path(workspace).resolve()
    root.mkdir(parents=True, exist_ok=True)
    search_fn = search or _default_search
    mcp_fn = mcp or _default_mcp
    trace: List[Dict[str, Any]] = []
    variables: Dict[str, str] = {}

    for index, step in enumerate(workflow.steps, start=1):
        kind = str(step.get("tool") or step.get("type") or "")
        args = dict(step.get("arguments") or step.get("args") or {})
        save_as = step.get("save_as")
        try:
            output = _dispatch(kind, args, root, search_fn, mcp_fn, variables)
            ok = True
            error = None
        except Exception as exc:  # noqa: BLE001 — workflow records the failure
            output = ""
            ok = False
            error = str(exc)
        if save_as and ok:
            variables[str(save_as)] = output
        trace.append(
            {
                "step": index,
                "tool": kind,
                "ok": ok,
                "output": output[:1200],
                "error": error,
            }
        )
        if not ok and step.get("required", True):
            break

    return {
        "name": workflow.name,
        "ok": all(item["ok"] for item in trace) and bool(trace),
        "steps": len(trace),
        "trace": trace,
        "variables": variables,
    }


def _expand(value: Any, variables: Dict[str, str]) -> Any:
    if isinstance(value, str):
        out = value
        for key, stored in variables.items():
            out = out.replace("{{" + key + "}}", stored)
        return out
    if isinstance(value, dict):
        return {k: _expand(v, variables) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand(v, variables) for v in value]
    return value


def _dispatch(
    kind: str,
    args: Dict[str, Any],
    root: Path,
    search_fn: SearchFn,
    mcp_fn: McpFn,
    variables: Dict[str, str],
) -> str:
    args = _expand(args, variables)
    if kind in {"list_files", "file.list"}:
        rel = str(args.get("path") or ".")
        target = _safe(root, rel)
        if not target.exists():
            return f"(missing) {rel}"
        names = sorted(p.name for p in target.iterdir())
        return "\n".join(names) if names else "(empty)"
    if kind in {"write_file", "file.write"}:
        path = _safe(root, str(args["path"]))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(args.get("content") or ""), encoding="utf-8")
        return f"wrote {path.name} ({path.stat().st_size} bytes)"
    if kind in {"read_file", "file.read"}:
        path = _safe(root, str(args["path"]))
        return path.read_text(encoding="utf-8")
    if kind in {"web_search", "search"}:
        return search_fn(str(args.get("query") or ""))
    if kind in {"mcp_call", "mcp"}:
        name = str(args.get("name") or "echo")
        call_args = dict(args.get("arguments") or {})
        return mcp_fn(name, call_args)
    if kind in {"note", "log"}:
        return str(args.get("text") or "")
    raise ValueError(f"unknown workflow tool: {kind}")


def demo_workflow(workspace: Optional[Path] = None) -> str:
    """Chat-style list, automation write, fixture search, MCP echo. No daemon."""
    import tempfile

    owned = workspace is None
    root = workspace or Path(tempfile.mkdtemp(prefix="glak-workflow-"))
    root.mkdir(parents=True, exist_ok=True)
    (root / "inbox.txt").write_text("hello local agent\n", encoding="utf-8")
    spec = {
        "name": "mvp-routing-tools",
        "steps": [
            {"tool": "list_files", "arguments": {"path": "."}, "save_as": "listing"},
            {
                "tool": "write_file",
                "arguments": {
                    "path": "automation-note.txt",
                    "content": "automation agent wrote this without a cloud key\n",
                },
            },
            {
                "tool": "web_search",
                "arguments": {"query": "ollama lm studio local agents"},
                "save_as": "hits",
            },
            {
                "tool": "mcp_call",
                "arguments": {"name": "echo", "arguments": {"text": "{{listing}}"}},
            },
        ],
    }

    def fixture_search(query: str) -> str:
        return f"1. Ollama local models\n2. LM Studio OpenAI-compatible server\nquery={query}"

    result = run_workflow(spec, root, search=fixture_search)
    lines = [
        f"workflow={result['name']} ok={result['ok']} steps={result['steps']}",
        "providers=ollama,lmstudio (router stays outside this offline path)",
        "tools=list_files,write_file,web_search,mcp_call",
    ]
    for item in result["trace"]:
        preview = item["output"].replace("\n", " | ")[:140]
        lines.append(f"  {item['step']}. {item['tool']} ok={item['ok']} {preview}")
    note = root / "automation-note.txt"
    lines.append(f"wrote={note.is_file()}")
    if owned:
        lines.append(f"workspace={root}")
    return "\n".join(lines)
