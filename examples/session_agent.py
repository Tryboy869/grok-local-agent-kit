#!/usr/bin/env python3
"""Named session example — persist history under .grok/sessions/.

Usage:
  python examples/session_agent.py --session demo
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit import create_agent, __version__


def main() -> None:
    parser = argparse.ArgumentParser(description="Named-session local agent")
    parser.add_argument("--session", default="demo")
    parser.add_argument("--model", default=None)
    parser.add_argument("--provider", default=None, choices=["ollama", "lmstudio", "openai"])
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--attach-mcp", action="store_true")
    args = parser.parse_args()

    agent = create_agent(
        model=args.model,
        provider=args.provider,
        verbose=args.verbose,
        session_name=args.session,
        attach_mcp=args.attach_mcp,
    )
    print(agent.load_named_session(args.session))
    print(f"Session agent v{__version__} — session={agent.session_name}")
    print("Type exit to quit. History is saved automatically.\n")
    try:
        while True:
            user = input("You › ").strip()
            if user.lower() in {"exit", "quit", "q"}:
                break
            if not user:
                continue
            print(f"\nAgent › {agent.chat(user)}\n")
    except (KeyboardInterrupt, EOFError):
        print("\nBye!")
    finally:
        print(agent.save_named_session(args.session))
        agent.close()


if __name__ == "__main__":
    main()
