"""Per-tool and global call budgets so agents cannot loop forever."""

from __future__ import annotations

import os
import threading
from collections import defaultdict
from typing import Dict, Optional


class BudgetExceeded(RuntimeError):
    pass


class ToolBudget:
    def __init__(
        self,
        max_calls: int = 50,
        per_tool: Optional[Dict[str, int]] = None,
        enabled: bool = True,
    ) -> None:
        env_max = os.environ.get("GROK_AGENT_MAX_TOOL_CALLS", "")
        if env_max.strip().isdigit():
            max_calls = int(env_max)
        self.max_calls = max(0, max_calls)
        self.per_tool = dict(per_tool or {})
        self.enabled = enabled
        self._counts: Dict[str, int] = defaultdict(int)
        self._total = 0
        self._lock = threading.Lock()

    def check(self, name: str) -> Optional[str]:
        if not self.enabled:
            return None
        with self._lock:
            if self.max_calls and self._total >= self.max_calls:
                return f"Budget exceeded: global tool-call cap {self.max_calls} reached."
            cap = self.per_tool.get(name)
            if cap is not None and self._counts[name] >= cap:
                return f"Budget exceeded: tool '{name}' capped at {cap} calls."
        return None

    def consume(self, name: str) -> Optional[str]:
        blocked = self.check(name)
        if blocked:
            return blocked
        if not self.enabled:
            return None
        with self._lock:
            self._counts[name] += 1
            self._total += 1
        return None

    def reset(self) -> None:
        with self._lock:
            self._counts.clear()
            self._total = 0

    def stats(self) -> dict:
        with self._lock:
            return {
                "enabled": self.enabled,
                "max_calls": self.max_calls,
                "total": self._total,
                "per_tool": dict(self._counts),
                "caps": dict(self.per_tool),
            }


_budget = ToolBudget()
_lock = threading.Lock()


def get_budget() -> ToolBudget:
    return _budget


def set_budget(budget: ToolBudget) -> ToolBudget:
    global _budget
    with _lock:
        _budget = budget
    return _budget


def reset_budget() -> ToolBudget:
    get_budget().reset()
    return get_budget()
