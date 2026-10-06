#!/usr/bin/env python3
"""Offline chat MVP — intent routing + tools, no model required.

Usage:
  python examples/mvp_chat.py
  python examples/mvp_chat.py "compute sqrt(144) + 10"
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline local chat MVP")
    parser.add_argument("prompt", nargs="?", default="write a note that the chat agent is ready")
    parser.add_argument("--workspace", default=".grok/mvp-chat")
    args = parser.parse_args()
    print(f"Local chat MVP v{__version__} (scripted router, Ollama/LM Studio optional)")
    for name, row in probe_providers().items():
        print(f"  provider {name}: {row['status']}")
    result = run_mvp(args.prompt, Path(args.workspace), search=lambda q: f"(offline) {q}")
    print(f"intent: {result['intent']}")
    for step in result["steps"]:
        print(f"  tool {step['tool']} -> {step['output'].splitlines()[0][:120]}")
    print(f"\nAgent › {result['answer']}")


if __name__ == "__main__":
    main()
