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

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from grok_local_agent_kit.tools import calculator, get_datetime, get_system_info, write_file, read_file, list_files


def offline_router(prompt: str) -> str:
    """Improved offline intent router. Handles compound plans (math→file, multi-step)."""
    p = prompt.lower().strip()

    # Multi-step plan detection (simple)
    if "then" in p or " and " in p or ";" in p:
        parts = [part.strip() for part in p.replace(";", " and ").split(" and ") if part.strip()]
        if len(parts) > 1:
            results = []
            for part in parts:
                results.append(offline_router(part))
            return "\n".join(f"• {r}" for r in results)

    if any(w in p for w in ("time", "date", "now", "heure", "datetime")):
        return get_datetime()
    if any(w in p for w in ("system", "os", "python", "cpu", "info", "platform")):
        return get_system_info()
    if any(w in p for w in ("list", "ls", "files", "dir")):
        return list_files(".")
    if any(w in p for w in ("calc", "calculate", "math", "compute", "2**", "2^", "+", "*", "sqrt", "pow")):
        expr = prompt
        for prefix in ("calculate ", "compute ", "what is ", "calc ", "calculate"):
            if expr.lower().startswith(prefix):
                expr = expr[len(prefix):].strip()
                break
        if "write" in p or "save" in p or "to file" in p or "note" in p:
            result = calculator(expr.split(" and ")[0].strip())
            content = f"Calculation result: {result}\nFrom: {prompt}\n"
            write_file("mvp_note.txt", content)
            return f"{result}\n(also saved to mvp_note.txt)"
        return calculator(expr.strip())
    if "write" in p or "save" in p or "create file" in p or "note" in p:
        content = "Note created by offline MVP agent.\nPrompt was: " + prompt + "\n"
        return write_file("mvp_note.txt", content)
    if "read" in p and ("note" in p or "file" in p or "mvp" in p):
        return read_file("mvp_note.txt")
    return (
        "Offline MVP router: handled time, math, system info, list files, and simple file ops. "
        "For full ReAct tool-calling, start Ollama or LM Studio and use Agent().chat()."
    )


def main() -> None:
    print("=== grok-local-agent-kit MVP (offline) ===\n")

    print("--- Chat agent (offline routing) ---")
    for q in [
        "What is the current time?",
        "Calculate 2**10 + 42",
        "Show system info",
        "List files in the current directory",
        "Write a note saying the MVP works",
        "Read the note",
        "Calculate 144**0.5 + 10 and write the result to a note",
    ]:
        print(f"User: {q}")
        print(f"Agent: {offline_router(q)}\n")

    print("--- Agent object (tools registered, offline run) ---")
    from grok_local_agent_kit.agent import Agent
    agent = Agent(verbose=False, max_iterations=4)
    print("Registered tools:", ", ".join(agent.list_registered_tools()[:8]), "...")

    print("\nAutomation plan (compound):")
    plan = [
        "get current datetime",
        "calculate 1024 + 42",
        "write result to automation_result.txt",
        "list files",
    ]
    for step in plan:
        print(f"  step: {step} -> {offline_router(step)[:100]}")

    print("\nDone. For live LLM: ollama serve && python examples/chat_agent.py")
    print("See README for 1-command install and more examples.")


if __name__ == "__main__":
    main()
