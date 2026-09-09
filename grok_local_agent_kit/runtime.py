"""Wrap execute_tool with cache + telemetry (v0.21)."""

from __future__ import annotations

from typing import Any, Callable, Dict

from .cache import get_cache
from .telemetry import get_telemetry


def wrap_execute(original: Callable[..., str]) -> Callable[..., str]:
    def execute_tool(name: str, arguments: Dict[str, Any], registry: Dict[str, Callable[..., str]]) -> str:
        cache = get_cache()
        tel = get_telemetry()
        hit = cache.get(name, arguments)
        if hit is not None:
            tel.record(name, 0.0, cached=True, ok=True)
            return hit

        import time

        t0 = time.perf_counter()
        ok = True
        try:
            value = original(name, arguments, registry)
            cache.put(name, arguments, value)
            return value
        except Exception:
            ok = False
            raise
        finally:
            tel.record(name, (time.perf_counter() - t0) * 1000.0, cached=False, ok=ok)

    return execute_tool


def patch() -> None:
    from . import tools

    if getattr(tools.execute_tool, "_grok_v021", False):
        return
    wrapped = wrap_execute(tools.execute_tool)
    wrapped._grok_v021 = True  # type: ignore[attr-defined]
    tools.execute_tool = wrapped
