"""Tool allow/deny lists and per-tool wall-clock timeouts."""

from __future__ import annotations

import os
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeout
from typing import Callable, Iterable, Optional, Set


DEFAULT_TIMEOUT_S = 30.0
DANGEROUS_DEFAULT = {"run_shell", "delete_file", "execute_python"}


def _split_names(raw: str) -> Set[str]:
    return {part.strip() for part in raw.split(",") if part.strip()}


class ToolGuard:
    """Allow/deny + timeout wrapper around the tool registry."""

    def __init__(
        self,
        allow: Optional[Iterable[str]] = None,
        deny: Optional[Iterable[str]] = None,
        timeout_s: float = DEFAULT_TIMEOUT_S,
    ) -> None:
        env_allow = os.environ.get("GROK_AGENT_ALLOW_TOOLS", "")
        env_deny = os.environ.get("GROK_AGENT_DENY_TOOLS", "")
        env_timeout = os.environ.get("GROK_AGENT_TOOL_TIMEOUT", "")
        self.allow: Optional[Set[str]] = set(allow) if allow is not None else (
            _split_names(env_allow) or None
        )
        self.deny: Set[str] = set(deny) if deny is not None else _split_names(env_deny)
        try:
            self.timeout_s = float(timeout_s if not env_timeout else env_timeout)
        except ValueError:
            self.timeout_s = DEFAULT_TIMEOUT_S

    def check(self, name: str) -> Optional[str]:
        if self.allow is not None and name not in self.allow:
            return f"Blocked by allow-list: '{name}' is not permitted."
        if name in self.deny:
            return f"Blocked by deny-list: '{name}'."
        return None

    def run(self, name: str, fn: Callable[..., str], kwargs: dict) -> str:
        blocked = self.check(name)
        if blocked:
            return blocked
        timeout = self.timeout_s
        if timeout <= 0:
            return fn(**kwargs)
        with ThreadPoolExecutor(max_workers=1) as pool:
            fut = pool.submit(fn, **kwargs)
            try:
                return fut.result(timeout=timeout)
            except FuturesTimeout:
                return f"Tool '{name}' timed out after {timeout}s."
            except Exception as e:
                return f"Tool '{name}' error: {type(e).__name__}: {e}"


_guard = ToolGuard()
_lock = threading.Lock()


def get_guard() -> ToolGuard:
    return _guard


def set_guard(guard: ToolGuard) -> ToolGuard:
    global _guard
    with _lock:
        _guard = guard
    return _guard
