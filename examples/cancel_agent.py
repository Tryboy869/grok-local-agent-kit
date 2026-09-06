#!/usr/bin/env python3
"""Demonstrate cancellation that kills a hung shell child (no LLM required)."""

from __future__ import annotations

import threading
import time

from grok_local_agent_kit.cancel import CancelToken, get_token, set_token
from grok_local_agent_kit.tools import run_shell


def main() -> None:
    prev = get_token()
    token = CancelToken()
    set_token(token)
    try:
        print("Starting sleep 10; cancelling after 0.3s...")

        def stop() -> None:
            time.sleep(0.3)
            token.cancel("demo")

        threading.Thread(target=stop, daemon=True).start()
        t0 = time.monotonic()
        print(run_shell("sleep 10", timeout=8))
        print(f"elapsed={time.monotonic() - t0:.2f}s")
    finally:
        token.reset()
        set_token(prev)


if __name__ == "__main__":
    main()
