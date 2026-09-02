"""Restricted execute_python sandbox used by the default toolkit."""

from __future__ import annotations

import ast
import contextlib
import io
import signal
from typing import Any, Dict


def execute_python(code: str, timeout: float = 3.0) -> str:
    """Run a short snippet in a restricted exec environment."""
    if not isinstance(code, str) or not code.strip():
        return "execute_python error: empty code"
    if len(code) > 8000:
        return "execute_python error: snippet too large (max 8000 chars)"

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return f"Syntax error: {e}"

    allowed_imports = {
        "math", "json", "re", "datetime", "collections", "itertools",
        "functools", "statistics", "decimal", "fractions", "string",
        "textwrap", "unicodedata",
    }
    blocked_names = {
        "eval", "exec", "compile", "open", "__import__", "input",
        "breakpoint", "exit", "quit", "getattr", "setattr", "delattr",
        "globals", "locals", "vars", "memoryview", "help",
    }
    blocked_attrs = {
        "system", "popen", "remove", "rmdir", "unlink", "replace",
        "chmod", "chown", "kill", "execl", "execv", "spawn",
        "walk", "__subclasses__", "tb_frame", "f_globals", "f_locals",
    }

    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            names = []
            if isinstance(node, ast.Import):
                names = [a.name.split(".")[0] for a in node.names]
            else:
                names = [node.module.split(".")[0]] if node.module else []
            for n in names:
                if n not in allowed_imports:
                    return f"Blocked import of '{n}'. Allowed: {sorted(allowed_imports)}"
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name) and node.func.id in blocked_names:
                return f"Blocked call to {node.func.id}"
            if isinstance(node.func, ast.Attribute) and node.func.attr in blocked_attrs:
                return f"Blocked attribute call .{node.func.attr}"
        if isinstance(node, ast.Attribute) and str(node.attr).startswith("__"):
            return f"Blocked dunder attribute .{node.attr}"
        if isinstance(node, ast.Name) and node.id in {"__builtins__", "__loader__", "__spec__"}:
            return f"Blocked name {node.id}"

    def _safe_import(name, globals=None, locals=None, fromlist=(), level=0):
        root = name.split(".")[0]
        if root not in allowed_imports:
            raise ImportError(f"Blocked import of {name!r}")
        return __import__(name, globals, locals, fromlist, level)

    safe_builtins = {
        "__import__": _safe_import,
        "print": print, "len": len, "range": range, "str": str, "int": int,
        "float": float, "list": list, "dict": dict, "set": set, "tuple": tuple,
        "bool": bool, "bytes": bytes, "abs": abs, "min": min, "max": max,
        "sum": sum, "sorted": sorted, "enumerate": enumerate, "zip": zip,
        "map": map, "filter": filter, "round": round, "repr": repr,
        "isinstance": isinstance, "issubclass": issubclass, "type": type,
        "any": any, "all": all, "pow": pow, "divmod": divmod, "chr": chr,
        "ord": ord, "hex": hex, "bin": bin, "oct": oct, "slice": slice,
        "True": True, "False": False, "None": None,
    }
    buf = io.StringIO()
    local_ns: Dict[str, Any] = {}

    def _timeout_handler(signum, frame):
        raise TimeoutError(f"execute_python timed out after {timeout}s")

    alarm_set = False
    try:
        if hasattr(signal, "SIGALRM") and timeout and timeout > 0:
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.setitimer(signal.ITIMER_REAL, float(timeout))
            alarm_set = True
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(compile(tree, "<agent>", "exec"), {"__builtins__": safe_builtins}, local_ns)
        out = buf.getvalue()
        return out if out else "(executed, no stdout)"
    except TimeoutError as e:
        return str(e)
    except Exception as e:
        return f"execute_python error: {type(e).__name__}: {e}"
    finally:
        if alarm_set:
            signal.setitimer(signal.ITIMER_REAL, 0)
