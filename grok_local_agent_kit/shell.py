"""Process-group-aware run_shell used by v0.18 cancellation."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .cancel import get_registry, get_token


def run_shell(command: str, timeout: int = 30) -> str:
    blocked = [
        "rm -rf",
        "rm -r",
        "mkfs",
        "dd if=",
        ":(){",
        "shutdown",
        "reboot",
        "passwd",
        "chmod 777",
        "chown",
        "> /dev/",
        "curl | sh",
        "wget | sh",
        "| bash",
        "| sh",
    ]
    lower = command.lower()
    for b in blocked:
        if b in lower:
            return f"Blocked potentially dangerous command containing '{b}'."
    token = get_token()
    if token.cancelled:
        return f"run_shell skipped: {token.reason}"
    try:
        proc = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(Path.cwd()),
            start_new_session=True,
        )
    except Exception as e:
        return f"run_shell error: {e}"
    registry = get_registry()
    registry.register(proc.pid)
    try:
        deadline = timeout if timeout and timeout > 0 else 30
        elapsed = 0.0
        step = 0.1
        while proc.poll() is None:
            if token.cancelled:
                _terminate_proc(proc)
                return f"run_shell cancelled: {token.reason}"
            if elapsed >= deadline:
                _terminate_proc(proc)
                return f"Command timed out after {deadline}s (process killed)"
            try:
                proc.wait(timeout=step)
            except subprocess.TimeoutExpired:
                elapsed += step
        stdout, stderr = proc.communicate()
        out = (stdout or "") + (stderr or "")
        if proc.returncode not in (0, None):
            out = f"[exit {proc.returncode}]\n{out}"
        return out[:8000] if out else "(no output)"
    except Exception as e:
        _terminate_proc(proc)
        return f"run_shell error: {e}"
    finally:
        registry.unregister(proc.pid)


def _terminate_proc(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    try:
        os.killpg(proc.pid, 15)
    except OSError:
        try:
            proc.terminate()
        except OSError:
            pass
    try:
        proc.wait(timeout=0.4)
    except subprocess.TimeoutExpired:
        try:
            os.killpg(proc.pid, 9)
        except OSError:
            try:
                proc.kill()
            except OSError:
                pass
        try:
            proc.wait(timeout=0.4)
        except subprocess.TimeoutExpired:
            pass


def patch_tools() -> None:
    """Point the built-in registry at the cancellable implementation."""
    from . import tools

    tools.run_shell = run_shell
    tools.TOOL_FUNCS["run_shell"] = run_shell
