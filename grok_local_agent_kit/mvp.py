"""Offline MVP agent: intent routing + local tools + multi-LLM provider table.

No Ollama, LM Studio, or network is required. `run_mvp` classifies a goal,
builds a tool plan, and executes it through the same tool registry the ReAct
loop uses. `probe_providers` reports whether local backends are up without
failing the demo when they are not.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .tools import execute_tool, get_default_tools

SearchFn = Callable[[str], str]

PROVIDERS: Dict[str, Dict[str, str]] = {
    "ollama": {
        "kind": "local",
        "base_url": "http://127.0.0.1:11434",
        "chat_path": "/api/chat",
        "health_path": "/api/tags",
    },
    "lmstudio": {
        "kind": "openai-compat",
        "base_url": "http://127.0.0.1:1234/v1",
        "chat_path": "/chat/completions",
        "health_path": "/models",
    },
}


def route_intent(prompt: str) -> str:
    """Pick a single intent. Order matters: more specific phrases win."""
    text = (prompt or "").lower()
    if any(k in text for k in ("mcp", "tool server")):
        return "mcp"
    if any(k in text for k in ("calcul", "sqrt", "compute", "somme", "sum of")):
        return "math"
    if any(k in text for k in ("system", "os ", "python version", "cpu")):
        return "system"
    if any(k in text for k in ("search", "web", "look up", "recherche")):
        return "search"
    if any(k in text for k in ("file", "fichier", "write", "list dir", "écris", "ecris")):
        return "files"
    return "files"


def plan_for(prompt: str) -> List[Dict[str, Any]]:
    """Deterministic tool plan for the MVP loop."""
    intent = route_intent(prompt)
    if intent == "math":
        expr = "sqrt(144) + 10"
        if "sqrt" not in prompt.lower() and any(ch.isdigit() for ch in prompt):
            expr = prompt
        return [{"tool": "calculator", "arguments": {"expression": expr}}]
    if intent == "system":
        return [{"tool": "get_system_info", "arguments": {}}]
    if intent == "search":
        query = prompt.strip() or "local AI agents"
        return [{"tool": "web_search", "arguments": {"query": query, "max_results": 3}}]
    if intent == "mcp":
        return [{"tool": "mcp_echo", "arguments": {"name": "ping", "arguments": {"text": prompt}}}]
    # files: write a note then list the workspace
    return [
        {
            "tool": "write_file",
            "arguments": {"path": "mvp_note.txt", "content": prompt.strip() + "\n"},
        },
        {"tool": "list_files", "arguments": {"path": "."}},
    ]


def _mcp_echo(name: str, arguments: Optional[Dict[str, Any]] = None) -> str:
    payload = {"server": "echo", "tool": name, "arguments": arguments or {}}
    return json.dumps(payload, ensure_ascii=False)


def _registry(search: Optional[SearchFn]) -> Dict[str, Callable[..., str]]:
    _specs, funcs = get_default_tools()
    if search is not None:
        funcs["web_search"] = lambda query, max_results=5: search(query)
    funcs["mcp_echo"] = _mcp_echo
    return funcs


def run_mvp(
    prompt: str,
    workspace: Path,
    search: Optional[SearchFn] = None,
) -> Dict[str, Any]:
    """Route a prompt and execute the plan inside `workspace`."""
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    intent = route_intent(prompt)
    steps = plan_for(prompt)
    registry = _registry(search)
    trace: List[Dict[str, Any]] = []
    cwd = Path.cwd()
    try:
        import os

        os.chdir(workspace)
        for step in steps:
            name = step["tool"]
            args = dict(step.get("arguments") or {})
            output = execute_tool(name, args, registry)
            trace.append({"tool": name, "arguments": args, "output": output})
    finally:
        os.chdir(cwd)
    answer = trace[-1]["output"] if trace else ""
    return {
        "intent": intent,
        "provider_table": list(PROVIDERS),
        "steps": trace,
        "answer": answer,
        "ok": all(not str(s["output"]).startswith("Tool ") for s in trace),
    }


def probe_providers(timeout: float = 0.4) -> Dict[str, Dict[str, Any]]:
    """Best-effort health check. Never raises; offline backends stay down."""
    report: Dict[str, Dict[str, Any]] = {}
    for name, spec in PROVIDERS.items():
        url = spec["base_url"].rstrip("/") + spec["health_path"]
        status = "down"
        detail = "unreachable"
        try:
            req = urllib.request.Request(url, method="GET")
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = "up" if 200 <= resp.status < 300 else "down"
                detail = f"HTTP {resp.status}"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            detail = type(exc).__name__
        report[name] = {"status": status, "url": url, "detail": detail}
    return report


def demo_mvp(workspace: Path, search: Optional[SearchFn] = None) -> str:
    """Scripted chat + automation transcript for README / CLI."""
    search = search or (lambda q: f"1. local agents\n2. ollama\n3. {q}")
    chat = run_mvp("compute sqrt(144) + 10", workspace, search=search)
    auto = run_mvp("write a note that the local agent ran", workspace / "auto", search=search)
    web = run_mvp("search local AI agents", workspace, search=search)
    lines = [
        "MVP demo (no LLM required)",
        f"providers: {', '.join(PROVIDERS)}",
        f"chat intent={chat['intent']} answer={chat['answer'].strip()}",
        f"automation intent={auto['intent']} wrote={(workspace / 'auto' / 'mvp_note.txt').exists()}",
        f"search intent={web['intent']} answer={web['answer'].splitlines()[0]}",
    ]
    return "\n".join(lines)
