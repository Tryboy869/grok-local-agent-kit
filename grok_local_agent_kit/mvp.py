"""Offline MVP agent: intent routing + local tools + multi-LLM provider table.

No Ollama, LM Studio, or network is required. `run_mvp` classifies a goal,
builds a tool plan, and executes it through the same tool registry the ReAct
loop uses. `probe_providers` reports whether local backends are up without
failing the demo when they are not.

v0.62: improved compound intent detection (math + save to file).
"""

from __future__ import annotations

import json
import re
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
    text = (prompt or "").lower().strip()
    # MCP first (explicit)
    if any(k in text for k in ("mcp", "tool server", "echo server", "mcp_call")):
        return "mcp"
    # Math: keywords or expression-like
    math_kw = ("calcul", "sqrt", "compute", "somme", "sum of", "plus", "minus", "times", "multiply", "evaluate", "math")
    if any(k in text for k in math_kw) or re.search(r"\b\d+\s*[+\-*/^]\s*\d+", text) or re.search(r"sqrt\s*\(", text) or "**" in text:
        return "math"
    if any(k in text for k in ("date", "time", "datetime", "heure", "aujourd'hui", "today", "clock", "what time")):
        return "datetime"
    if any(k in text for k in ("system", "os ", "python version", "cpu", "memory", "hostname", "sysinfo")):
        return "system"
    if any(k in text for k in ("search", "web", "look up", "recherche", "find online", "google", "lookup")):
        return "search"
    if any(k in text for k in ("read", "open", "show file", "cat ", "display")) and any(k in text for k in ("file", "fichier", ".txt", ".md")):
        return "read"
    if any(k in text for k in ("file", "fichier", "write", "list dir", "écris", "ecris", "create note", "save", "list files")):
        return "files"
    return "files"


def plan_for(prompt: str) -> List[Dict[str, Any]]:
    """Deterministic tool plan for the MVP loop.

    Supports simple compound goals like "calculate X and save to file".
    """
    text = (prompt or "").lower()
    intent = route_intent(prompt)

    # Compound: math + write/save
    compound_math_save = (
        intent == "math"
        and any(k in text for k in ("save", "write", "save to", "write to", "and save", "then write", "store in"))
    )

    if compound_math_save:
        # Extract expression similar to pure math
        expr = "sqrt(144) + 10"
        cleaned = re.sub(
            r"^(compute|calculate|calc|somme|sum of|what is|what's|evaluate|math|please|calculate the)\s+",
            "",
            prompt,
            flags=re.I,
        ).strip()
        cleaned = re.sub(r"\s*\?+\s*$", "", cleaned)
        m = re.search(r"([0-9.+*/()^sqrt\s\-]+|\*\*)", cleaned, re.I)
        candidate = (m.group(1).strip() if m else cleaned).strip()
        if "**" in candidate:
            candidate = candidate.replace("**", "^")
        if any(ch.isdigit() for ch in candidate) and any(op in candidate for op in "+-*/()^"):
            expr = candidate
        # Determine output filename
        fname = "result.txt"
        fm = re.search(r"(?:to|in|as)\s+([a-zA-Z0-9_.-]+\.(?:txt|md))", text)
        if fm:
            fname = fm.group(1)
        return [
            {"tool": "calculator", "arguments": {"expression": expr}},
            # Note: the write happens after; content will be filled by caller if needed,
            # but for demo we write a placeholder that the runner can improve.
            # For simplicity we write a fixed message; real chaining is in the example.
            {"tool": "write_file", "arguments": {"path": fname, "content": f"Computed: {expr}\n(result available in trace)\n"}},
        ]

    if intent == "math":
        expr = "sqrt(144) + 10"
        lower = prompt.lower()
        cleaned = re.sub(
            r"^(compute|calculate|calc|somme|sum of|what is|what's|evaluate|math|please|calculate the)\s+",
            "",
            prompt,
            flags=re.I,
        ).strip()
        cleaned = re.sub(r"\s*\?+\s*$", "", cleaned)
        m = re.search(r"([0-9.+*/()^sqrt\s\-]+|\*\*)", cleaned, re.I)
        candidate = (m.group(1).strip() if m else cleaned).strip()
        if "**" in candidate:
            candidate = candidate.replace("**", "^")
        if any(ch.isdigit() for ch in candidate) and any(op in candidate for op in "+-*/()^"):
            expr = candidate
        elif "sqrt" in lower and any(ch.isdigit() for ch in lower):
            expr = re.sub(r".*?(sqrt\s*\([^)]+\)[^a-zA-Z0-9]*)", r"\1", lower)
            expr = expr or "sqrt(144) + 10"
        elif any(ch.isdigit() for ch in prompt):
            expr = cleaned or prompt
        return [{"tool": "calculator", "arguments": {"expression": expr}}]

    if intent == "datetime":
        return [{"tool": "get_datetime", "arguments": {}}]
    if intent == "system":
        return [{"tool": "get_system_info", "arguments": {}}]
    if intent == "search":
        query = prompt.strip() or "local AI agents"
        return [{"tool": "web_search", "arguments": {"query": query, "max_results": 3}}]
    if intent == "mcp":
        return [{"tool": "mcp_echo", "arguments": {"name": "ping", "arguments": {"text": prompt}}}]
    if intent == "read":
        # simple read of common name or first mentioned
        path = "mvp_note.txt"
        m = re.search(r"([a-zA-Z0-9_.-]+\.(?:txt|md|py))", text)
        if m:
            path = m.group(1)
        return [{"tool": "read_file", "arguments": {"path": path}}]
    # files: write a note then list the workspace
    note = prompt.strip()[:200] or "local agent note"
    return [
        {
            "tool": "write_file",
            "arguments": {"path": "mvp_note.txt", "content": note + "\n"},
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
    """Route a prompt and execute the plan inside `workspace`.

    For compound math+save, the second step uses the actual calculator result.
    """
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
        calc_result = None
        for i, step in enumerate(steps):
            name = step["tool"]
            args = dict(step.get("arguments") or {})
            # Special: if this is a write after calculator in compound, inject result
            if name == "write_file" and calc_result is not None and "result available" in str(args.get("content", "")):
                args["content"] = f"Computed result: {calc_result}\nExpression was evaluated offline.\n"
            output = execute_tool(name, args, registry)
            trace.append({"tool": name, "arguments": args, "output": output})
            if name == "calculator":
                calc_result = output
    finally:
        os.chdir(cwd)
    answer = trace[-1]["output"] if trace else ""
    return {
        "intent": intent,
        "provider_table": list(PROVIDERS),
        "steps": trace,
        "trace": trace,
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
