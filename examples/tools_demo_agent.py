#!/usr/bin/env python3
"""LLM-free tools demo — run this even if Ollama is not started.

Usage:
  python examples/tools_demo_agent.py
"""

from __future__ import annotations

from grok_local_agent_kit import __version__
from grok_local_agent_kit.tools import calculator, get_system_info, list_files, list_tools


def main() -> None:
    print(f"grok-local-agent-kit v{__version__} — tools demo (no LLM required)\n")
    print("=== registered tools ===")
    print(list_tools())
    print("\n=== calculator ===")
    print(calculator("sqrt(144) + 10"))
    print("\n=== list_files ===")
    print(list_files("."))
    print("\n=== system ===")
    print(get_system_info())


if __name__ == "__main__":
    main()
