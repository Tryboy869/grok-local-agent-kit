"""Simple retry helper for flaky local LLM / HTTP calls."""

from __future__ import annotations

import time
from typing import Callable, Optional, TypeVar

T = TypeVar("T")


def retry_call(
    fn: Callable[[], T],
    *,
    attempts: int = 3,
    base_delay: float = 0.05,
    retry_on: tuple = (Exception,),
    sleep: Optional[Callable[[float], None]] = None,
) -> T:
    """Run fn up to `attempts` times with exponential backoff."""
    sleeper = sleep or time.sleep
    last: Optional[BaseException] = None
    tries = max(1, attempts)
    for i in range(tries):
        try:
            return fn()
        except retry_on as exc:  # type: ignore[misc]
            last = exc
            if i >= tries - 1:
                raise
            sleeper(base_delay * (2**i))
    assert last is not None
    raise last
