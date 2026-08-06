#!/usr/bin/env python3
"""
Code assistant example — analyze & improve a small Python snippet using tools.

Requires Ollama (or LM Studio) running with a coding-capable model.

Usage:
  python examples/code_assistant.py
"""

from __future__ import annotations

from grok_local_agent_kit import create_agent, __version__


def main() -> None:
    agent = create_agent(model="llama3.2", provider="ollama", verbose=True)

    print(f"💻 Code Assistant (v{__version__})\n")

    task = (
        "Create a file named fib.py containing a recursive Fibonacci function. "
        "Then use execute_python to compute fib(10) and print the result. "
        "Finally list the files to confirm fib.py exists and summarize what you did."
    )

    print(f"Task:\n{task}\n")
    result = agent.run(task)
    print("\n=== Final answer ===")
    print(result)

    agent.close()


if __name__ == "__main__":
    main()
