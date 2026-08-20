#!/usr/bin/env python3
"""
Interactive chat agent example.

Requires a running local LLM:
  - Ollama:  ollama serve && ollama pull llama3.2
  - LM Studio: start the local server (default port 1234)

Usage:
  python examples/chat_agent.py
  python examples/chat_agent.py --provider lmstudio --model local-model
  python examples/chat_agent.py --verbose --stream
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit import create_agent, __version__


def main() -> None:
    parser = argparse.ArgumentParser(description="Local chat agent")
    parser.add_argument("--model", default=None, help="Override GROK_AGENT_MODEL")
    parser.add_argument(
        "--provider",
        default=None,
        choices=["ollama", "lmstudio", "openai"],
        help="Override GROK_AGENT_PROVIDER",
    )
    parser.add_argument("--base-url", default=None)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--stream", action="store_true", help="Stream final answer tokens")
    args = parser.parse_args()

    agent = create_agent(
        model=args.model,
        provider=args.provider,
        base_url=args.base_url,
        verbose=args.verbose,
        stream=args.stream or args.verbose,
    )

    print(f"🚀 Local Chat Agent ready (v{__version__})")
    print(
        "   Tools: web_search, http_get, files (cwd-safe), shell, execute_python, "
        "calculator, list_tools, MCP foundation"
    )
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
