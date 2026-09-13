#!/usr/bin/env python3
"""Pack and search the current workspace without a live LLM.

Usage:
  python examples/workspace_agent.py
  python examples/workspace_agent.py --query "routing ollama"
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit.workspace import pack_workspace, search_workspace


def main() -> None:
    parser = argparse.ArgumentParser(description="Workspace pack + file RAG")
    parser.add_argument("--path", default=".")
    parser.add_argument("--query", default="local agent tools MCP")
    args = parser.parse_args()

    print("=== pack ===")
    print(pack_workspace(args.path))
    print("\n=== search ===")
    print(search_workspace(args.query, path=args.path))


if __name__ == "__main__":
    main()
