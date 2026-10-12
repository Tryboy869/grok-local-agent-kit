#!/usr/bin/env python3
"""Ready-to-run automation agent that uses the offline MVP core by default.

Demonstrates file ops, math, system info, and search fixtures without a model.
Falls back to live ReAct if a local LLM is up.

Usage:
  python examples/enhanced_automation_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"🤖 Enhanced Automation Agent (v{__version__})")
    workspace = Path(".grok/automation-demo")
    workspace.mkdir(parents=True, exist_ok=True)

    probes = probe_providers()
    live = any(p["status"] == "up" for p in probes.values())
    print("Providers:", {k: v["status"] for k, v in probes.items()})
    print("Mode:", "live ReAct" if live else "offline MVP core\n")

    goals = [
        "write a note that automation completed successfully",
        "compute (21 * 2) + sqrt(16)",
        "list files in the workspace",
        "search for local AI agents with tools",
        "what is the current system info",
    ]

    for i, goal in enumerate(goals, 1):
        print(f"{i}. {goal}")
        result = run_mvp(
            goal,
            workspace,
            search=lambda q: f"[fixture] Top result for '{q}': local agent kits (Ollama + MCP)",
        )
        status = "OK" if result["ok"] else "PARTIAL"
        print(f"   [{status}] intent={result['intent']}")
        print(f"   → {result['answer'].splitlines()[0][:100]}\n")

    note = workspace / "mvp_note.txt"
    if note.exists():
        print(f"Note written: {note.read_text().strip()[:120]}")

    print("\n✅ Automation complete (offline-first).")
    if not live:
        print("Start a local model for full ReAct chat: see examples/chat_agent.py")


if __name__ == "__main__":
    main()
