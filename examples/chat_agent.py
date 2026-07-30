#!/usr/bin/env python3
"""
Interactive chat agent example.

Requires a running local LLM:
  - Ollama:  ollama serve && ollama pull llama3.2
  - LM Studio: start the local server (default port 1234)

Usage:
  python examples/chat_agent.py
  python examples/chat_agent.py --provider lmstudio --model local-model
  python examples/chat_agent.py --verbose
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit import create_agent, __version__


def main() -> None:
    parser = argparse.ArgumentParser(description="Local chat agent")
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument(
        "--provider",
        default="ollama",
        choices=["ollama", "lmstudio", "openai"],
    )
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    provider = args.provider
    base_url = args.base_url
    if provider == "lmstudio":
        provider = "openai"
        base_url = base_url or "http://localhost:1234/v1"

    agent = create_agent(
        model=args.model,
        provider=provider,
        base_url=base_url,
        verbose=args.verbose,
    )

    print(f"🚀 Local Chat Agent ready (v{__version__})")
    print("   Tools: web_search, files, shell, execute_python, calculator, MCP stub")
    print("   Type 'exit' / 'quit' / Ctrl-C to leave.\n")

    try:
        while True:
            user = input("You › ").strip()
            if user.lower() in {"exit", "quit", "q"}:
                break
            if not user:
                continue
            reply = agent.chat(user)
            print(f"\nAgent › {reply}\n")
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
    finally:
        agent.close()


if __name__ == "__main__":
    main()
