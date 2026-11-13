#!/usr/bin/env python3
"""
Ready-to-run local agent demo (v0.71).

Fully offline by default (uses scripted/intent routing for common tasks).
Optionally uses live Ollama / LM Studio if available via --live.

Demonstrates:
- Tool routing (calculator, datetime, system info, file ops, web search fallback)
- Multi-step compound plans
- Multi-LLM ready (falls back gracefully)
"""

from __future__ import annotations

import argparse
import datetime
import platform
import sys
from pathlib import Path

from grok_local_agent_kit import create_agent, __version__


def offline_demo() -> None:
    print(f"=== grok-local-agent-kit Ready Local Agent (v{__version__}) ===\n")
    print("Mode: offline / scripted (no LLM required)\n")

    # Simulate a few tool calls that the real agent would make
    print("1. Datetime tool →", datetime.datetime.now().isoformat(timespec="seconds"))
    print("2. Calculator → 2**10 + 42 =", 2**10 + 42)
    print("3. System info →", platform.system(), platform.python_version(), Path.cwd())
    print("4. List files →", [p.name for p in Path.cwd().iterdir() if not p.name.startswith(".")][:8])
    note = Path("agent_note.txt")
    note.write_text("Hello from ready local agent (offline MVP)\n", encoding="utf-8")
    print("5. Wrote note →", note.read_text().strip())
    print("\nCompound plan example (math → file):")
    result = 144 ** 0.5 + 10
    Path("math_result.txt").write_text(f"sqrt(144)+10 = {result}\n", encoding="utf-8")
    print(f"   wrote math_result.txt with value {result}")
    print("\nDone. For live ReAct loop start Ollama or LM Studio and re-run with --live.\n")


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
