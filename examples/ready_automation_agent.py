#!/usr/bin/env python3
"""Ready-to-run automation agent demo (offline-first).

One-shot goals with core routing + real tools.
No live LLM required.

Usage:
  python examples/ready_automation_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"⚙️  grok-local-agent-kit Ready Automation Agent (v{__version__})")
    print("Offline one-shot automation with routing + tools + probes\n")

    workspace = Path(".grok/ready-automation")
    workspace.mkdir(parents=True, exist_ok=True)

    print("=== Multi-LLM probes ===")
    probes = probe_providers()
    for name, info in probes.items():
        print(f"  {name}: {info['status']} ({info.get('detail', '')})")
    print()

    goals = [
        "create a note that automation ran successfully",
        "compute sqrt(81) + 15",
        "list files in the workspace",
        "search local agent toolkits",
        "mcp echo automation ping",
    ]

    for goal in goals:
        print(f"Goal: {goal}")
        result = run_mvp(goal, workspace, search=lambda q: f"[fixture search] {q}")
        print(f"  Intent: {result['intent']} | Success: {result['ok']}")
        first = str(result.get('answer', '')).splitlines()[0][:140] if result.get('answer') else ""
        print(f"  Result: {first}")
        print()

    note = workspace / "mvp_note.txt"
    print(f"Note written: {note.exists()}")
    print("✅ Automation demo complete. Offline-first, no API keys.")
    print(f"Artifacts: {workspace.resolve()}")


if __name__ == "__main__":
    main()
