"""v0.18 tests — cancellation + process kill, no live LLM."""

from __future__ import annotations

import time

from grok_local_agent_kit.cancel import (
    CancelToken,
    ProcessRegistry,
    cancel_all,
    get_token,
    set_token,
)
import grok_local_agent_kit  # noqa: F401 — patches tools.run_shell
from grok_local_agent_kit.tools import calculator, run_shell


def test_calculator_regression():
    assert calculator("3*7") == "21"


def test_cancel_token_roundtrip():
    token = CancelToken()
    assert token.cancelled is False
    token.cancel("stop")
    assert token.cancelled is True
    assert token.reason == "stop"
    token.reset()
    assert token.cancelled is False


def test_run_shell_respects_cancel():
    prev = get_token()
    token = CancelToken()
    set_token(token)
    try:
        token.cancel("unit-test")
        out = run_shell("echo should-not-run")
        assert "cancelled" in out.lower() or "skipped" in out.lower()
    finally:
        token.reset()
        set_token(prev)


def test_run_shell_kills_sleep():
    prev = get_token()
    token = CancelToken()
    set_token(token)
    try:
        started = time.monotonic()
        token.reset()

        import threading

        def boom():
            time.sleep(0.2)
            token.cancel("kill-sleep")

        threading.Thread(target=boom, daemon=True).start()
        out = run_shell("sleep 8", timeout=5)
        elapsed = time.monotonic() - started
        assert elapsed < 4.5, elapsed
        assert "cancel" in out.lower() or "timed out" in out.lower() or "killed" in out.lower()
    finally:
        token.reset()
        set_token(prev)


def test_process_registry_empty_kill():
    reg = ProcessRegistry()
    assert reg.kill_all() == 0


def test_cancel_all_sets_flag():
    prev = get_token()
    token = CancelToken()
    set_token(token)
    try:
        n = cancel_all("batch")
        assert token.cancelled is True
        assert n >= 0
    finally:
        token.reset()
        set_token(prev)
