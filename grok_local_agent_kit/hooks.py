"""Lightweight event hooks for the ReAct loop."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

HookFn = Callable[..., None]


@dataclass
class HookBus:
    """Named callbacks fired by Agent._run_loop."""

    listeners: Dict[str, List[HookFn]] = field(default_factory=dict)

    def on(self, event: str, fn: HookFn) -> HookFn:
        self.listeners.setdefault(event, []).append(fn)
        return fn

    def off(self, event: str, fn: HookFn) -> None:
        if event in self.listeners:
            self.listeners[event] = [f for f in self.listeners[event] if f is not fn]

    def emit(self, event: str, **payload: Any) -> None:
        for fn in list(self.listeners.get(event, [])):
            try:
                fn(**payload)
            except TypeError:
                fn(payload)
            except Exception:
                pass


EVENTS = (
    "on_start",
    "on_iteration",
    "before_llm",
    "after_llm",
    "before_tool",
    "after_tool",
    "on_final",
    "on_error",
)


def default_verbose_hooks(print_fn: Optional[Callable[[str], None]] = None) -> HookBus:
    """Pretty-print tool traffic without depending on Agent.verbose internals."""
    out = print_fn or print
    bus = HookBus()

    def _before_tool(*, name: str, args: Dict[str, Any], **_: Any) -> None:
        out(f"  → hook before_tool: {name}({args})")

    def _after_tool(*, name: str, result: str, **_: Any) -> None:
        preview = result[:200] + ("..." if len(result) > 200 else "")
        out(f"  ← hook after_tool: {name} → {preview}")

    def _on_final(*, text: str, **_: Any) -> None:
        out(f"  ✓ hook on_final ({len(text)} chars)")

    bus.on("before_tool", _before_tool)
    bus.on("after_tool", _after_tool)
    bus.on("on_final", _on_final)
    return bus
