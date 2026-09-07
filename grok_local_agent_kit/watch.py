"""Polling workspace watcher — trigger an agent when files change.

Stdlib only. No inotify dependency so it works on Linux/macOS/Windows.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable, Iterable, List, Optional, Sequence, Set


DEFAULT_IGNORE = {
    ".git",
    ".grok",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".pytest_cache",
    ".ruff_cache",
}


@dataclass
class FileEvent:
    path: str
    kind: str  # created | modified | deleted
    mtime: float = 0.0
    size: int = 0


@dataclass
class WatchSnapshot:
    files: dict = field(default_factory=dict)  # path -> (mtime, size)


def _should_ignore(path: Path, ignore: Set[str]) -> bool:
    return any(part in ignore for part in path.parts)


def snapshot(
    root: str | Path = ".",
    patterns: Sequence[str] = ("*",),
    ignore: Optional[Set[str]] = None,
) -> WatchSnapshot:
    root_p = Path(root).resolve()
    ignore = ignore or set(DEFAULT_IGNORE)
    files: dict = {}
    for pattern in patterns:
        for p in root_p.rglob(pattern):
            if not p.is_file():
                continue
            try:
                rel = p.relative_to(root_p)
            except ValueError:
                continue
            if _should_ignore(rel, ignore):
                continue
            try:
                st = p.stat()
            except OSError:
                continue
            files[str(rel)] = (st.st_mtime, st.st_size)
    return WatchSnapshot(files=files)


def diff(old: WatchSnapshot, new: WatchSnapshot) -> List[FileEvent]:
    events: List[FileEvent] = []
    old_keys = set(old.files)
    new_keys = set(new.files)
    for path in sorted(new_keys - old_keys):
        mtime, size = new.files[path]
        events.append(FileEvent(path=path, kind="created", mtime=mtime, size=size))
    for path in sorted(old_keys - new_keys):
        events.append(FileEvent(path=path, kind="deleted"))
    for path in sorted(old_keys & new_keys):
        if old.files[path] != new.files[path]:
            mtime, size = new.files[path]
            events.append(FileEvent(path=path, kind="modified", mtime=mtime, size=size))
    return events


def format_events(events: Iterable[FileEvent]) -> str:
    lines = [f"{e.kind:9} {e.path}" for e in events]
    return "\n".join(lines) if lines else "(no changes)"


def watch(
    root: str | Path = ".",
    patterns: Sequence[str] = ("*",),
    interval: float = 1.0,
    ignore: Optional[Set[str]] = None,
    on_events: Optional[Callable[[List[FileEvent]], None]] = None,
    stop_after: Optional[int] = None,
    max_seconds: Optional[float] = None,
    once: bool = False,
) -> List[FileEvent]:
    """Poll `root` until events fire (once=True) or until limits.

    Returns the last batch of events (empty if timed out with no changes).
    """
    current = snapshot(root, patterns, ignore)
    started = time.monotonic()
    loops = 0
    last: List[FileEvent] = []
    while True:
        time.sleep(max(0.05, interval))
        loops += 1
        nxt = snapshot(root, patterns, ignore)
        events = diff(current, nxt)
        current = nxt
        if events:
            last = events
            if on_events:
                on_events(events)
            if once:
                return events
        if stop_after is not None and loops >= stop_after:
            return last
        if max_seconds is not None and (time.monotonic() - started) >= max_seconds:
            return last
