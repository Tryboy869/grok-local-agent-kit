#!/usr/bin/env python3
"""
Automation agent example — one-shot goal with tools.

Creates a small Python script, lists files, and searches the web.

Requires Ollama (or LM Studio) running.

Usage:
  python examples/automation_agent.py
"""

from __future__ import annotations

from grok_local_agent_kit import create_agent


def main() -> None:
    agent = create_agent(model="llama3.2", provider="ollama", verbose=True)

    print("🤖 Automation Agent\n")

    goal = (
        "Create a file named hello_from_agent.py that prints "
        "'Hello from local agent!'. Then list the files in the current directory "
        "and confirm the new file exists. Finally do a quick web search for "
        "'local AI agents 2026' and give me the top titles."
    )

    print(f"Goal: {goal}\n")
    result = agent.run(goal)
    print("\n=== Final answer ===")
    print(result)

    agent.close()


if __name__ == "__main__":
    main()
