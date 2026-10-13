#!/usr/bin/env python3
"""Core MVP agent — offline-first routing + tools demo.

Shows the real core: intent routing, file ops, calculator, system info,
web search fixture, and MCP echo. Works with zero models installed.

Usage:
  python examples/core_mvp_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"🚀 grok-local-agent-kit Core MVP (v{__version__})")
    print("Offline-first agent core: routing + tools + multi-LLM probes\n")

    workspace = Path(".grok/core-mvp")
    workspace.mkdir(parents=True, exist_ok=True)

    probes = probe_providers()
    print("Multi-LLM providers:")
    for name, info in probes.items():
        status = info.get("status", "unknown")
        print(f"  • {name}: {status}")
    print()

    scenarios = [
        ("files", "write a welcome note for the local agent"),
        ("math", "compute 15 * 3 + sqrt(81)"),
        ("system", "what is the python version and os"),
        ("search", "search local AI agents ollama mcp"),
        ("mcp", "ping the mcp echo server"),
    ]

    for intent, goal in scenarios:
        print(f"--- {intent.upper()} ---")
        print(f"Goal: {goal}")
        result = run_mvp(goal, workspace)
        print(f"Intent detected: {result.get('intent')}")
        for step in result.get("trace", []):
            tool = step["tool"]
            out = str(step.get("output", ""))[:200]
            print(f"  → {tool}: {out}")
        print()

    print("✅ Core MVP finished. No cloud, no API keys required.")
    print(f"Workspace: {workspace.resolve()}")


if __name__ == "__main__":
    main()
