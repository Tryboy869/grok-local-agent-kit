"""Tiny interval scheduler for local automation agents."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class Job:
    name: str
    interval_s: float
    fn: Callable[[], str]
    last_run: float = 0.0
    last_result: str = ""
    runs: int = 0


@dataclass
class Scheduler:
    jobs: Dict[str, Job] = field(default_factory=dict)
    _stop: threading.Event = field(default_factory=threading.Event)

    def add(self, name: str, interval_s: float, fn: Callable[[], str]) -> None:
        self.jobs[name] = Job(name=name, interval_s=max(0.01, float(interval_s)), fn=fn)

    def run_once(self, now: Optional[float] = None) -> List[str]:
        now = time.time() if now is None else now
        fired: List[str] = []
        for job in self.jobs.values():
            if now - job.last_run >= job.interval_s:
                try:
                    job.last_result = job.fn() or ""
                except Exception as e:
                    job.last_result = f"job error: {e}"
                job.last_run = now
                job.runs += 1
                fired.append(job.name)
        return fired

    def describe(self) -> str:
        if not self.jobs:
            return "No jobs."
        lines = []
        for j in self.jobs.values():
            preview = (j.last_result or "")[:80]
            lines.append(f"- {j.name} every {j.interval_s}s runs={j.runs} last={preview!r}")
        return "Jobs:\n" + "\n".join(lines)

    def loop(self, ticks: int = 0, sleep_s: float = 0.25) -> None:
        n = 0
        while not self._stop.is_set():
            self.run_once()
            n += 1
            if ticks and n >= ticks:
                break
            time.sleep(sleep_s)

    def stop(self) -> None:
        self._stop.set()
