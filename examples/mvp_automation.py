#!/usr/bin/env python3
"""Offline automation MVP — file note, math, search, system info.

No Ollama required. Swap in a live model later via `grok-agent chat --router`.

Usage:
  python examples/mvp_automation.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit.mvp import run_mvp


def main() -> None:
    workspace = Path(".grok/mvp-automation")
    goals = [
        "write a note that automation finished the checklist",
        "compute sqrt(144) + 10",
        "what is the python version",
        "search local AI agents 2026",
    ]
    print("Automation MVP (offline tool plan)\n")
    for goal in goals:
        result = run_mvp(goal, workspace, search=lambda q: f"1. {q}\n2. ollama\n3. mcp")
        print(f"- {goal}")
        print(f"  intent={result['intent']} ok={result['ok']}")
        print(f"  {result['answer'].splitlines()[0][:160]}")
    print(f"\nnote: {(workspace / 'mvp_note.txt').resolve()}")


if __name__ == "__main__":
    main()
