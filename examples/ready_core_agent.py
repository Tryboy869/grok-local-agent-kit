#!/usr/bin/env python3
"""Ready core agent demo (v0.59+).

Clean offline entry point: improved intent routing + real tools
(calculator with better expr extraction, datetime, files, search fixture,
system info, MCP echo) + multi-LLM health probes.

No Ollama, LM Studio, or network required.

Usage:
  python examples/ready_core_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"🚀 grok-local-agent-kit Ready Core Agent (v{__version__})")
    print("Improved routing + real local tools + multi-LLM probes (fully offline)\n")

    workspace = Path(".grok/ready-core")
    workspace.mkdir(parents=True, exist_ok=True)

    print("=== Multi-LLM provider health ===")
    for name, info in probe_providers().items():
        status = info.get("status", "?")
        detail = info.get("detail", "")
        print(f"  {name:10} {status:6} {detail}")
    print()

    goals = [
        "what time is it?",
        "calculate 15 * 4 + sqrt(81) - 3",
        "write a note: ready core agent v0.59 is live",
        "search for offline AI agent toolkits",
        "get system info",
        "mcp echo ready core ping",
    ]

    for i, goal in enumerate(goals, 1):
        print(f"[{i}] {goal}")
        result = run_mvp(goal, workspace, search=lambda q: f"[fixture] results for: {q}")
        intent = result.get("intent", "?")
        ok = result.get("ok", False)
        ans = str(result.get("answer", "")).replace("\n", " ")[:140]
        print(f"    intent={intent} ok={ok}")
        print(f"    → {ans}")
        print()

    print("✅ Ready core demo complete.")
    print(f"Workspace: {workspace.resolve()}")
    print("Try the full ReAct loop with a local model: grok-agent chat")


if __name__ == "__main__":
    main()
