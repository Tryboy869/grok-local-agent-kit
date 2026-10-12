#!/usr/bin/env python3
"""Enhanced ready-to-run chat agent with explicit multi-LLM routing demo.

Works offline for tool demos via MVP path; live chat requires Ollama or LM Studio.

Usage:
  python examples/enhanced_chat_agent.py
  python examples/enhanced_chat_agent.py --provider lmstudio
  python examples/enhanced_chat_agent.py --offline
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit import create_agent, __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp
from grok_local_agent_kit.router import MultiLLMRouter


def demo_offline(workspace: Path) -> None:
    print("=== Offline core routing + tools (no model) ===")
    for name, info in probe_providers().items():
        print(f"  {name}: {info['status']}")
    goals = [
        "write a note: local agent kit is ready",
        "calculate 42 * 2 + sqrt(16)",
        "list files here",
        "search for Ollama MCP",
    ]
    for g in goals:
        r = run_mvp(g, workspace, search=lambda q: f"[offline fixture] {q}")
        print(f"\nGoal: {g}")
        print(f"  intent={r['intent']} ok={r['ok']}")
        print(f"  answer: {r['answer'].splitlines()[0][:120]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Enhanced local chat agent")
    parser.add_argument("--provider", choices=["ollama", "lmstudio", "openai"], default=None)
    parser.add_argument("--model", default=None)
    parser.add_argument("--offline", action="store_true", help="Run offline MVP demos only")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print(f"🚀 Enhanced Local Chat Agent (v{__version__})")
    workspace = Path(".grok/enhanced-demo")
    workspace.mkdir(parents=True, exist_ok=True)

    if args.offline or not any(p["status"] == "up" for p in probe_providers().values()):
        print("No live local LLM detected (or --offline). Running core MVP demos.\n")
        demo_offline(workspace)
        print("\nStart Ollama (`ollama serve && ollama pull llama3.2`) or LM Studio, then re-run without --offline.")
        return

    print("Live local LLM detected. Starting interactive chat with multi-LLM router.\n")
    router = MultiLLMRouter()
    agent = create_agent(
        model=args.model,
        provider=args.provider,
        verbose=args.verbose,
        use_router=True,
    )
    print("Type 'exit' to quit. Tools available: files, calculator, web_search, MCP, system info.\n")

    while True:
        try:
            user = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if user.lower() in {"exit", "quit", "q"}:
            break
        if not user:
            continue
        if user.startswith("/mvp "):
            r = run_mvp(user[5:], workspace)
            print(f"Agent (MVP): {r['answer']}")
            continue
        answer = agent.run(user)
        print(f"Agent: {answer}\n")

    agent.close()
    print("Session ended.")


if __name__ == "__main__":
    main()
