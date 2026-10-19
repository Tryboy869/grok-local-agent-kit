#!/usr/bin/env python3
"""Ready-to-run chat-style agent demo (offline-first).

Uses the core MVP router + tools. No live LLM required.
Shows multi-turn style goals with probes.

Usage:
  python examples/ready_chat_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"💬 grok-local-agent-kit Ready Chat Agent (v{__version__})")
    print("Offline chat-style loop with routing + tools + multi-LLM probes\n")

    workspace = Path(".grok/ready-chat")
    workspace.mkdir(parents=True, exist_ok=True)

    print("=== Provider health ===")
    for name, info in probe_providers().items():
        print(f"  {name}: {info['status']}")
    print()

    turns = [
        "write a note: ready chat agent started",
        "calculate 42 * 2 + 8",
        "search for local AI agents",
        "get system info",
        "echo mcp hello from ready chat",
    ]

    for i, goal in enumerate(turns, 1):
        print(f"Turn {i}: {goal}")
        result = run_mvp(goal, workspace, search=lambda q: f"[offline fixture] {q}")
        print(f"  → intent={result['intent']} ok={result['ok']}")
        ans = str(result.get('answer', ''))[:120].replace('\n', ' ')
        print(f"  → {ans}")
        print()

    print("✅ Ready chat demo complete. Fully offline.")
    print(f"Workspace: {workspace.resolve()}")


if __name__ == "__main__":
    main()
