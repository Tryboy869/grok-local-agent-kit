#!/usr/bin/env python3
"""Ready-to-run core MVP demo for grok-local-agent-kit.

Demonstrates:
- Intent routing (offline, no model needed)
- Tool execution: file ops, calculator, web search fixture, system info
- Multi-LLM provider probing (Ollama / LM Studio) — reports status without failing
- Session-like batching

Usage (from repo root, after `pip install -e .`):
  python examples/mvp_core_demo.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"=== grok-local-agent-kit Core MVP Demo v{__version__} ===\n")
    print("Multi-LLM probes (optional backends):")
    for name, info in probe_providers().items():
        print(f"  • {name}: {info.get('status', 'unknown')} ({info.get('base_url', '')})")

    workspace = Path(".grok/mvp-core-demo")
    workspace.mkdir(parents=True, exist_ok=True)

    goals = [
        "write a note that the core agent MVP is ready",
        "compute 21 * 2 + sqrt(16)",
        "list files in the current workspace",
        "search for local AI agents with MCP",
        "what is the current Python and OS info",
    ]

    print("\nRouting + tool execution (offline):\n")
    for i, goal in enumerate(goals, 1):
        result = run_mvp(goal, workspace, search=lambda q: f"[fixture] results for: {q}")
        print(f"{i}. Goal: {goal}")
        print(f"   Intent: {result['intent']} | OK: {result['ok']}")
        answer_preview = result["answer"].splitlines()[0][:100] if result.get("answer") else "(no answer)"
        print(f"   Answer: {answer_preview}")
        if result.get("steps"):
            last = result["steps"][-1]
            print(f"   Last tool: {last.get('tool')} → {str(last.get('output', ''))[:80]}")
        print()

    note = workspace / "mvp_note.txt"
    if note.exists():
        print(f"Created note: {note.resolve()}")
        print(note.read_text()[:200])

    print("\n✅ Core MVP complete. For live chat: start Ollama or LM Studio, then `python examples/chat_agent.py`")
    print("For automation: `python examples/automation_agent.py`")
    print("Full CLI: `grok-agent doctor && grok-agent pack demo`")


if __name__ == "__main__":
    main()
