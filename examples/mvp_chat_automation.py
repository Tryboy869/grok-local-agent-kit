#!/usr/bin/env python3
"""
Ready-to-run MVP Chat + Automation Agent.
Fully offline: uses intent routing + real tools (calculator, files, datetime, system info).
No Ollama / LM Studio required.

Usage:
  python examples/mvp_chat_automation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure local package is importable when run from repo root
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grok_local_agent_kit.agent import Agent
from grok_local_agent_kit.tools import calculator, get_datetime, get_system_info, write_file, read_file


def offline_router(prompt: str) -> str:
    """Simple offline intent router for demo purposes. Handles basic compound cases."""
    p = prompt.lower()
    if any(w in p for w in ("time", "date", "now", "heure")):
        return get_datetime()
    if any(w in p for w in ("system", "os", "python", "cpu", "info")):
        return get_system_info()
    if any(w in p for w in ("calc", "calculate", "math", "compute", "2**", "2^", "+", "*")):
        # Extract a simple expression if present
        expr = prompt
        for prefix in ("calculate ", "compute ", "what is ", "calc ", "calculate"):
            if expr.lower().startswith(prefix):
                expr = expr[len(prefix):].strip()
                break
        # Handle compound like "calculate X and write to file"
        if "write" in p or "save" in p or "to file" in p:
            result = calculator(expr.split(" and ")[0].strip())
            content = f"Calculation result: {result}\nFrom: {prompt}"
            write_file("mvp_note.txt", content)
            return f"{result}\n(also saved to mvp_note.txt)"
        return calculator(expr.strip())
    if "write" in p or "save" in p or "create file" in p:
        content = "Note created by offline MVP agent.\nPrompt was: " + prompt
        return write_file("mvp_note.txt", content)
    if "read" in p and "note" in p:
        return read_file("mvp_note.txt")
    return (
        "Offline MVP router: I handled time, math, system info, and simple file ops. "
        "For full ReAct tool-calling, start Ollama or LM Studio and use Agent().chat()."
    )


def main() -> None:
    print("=== grok-local-agent-kit MVP (offline) ===\n")

    # 1. Chat-style demo
    print("--- Chat agent (offline routing) ---")
    for q in [
        "What is the current time?",
        "Calculate 2**10 + 42",
        "Show system info",
        "Write a note saying the MVP works",
        "Read the note",
    ]:
        print(f"User: {q}")
        print(f"Agent: {offline_router(q)}\n")

    # 2. Full Agent object (tools available, but offline path)
    print("--- Agent object (tools registered, offline run) ---")
    agent = Agent(verbose=False, max_iterations=4)
    print("Registered tools:", ", ".join(agent.list_registered_tools()[:8]), "...")

    # Automation-style: chain via the router
    print("\nAutomation plan:")
    plan = [
        "get current datetime",
        "calculate 1024 + 42",
        "write result to automation_result.txt",
    ]
    for step in plan:
        print(f"  step: {step} -> {offline_router(step)[:80]}")

    print("\nDone. For live LLM: ollama serve && python examples/chat_agent.py")
    print("See README for 1-command install and more examples.")


if __name__ == "__main__":
    main()
