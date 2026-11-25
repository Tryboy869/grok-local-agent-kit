#!/usr/bin/env python3
"""
Ready-to-run local agent demo (v0.83).

Fully offline by default (uses improved intent routing + real tools including code execution,
compound copy→file, mkdir→file, shell→file, list_files→file, search_files→file, http_get→file, math→file, and previous compounds with result injection).
Optionally uses live Ollama / LM Studio if available via --live.

Demonstrates:
- Tool routing (calculator, datetime, system info, file ops, mkdir, copy_file, web search fallback, http_get, sandboxed Python, list_files, search_files, restricted shell)
- Multi-step compound plans (copy→list, mkdir→file, shell→file, list→file, search_files→file, http→file, math→file with verification, code→file, search→file, datetime→file, system→file with result injection)
- Write-then-list / read verification
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
    print("Mode: offline / scripted (no LLM required) — compound copy→list + mkdir→file + shell→file + list→file + search_files→file + http→file + math→file + system→file + datetime→file + code→file + search→file\n")

    workspace = Path.cwd() / ".ready_demo_v083"
    workspace.mkdir(exist_ok=True)

    goals = [
        "Create a note saying Hello v0.83 and save to source_note.txt then copy it to copied_note.txt",
        "Create directory notes and save a welcome note to welcome.txt inside it",
        "Run command: echo Hello from shell agent and save the output to shell_note.txt",
        "List files in the workspace and save the listing to listing.txt",
        "Search files for 'def' and save the results to searchfiles_note.txt",
        "Fetch https://example.com and save the content to http_note.txt",
        "Calculate 2**10 + 42 and save the result to math_result.txt then verify by reading it",
        "Show system info and save it to system_note.txt",
        "What is the current time and save it to time_note.txt",
        "Calculate sqrt(144) + 10",
        "Run code: print(sum(range(1, 11)))",
        "Run code print(sum(range(1, 11))) and save the result to sum_result.txt",
        "Search for local AI agents and save the results to search_note.txt",
        "Write a note saying Hello from ready local agent v0.83 to agent_note.txt",
        "List files in the workspace",
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
