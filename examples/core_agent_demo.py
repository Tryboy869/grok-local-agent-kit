#!/usr/bin/env python3
"""Core agent demo: routing + real tools (web search, file ops, MCP) + multi-LLM probes.

Ready-to-run offline. Shows the functional MVP path.

Usage:
  python examples/core_agent_demo.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"🚀 grok-local-agent-kit Core Agent Demo (v{__version__})")
    print("Routing + tools (files, math, system, web_search, MCP) + multi-LLM health\n")

    workspace = Path(".grok/core-agent-demo")
    workspace.mkdir(parents=True, exist_ok=True)

    print("=== Multi-LLM provider probes ===")
    for name, info in probe_providers().items():
        print(f"  {name}: {info['status']} ({info.get('detail', '')})")
    print()

    goals = [
        "write a note: MVP core agent is functional",
        "calculate 100 / 4 + sqrt(16)",
        "get system info",
        "search for local AI agent toolkits",
        "ping mcp echo with hello from core demo",
    ]

    for goal in goals:
        print(f"Goal: {goal}")
        result = run_mvp(goal, workspace, search=lambda q: f"[fixture] results for {q}")
        print(f"  Intent: {result['intent']} | OK: {result['ok']}")
        print(f"  Answer: {str(result['answer']).splitlines()[0][:150]}")
        print()

    print("✅ Core agent demo complete. Offline-first, no API keys.")
    print(f"Artifacts in: {workspace.resolve()}")


if __name__ == "__main__":
    main()
