#!/usr/bin/env python3
"""
Ready-to-run local agent demo (v0.72).

Fully offline by default (uses scripted/intent routing + real tools).
Optionally uses live Ollama / LM Studio if available via --live.

Demonstrates:
- Tool routing (calculator, datetime, system info, file ops, web search fallback)
- Multi-step compound plans
- Multi-LLM ready (falls back gracefully)
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from grok_local_agent_kit import create_agent, __version__
from grok_local_agent_kit.mvp import run_mvp, probe_providers


def offline_demo() -> None:
    print(f"=== grok-local-agent-kit Ready Local Agent (v{__version__}) ===\n")
    print("Mode: offline / scripted (no LLM required)\n")

    workspace = Path.cwd() / ".ready_demo"
    workspace.mkdir(exist_ok=True)

    goals = [
        "What is the current time?",
        "Calculate 2**10 + 42",
        "Show system info",
        "Write a note saying Hello from ready local agent (offline MVP) to agent_note.txt",
        "Calculate sqrt(144) + 10 and save the result to math_result.txt",
    ]

    for i, goal in enumerate(goals, 1):
        print(f"{i}. Goal: {goal}")
        result = run_mvp(goal, workspace)
        answer = result.get("answer", "")
        print(f"   → {str(answer).strip()[:200]}\n")

    print("Providers probe (non-blocking):")
    print(json.dumps(probe_providers(), indent=2, default=str))
    print("\nDone. For live ReAct loop start Ollama or LM Studio and re-run with --live.\n")
    print(f"Demo workspace: {workspace}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Use real LLM if available")
    args = parser.parse_args()

    if not args.live:
        offline_demo()
        return

    print(f"🚀 Live agent (v{__version__}) — trying Ollama / LM Studio...\n")
    try:
        agent = create_agent(verbose=True, stream=True, use_router=True)
        reply = agent.run(
            "What is the current time, compute 2**10 + 42, "
            "write the result to math_live.txt, then list the files and summarize."
        )
        print("\n=== Final ===\n", reply)
        agent.close()
    except Exception as e:
        print("Live mode failed (no local model?). Falling back to offline demo.\n", e)
        offline_demo()


if __name__ == "__main__":
    main()
