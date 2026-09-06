"""Cancellation tokens that can actually kill hung subprocesses."""

from __future__ import annotations

import os
import signal
import threading
import time
from typing import Iterable, Optional, Set


class CancelledError(RuntimeError):
    """Raised or returned when a token is cancelled."""


class CancelToken:
    """Thread-safe cancellation flag shared by the agent loop and tools."""

    def __init__(self) -> None:
        self._event = threading.Event()
        self._reason = ""

    def cancel(self, reason: str = "cancelled") -> None:
        self._reason = reason or "cancelled"
        self._event.set()

    def reset(self) -> None:
        self._reason = ""
        self._event.clear()

    @property
    def cancelled(self) -> bool:
        return self._event.is_set()

    @property
    def reason(self) -> str:
        return self._reason or "cancelled"

    def wait(self, timeout: float) -> bool:
        return self._event.wait(timeout)

    def raise_if_cancelled(self) -> None:
        if self.cancelled:
            raise CancelledError(self.reason)


class ProcessRegistry:
    """Track child PIDs started by run_shell so timeouts can SIGKILL them."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pids: Set[int] = set()

    def register(self, pid: int) -> None:
        with self._lock:
            self._pids.add(pid)

    def unregister(self, pid: int) -> None:
        with self._lock:
            self._pids.discard(pid)

    def pids(self) -> Set[int]:
        with self._lock:
            return set(self._pids)

    def kill_all(self, sig: int = signal.SIGTERM) -> int:
        killed = 0
        for pid in self.pids():
            if _kill_tree(pid, sig):
                killed += 1
            self.unregister(pid)
        return killed


def _kill_tree(pid: int, sig: int) -> bool:
    if pid <= 0:
        return False
    try:
        try:
            os.killpg(pid, sig)
        except (ProcessLookupError, PermissionError, OSError):
            os.kill(pid, sig)
        return True
    except ProcessLookupError:
        return False
    except OSError:
        try:
            os.kill(pid, signal.SIGKILL)
            return True
        except OSError:
            return False


_token = CancelToken()
_procs = ProcessRegistry()
_lock = threading.Lock()


def get_token() -> CancelToken:
    return _token


def set_token(token: CancelToken) -> CancelToken:
    global _token
    with _lock:
        _token = token
    return _token


def get_registry() -> ProcessRegistry:
    return _procs


def cancel_all(reason: str = "cancelled") -> int:
    get_token().cancel(reason)
    return get_registry().kill_all(signal.SIGTERM)


def wait_or_cancel(seconds: float, token: Optional[CancelToken] = None, step: float = 0.05) -> bool:
    """Sleep up to `seconds`. Return True if cancelled."""
    token = token or get_token()
    deadline = time.monotonic() + max(0.0, seconds)
    while time.monotonic() < deadline:
        if token.cancelled:
            return True
        remaining = deadline - time.monotonic()
        token.wait(min(step, remaining))
    return token.cancelled
