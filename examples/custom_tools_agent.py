#!/usr/bin/env python3
"""
Custom tools example — register your own tools at runtime.

Shows how to extend the agent with domain-specific tools while keeping
the built-in ones (web, files, shell, calculator, MCP foundation…).

Requires a running local LLM (Ollama or LM Studio).

Usage:
  python examples/custom_tools_agent.py
  python examples/custom_tools_agent.py --verbose
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone

from grok_local_agent_kit import create_agent, __version__


def greet(name: str) -> str:
    """Simple custom tool: personalized greeting."""
    return f"Hello, {name}! Greeted at {datetime.now(timezone.utc).isoformat()}."


def word_count(text: str) -> str:
    """Count words and characters in a string."""
    words = len(text.split())
    chars = len(text)
    return f"words={words}, chars={chars}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Custom tools agent example")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--stream", action="store_true")
    args = parser.parse_args()

    agent = create_agent(verbose=args.verbose, stream=args.stream or args.verbose)

    # Register custom tools
    agent.register_tools(
        [
            {
                "name": "greet",
                "func": greet,
                "description": "Greet a person by name and return a timestamped message.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "Name to greet"},
                    },
                    "required": ["name"],
                },
            },
            {
                "name": "word_count",
                "func": word_count,
                "description": "Count words and characters in a piece of text.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "Text to analyse"},
                    },
                    "required": ["text"],
                },
            },
        ]
    )

    print(f"🧩 Custom Tools Agent (v{__version__})")
    print(f"   Registered tools: {agent.list_registered_tools()}")
    print()

    goal = (
        "1. Use the greet tool to say hello to 'Local Agent'. "
        "2. Use word_count on the sentence 'Offline-first AI agents that actually call tools'. "
        "3. Use get_system_info to report the OS and Python version. "
        "Summarize the results."
    )

    print(f"Goal:\n{goal}\n")
    result = agent.run(goal)
    print("\n=== Final answer ===")
    print(result)

    agent.close()


if __name__ == "__main__":
    main()
