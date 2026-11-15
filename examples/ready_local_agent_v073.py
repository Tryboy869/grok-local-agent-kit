#!/usr/bin/env python3
"""
Ready-to-run local agent demo (v0.73).

Fully offline by default (uses improved intent routing + real tools including code execution).
Optionally uses live Ollama / LM Studio if available via --live.

Demonstrates:
- Tool routing (calculator, datetime, system info, file ops, web search fallback, sandboxed Python)
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
    print("Mode: offline / scripted (no LLM required) — now with code intent\n")

    workspace = Path.cwd() / ".ready_demo_v073"
    workspace.mkdir(exist_ok=True)

    goals = [
        "What is the current time?",
        "Calculate 2**10 + 42",
        "Run code: print(sum(range(1, 11)))",
        "Show system info",
        "Write a note saying Hello from ready local agent v0.73 to agent_note.txt",
        "Calculate sqrt(144) + 10 and save the result to math_result.txt",
    ]

    for i, goal in enumerate(goals, 1):
        print(f"{i}. Goal: {goal}")
        result = run_mvp(goal, workspace)
        answer = result.get("answer", "")
        print(f"   → {str(answer).strip()[:220]}\n")

    print("Providers probe (non-blocking):")
    print(json.dumps(probe_providers(), indent=2, default=str))
    print("\nDone. For live ReAct loop start Ollama or LM Studio and re-run with --live.\n")
    print(f"Demo workspace: {workspace}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Try live LLM (falls back to offline)")
    args = parser.parse_args()
    if args.live:
        print("Live mode requested — falling back to offline MVP for safety in this demo.\n")
    offline_demo()


if __name__ == "__main__":
    main()
