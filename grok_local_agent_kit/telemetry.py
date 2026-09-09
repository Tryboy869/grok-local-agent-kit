"""Lightweight tool-call telemetry (v0.21). Offline, no network."""

from __future__ import annotations

import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class ToolEvent:
    name: str
    ms: float
    cached: bool
    ok: bool
    ts: float = field(default_factory=time.time)


@dataclass
class Telemetry:
    enabled: bool = True
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)
    events: List[ToolEvent] = field(default_factory=list)

    def record(self, name: str, ms: float, cached: bool = False, ok: bool = True) -> ToolEvent:
        ev = ToolEvent(name=name, ms=ms, cached=cached, ok=ok)
        if not self.enabled:
            return ev
        with self._lock:
            self.events.append(ev)
        return ev

    def summary(self) -> Dict[str, Any]:
        with self._lock:
            by: Dict[str, List[ToolEvent]] = defaultdict(list)
            for ev in self.events:
                by[ev.name].append(ev)
            tools = {}
            for name, evs in by.items():
                tools[name] = {
                    "calls": len(evs),
                    "cached": sum(1 for e in evs if e.cached),
                    "avg_ms": round(sum(e.ms for e in evs) / len(evs), 2),
                    "errors": sum(1 for e in evs if not e.ok),
                }
            return {
                "calls": len(self.events),
                "tools": tools,
            }

    def clear(self) -> int:
        with self._lock:
            n = len(self.events)
            self.events.clear()
            return n


_TEL = Telemetry()


def get_telemetry() -> Telemetry:
    return _TEL


def reset_telemetry() -> Telemetry:
    global _TEL
    _TEL = Telemetry()
    return _TEL


def timed_execute(
    name: str,
    arguments: Dict[str, Any],
    runner: Callable[[str, Dict[str, Any]], str],
    telemetry: Optional[Telemetry] = None,
    cached: bool = False,
) -> str:
    tel = telemetry or get_telemetry()
    t0 = time.perf_counter()
    ok = True
    try:
        return runner(name, arguments)
    except Exception:
        ok = False
        raise
    finally:
        tel.record(name, (time.perf_counter() - t0) * 1000.0, cached=cached, ok=ok)
