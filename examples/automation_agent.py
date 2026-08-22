#!/usr/bin/env python3
"""
Automation agent example — one-shot goal with tools.

Creates a small Python script, lists files, runs a calculation,
checks system info, and searches the web.

Requires Ollama (or LM Studio) running.

Usage:
  python examples/automation_agent.py
"""

from __future__ import annotations

from grok_local_agent_kit import create_agent, __version__


def main() -> None:
    agent = create_agent(verbose=True, stream=True)

    print(f"🤖 Automation Agent (v{__version__})\n")

    goal = (
        "1. Create a file named hello_from_agent.py that prints "
        "'Hello from local agent!'. "
        "2. List the files in the current directory and confirm the new file exists. "
        "3. Use the calculator to compute sqrt(144) + 10. "
        "4. Call get_system_info and note the OS and Python version. "
        "5. Do a quick web search for 'local AI agents 2026' and give me the top 3 titles. "
        "Finally summarize everything you did."
    )

    print(f"Goal:\n{goal}\n")
    result = agent.run(goal)
    print("\n=== Final answer ===")
    print(result)

    agent.close()


if __name__ == "__main__":
    main()
