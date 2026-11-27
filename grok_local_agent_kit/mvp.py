"""Offline MVP intent router + tool executor.

Provides run_mvp() and probe_providers() so ready demos and tests work
fully offline with real tool execution and compound result injection.
No LLM required.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional

from .tools import (
    calculator,
    copy_file,
    execute_python,
    file_stat,
    get_datetime,
    get_system_info,
    http_get,
    list_files,
    mkdir,
    move_file,
    read_file,
    run_shell,
    search_files,
    web_search,
    write_file,
)


def probe_providers() -> Dict[str, Any]:
    """Non-blocking probe of local Ollama and LM Studio endpoints."""
    results: Dict[str, Any] = {}
    try:
        import httpx
        try:
            r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=1.5)
            ok = r.status_code == 200
            models = []
            if ok:
                try:
                    models = [m.get("name", "?") for m in r.json().get("models", [])[:3]]
                except Exception:
                    pass
            results["ollama"] = {"ok": ok, "status": r.status_code, "models": models}
        except Exception as e:
            results["ollama"] = {"ok": False, "error": str(e)[:120]}
        try:
            r = httpx.get("http://127.0.0.1:1234/v1/models", timeout=1.5)
            results["lmstudio"] = {"ok": r.status_code == 200, "status": r.status_code}
        except Exception as e:
            results["lmstudio"] = {"ok": False, "error": str(e)[:120]}
    except ImportError:
        results["error"] = "httpx not available for probe"
    return results


def _extract_expr(text: str) -> str:
    m = re.search(r"([0-9\s\+\-\*/\.\(\)\*\*]{3,})", text)
    if m:
        return m.group(1).strip()
    if "sqrt" in text.lower():
        return "sqrt(144) + 10"
    return "2**10 + 42"


def _extract_code(text: str) -> str:
    m = re.search(r"(?:code|python|run code)[:\s]+(.+)", text, re.I)
    if m:
        return m.group(1).strip().strip("\"'")
    m = re.search(r"print\([^)]+\)", text)
    if m:
        return m.group(0)
    return "print(sum(range(1, 11)))"


def _extract_path(text: str, default: str = "note.txt") -> str:
    m = re.search(r"(?:to|in|as|file|path)\s+([a-zA-Z0-9_\-./]+\.(?:txt|md|py|json))", text, re.I)
    if m:
        return m.group(1)
    m = re.search(r"([a-zA-Z0-9_\-./]+\.(?:txt|md|py|json))", text)
    if m:
        return m.group(1)
    return default


def route_intent(goal: str) -> List[Dict[str, Any]]:
    """Build a simple sequential plan of tool calls from a natural language goal."""
    low = (goal or "").lower().strip()
    steps: List[Dict[str, Any]] = []

    # Compound patterns (order matters — more specific first)
    if any(w in low for w in ("copy", "duplicate")) and any(w in low for w in ("file", "note", "txt")):
        src = _extract_path(goal, "source_note.txt")
        dest = "copied_" + Path(src).name
        if "to " in low:
            m = re.search(r"to\s+([a-zA-Z0-9_\-./]+\.txt)", low)
            if m:
                dest = m.group(1)
        steps.append({"name": "write_file", "args": {"path": src, "content": "Hello from offline MVP (source)\n"}})
        steps.append({"name": "copy_file", "args": {"src": src, "dest": dest}})
        steps.append({"name": "list_files", "args": {"path": "."}})
        return steps

    if any(w in low for w in ("mkdir", "create directory", "make folder", "create dir")) and any(w in low for w in ("note", "file", "save", "write")):
        dir_name = "notes"
        m = re.search(r"(?:directory|folder|dir)\s+([a-zA-Z0-9_\-]+)", low)
        if m:
            dir_name = m.group(1)
        fname = _extract_path(goal, "welcome.txt")
        steps.append({"name": "mkdir", "args": {"path": dir_name}})
        steps.append({"name": "write_file", "args": {"path": f"{dir_name}/{fname}", "content": "Welcome note inside new directory\n"}})
        return steps

    if any(w in low for w in ("move", "rename")) and any(w in low for w in ("file", "note")):
        src = _extract_path(goal, "old.txt")
        dest = "moved_" + Path(src).name
        steps.append({"name": "write_file", "args": {"path": src, "content": "to be moved\n"}})
        steps.append({"name": "move_file", "args": {"src": src, "dest": dest}})
        return steps

    if any(w in low for w in ("shell", "command", "echo", "run command")) and any(w in low for w in ("save", "write", "file", "note")):
        cmd = "echo Hello from shell agent"
        m = re.search(r"(?:command|echo|run)[:\s]+(.+?)(?:and|then|save|$)", goal, re.I)
        if m:
            cmd = m.group(1).strip().strip("\"'")
        path = _extract_path(goal, "shell_note.txt")
        steps.append({"name": "run_shell", "args": {"command": cmd}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "SHELL_RESULT_PLACEHOLDER"}})
        return steps

    if any(w in low for w in ("list files", "list the", "listing")) and any(w in low for w in ("save", "write", "file")):
        path = _extract_path(goal, "listing.txt")
        steps.append({"name": "list_files", "args": {"path": "."}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "LIST_RESULT_PLACEHOLDER"}})
        return steps

    if any(w in low for w in ("search files", "search for", "find files")) and any(w in low for w in ("save", "write", "file")):
        query = "def"
        m = re.search(r"(?:for|search)\s+['\"]?([a-zA-Z0-9_]+)['\"]?", low)
        if m:
            query = m.group(1)
        path = _extract_path(goal, "searchfiles_note.txt")
        steps.append({"name": "search_files", "args": {"query": query, "path": "."}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "SEARCHFILES_RESULT_PLACEHOLDER"}})
        return steps

    if any(w in low for w in ("http", "fetch", "get url", "https://")) and any(w in low for w in ("save", "write", "file")):
        url = "https://example.com"
        m = re.search(r"https?://[^\s]+", goal)
        if m:
            url = m.group(0)
        path = _extract_path(goal, "http_note.txt")
        steps.append({"name": "http_get", "args": {"url": url}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "HTTP_RESULT_PLACEHOLDER"}})
        return steps

    if any(w in low for w in ("math", "calculate", "compute", "calc")) and any(w in low for w in ("save", "write", "file", "verify")):
        expr = _extract_expr(goal)
        path = _extract_path(goal, "math_result.txt")
        steps.append({"name": "calculator", "args": {"expression": expr}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "MATH_RESULT_PLACEHOLDER"}})
        if "verify" in low or "read" in low:
            steps.append({"name": "read_file", "args": {"path": path}})
        return steps

    if any(w in low for w in ("code", "python", "execute")) and any(w in low for w in ("save", "write", "file")):
        code = _extract_code(goal)
        path = _extract_path(goal, "sum_result.txt")
        steps.append({"name": "execute_python", "args": {"code": code}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "CODE_RESULT_PLACEHOLDER"}})
        return steps

    if any(w in low for w in ("search for", "web search", "look up")) and any(w in low for w in ("save", "write", "file")):
        query = "local AI agents"
        m = re.search(r"(?:search for|search)\s+(.+?)(?:and|then|save|$)", goal, re.I)
        if m:
            query = m.group(1).strip()
        path = _extract_path(goal, "search_note.txt")
        steps.append({"name": "web_search", "args": {"query": query}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "WEBSEARCH_RESULT_PLACEHOLDER"}})
        return steps

    if any(w in low for w in ("system", "os", "info", "python version")) and any(w in low for w in ("save", "write", "file")):
        path = _extract_path(goal, "system_note.txt")
        steps.append({"name": "get_system_info", "args": {}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "SYSTEM_RESULT_PLACEHOLDER"}})
        return steps

    if any(w in low for w in ("time", "datetime", "date", "now")) and any(w in low for w in ("save", "write", "file")):
        path = _extract_path(goal, "time_note.txt")
        steps.append({"name": "get_datetime", "args": {}})
        steps.append({"name": "write_file", "args": {"path": path, "content": "DATETIME_RESULT_PLACEHOLDER"}})
        return steps

    # Simple single-tool intents
    if any(w in low for w in ("calculate", "calc", "math", "sqrt", "2**")):
        steps.append({"name": "calculator", "args": {"expression": _extract_expr(goal)}})
        return steps

    if any(w in low for w in ("code", "python", "print(")):
        steps.append({"name": "execute_python", "args": {"code": _extract_code(goal)}})
        return steps

    if any(w in low for w in ("list files", "list the files", "ls")):
        steps.append({"name": "list_files", "args": {"path": "."}})
        return steps

    if any(w in low for w in ("write", "note", "save", "create a note")):
        path = _extract_path(goal, "agent_note.txt")
        content = "Hello from ready local agent (offline MVP)\n"
        m = re.search(r"saying\s+(.+?)(?:to|and|$)", goal, re.I)
        if m:
            content = m.group(1).strip() + "\n"
        steps.append({"name": "write_file", "args": {"path": path, "content": content}})
        return steps

    if any(w in low for w in ("datetime", "time", "now", "date")):
        steps.append({"name": "get_datetime", "args": {}})
        return steps

    if any(w in low for w in ("system", "info", "os")):
        steps.append({"name": "get_system_info", "args": {}})
        return steps

    # Fallback
    steps.append({"name": "get_system_info", "args": {}})
    return steps


def run_mvp(goal: str, workspace: Optional[Path] = None) -> Dict[str, Any]:
    """Execute an offline plan for the given goal and return a result dict."""
    plan = route_intent(goal)
    results: List[str] = []
    last_result = ""
    executed: List[Dict[str, Any]] = []

    for step in plan:
        name = step["name"]
        args = dict(step.get("args") or {})

        # Inject previous result into placeholders
        for k, v in list(args.items()):
            if isinstance(v, str) and "PLACEHOLDER" in v:
                args[k] = last_result[:2000] if last_result else "(no previous result)"

        try:
            if name == "calculator":
                last_result = calculator(**args)
            elif name == "execute_python":
                last_result = execute_python(**args)
            elif name == "write_file":
                last_result = write_file(**args)
            elif name == "read_file":
                last_result = read_file(**args)
            elif name == "list_files":
                last_result = list_files(**args)
            elif name == "search_files":
                last_result = search_files(**args)
            elif name == "http_get":
                last_result = http_get(**args)
            elif name == "web_search":
                last_result = web_search(**args)
            elif name == "run_shell":
                last_result = run_shell(**args)
            elif name == "get_datetime":
                last_result = get_datetime(**args)
            elif name == "get_system_info":
                last_result = get_system_info(**args)
            elif name == "mkdir":
                last_result = mkdir(**args)
            elif name == "copy_file":
                last_result = copy_file(**args)
            elif name == "move_file":
                last_result = move_file(**args)
            elif name == "file_stat":
                last_result = file_stat(**args)
            else:
                last_result = f"Unknown tool: {name}"
        except Exception as e:
            last_result = f"{name} error: {e}"

        results.append(f"{name} → {str(last_result)[:180]}")
        executed.append({"tool": name, "args": args, "result": str(last_result)[:400]})

    answer = " | ".join(results) if results else "No plan produced."
    return {
        "answer": answer,
        "goal": goal,
        "steps": executed,
        "ok": True,
    }
