"""Offline MVP agent: intent routing + local tools + multi-LLM provider table.

No Ollama, LM Studio, or network is required. `run_mvp` classifies a goal,
builds a tool plan, and executes it through the same tool registry the ReAct
loop uses. `probe_providers` reports whether local backends are up without
failing the demo when they are not.

v0.75: better multi-step chaining (search→file with result injection, improved NL plan extraction).
v0.74: compound code→file (execute_python result injected into write_file).
v0.73: added offline "code" intent that routes to sandboxed execute_python.
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
    # Code / Python execution (offline sandboxed)
    if any(k in text for k in ("python", "code", "execute code", "run code", "script", "print(", "def ", "import ")):
        return "code"
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

    Supports simple compound goals like "calculate X and save to file", "run code and save result",
    or "search X and save to note".
    """
    text = (prompt or "").lower()
    intent = route_intent(prompt)

    # Compound: math + write/save
    compound_math_save = (
        intent == "math"
        and any(k in text for k in ("save", "write", "save to", "write to", "and save", "then write", "store in"))
    )

    # Compound: code + write/save
    compound_code_save = (
        intent == "code"
        and any(k in text for k in ("save", "write", "save to", "write to", "and save", "then write", "store in", "save result", "write result"))
    )

    # Compound: search + write/save (v0.75)
    compound_search_save = (
        intent == "search"
        and any(k in text for k in ("save", "write", "save to", "write to", "and save", "then write", "store in", "note", "to file"))
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
            {"tool": "write_file", "arguments": {"path": fname, "content": f"Computed expression: {expr}\n(see calculator result in previous step)\n"}},
        ]

    if compound_code_save:
        code = "print(sum(range(1, 11)))"
        if "print(" in text or "def " in text or "import " in text:
            m = re.search(r"(print\([^)]+\)|def\s+\w+|import\s+\w+)", prompt)
            if m:
                code = m.group(1)
            else:
                code = prompt.strip()[:200]
        fname = "code_result.txt"
        fm = re.search(r"(?:to|in|as)\s+([a-zA-Z0-9_.-]+\.(?:txt|md|py))", text)
        if fm:
            fname = fm.group(1)
        return [
            {"tool": "execute_python", "arguments": {"code": code, "timeout": 5}},
            {"tool": "write_file", "arguments": {"path": fname, "content": "(code result will be injected)\n"}},
        ]

    if compound_search_save:
        query = prompt.strip() or "local AI agents"
        # strip save instructions from query roughly
        query = re.sub(r"\s*(and|then)?\s*(save|write|store).*$ ", "", query, flags=re.I).strip() or query
        fname = "search_note.txt"
        fm = re.search(r"(?:to|in|as)\s+([a-zA-Z0-9_.-]+\.(?:txt|md))", text)
        if fm:
            fname = fm.group(1)
        return [
            {"tool": "web_search", "arguments": {"query": query, "max_results": 3}},
            {"tool": "write_file", "arguments": {"path": fname, "content": "(search results will be injected)\n"}},
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

    if intent == "code":
        # Extract or generate a simple safe Python snippet
        code = "print(2**10 + 42)"
        if "print(" in text or "def " in text or "import " in text:
            # Try to pull a snippet if present
            m = re.search(r"(print\([^)]+\)|def\s+\w+|import\s+\w+)", prompt)
            if m:
                code = m.group(1)
            else:
                code = prompt.strip()[:200]
        return [{"tool": "execute_python", "arguments": {"code": code, "timeout": 5}}]

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


def run_mvp(
    prompt: str,
    workspace: Path,
    *,
    search: Optional[SearchFn] = None,
    registry: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Execute a deterministic offline plan and return a structured result."""
    workspace = Path(workspace)
    workspace.mkdir(parents=True, exist_ok=True)
    cwd = Path.cwd()
    try:
        import os

        os.chdir(workspace)
        registry = registry or get_default_tools()
        intent = route_intent(prompt)
        steps = plan_for(prompt)
        trace = []
        last_result = None
        for step in steps:
            name = step["tool"]
            args = dict(step.get("arguments") or {})
            # Inject previous tool result into write_file when placeholder present
            if name == "write_file" and last_result is not None:
                content = str(args.get("content", ""))
                if any(ph in content for ph in ("(code result will be injected)", "see calculator result", "result available", "(search results will be injected)")):
                    args["content"] = f"Result from previous step:\n{last_result}\n\n---\nGenerated offline by grok-local-agent-kit MVP.\n"
            output = execute_tool(name, args, registry)
            trace.append({"tool": name, "arguments": args, "output": output})
            last_result = output
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
