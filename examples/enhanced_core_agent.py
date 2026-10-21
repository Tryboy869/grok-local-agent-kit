#!/usr/bin/env python3
"""Enhanced core agent demo (v0.58+).

Improved offline routing, real tools (files, calculator, datetime, system,
web_search fixture, MCP echo), multi-LLM probes, and clearer output.
Fully offline — no Ollama, LM Studio, or network required.

Usage:
  python examples/enhanced_core_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"⚡ grok-local-agent-kit Enhanced Core Agent (v{__version__})")
    print("Smarter routing + real local tools + multi-LLM health probes\n")

    workspace = Path(".grok/enhanced-core")
    workspace.mkdir(parents=True, exist_ok=True)

    print("=== Multi-LLM provider probes ===")
    probes = probe_providers()
    for name, info in probes.items():
        status = info.get("status", "unknown")
        detail = info.get("detail", "")
        print(f"  {name}: {status}" + (f" — {detail}" if detail else ""))
    print()

    goals = [
        "what time is it right now?",
        "calculate 2**8 + sqrt(144) - 10",
        "write a note: enhanced core agent is ready for local AI",
        "search for offline-first AI agent toolkits",
        "get system info and python version",
        "mcp echo: hello from enhanced core agent",
    ]

    for goal in goals:
        print(f"Goal: {goal}")
        result = run_mvp(
            goal,
            workspace,
            search=lambda q: f"[fixture] offline results for '{q}' — local agents, MCP, Ollama",
        )
        intent = result.get("intent", "?")
        ok = result.get("ok", False)
        answer = str(result.get("answer", "")).splitlines()[0][:140]
        print(f"  → intent={intent} ok={ok}")
        print(f"  → {answer}")
        print()

    print("✅ Enhanced core agent demo complete.")
    print("All tools ran offline. Artifacts in:", workspace.resolve())
    print("Next: try `python examples/ready_chat_agent.py` or attach a real local model.")


if __name__ == "__main__":
    main()
