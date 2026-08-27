#!/usr/bin/env python3
"""
MCP agent example — talks to the bundled echo MCP server over stdio.

No extra npm packages required. Demonstrates:
  mcp_list_tools → mcp_call_tool(echo) → mcp_call_tool(add)

Requires a running local LLM for the agent loop.
You can also run the raw client without an LLM (see bottom).

Usage:
  python examples/mcp_agent.py
  python examples/mcp_agent.py --no-llm
"""

from __future__ import annotations

import argparse
import json
import os
import sys

from grok_local_agent_kit import MCPManager, __version__, create_agent


def _echo_server_config() -> str:
    return json.dumps(
        [
            {
                "name": "echo",
                "command": sys.executable,
                "args": ["-m", "grok_local_agent_kit.mcp_echo_server"],
            }
        ]
    )


def demo_no_llm() -> None:
    os.environ["GROK_MCP_SERVERS"] = _echo_server_config()
    mgr = MCPManager()
    try:
        print(mgr.describe())
        print("\n--- tools/list ---\n")
        print(mgr.list_tools())
        print("\n--- tools/call echo ---\n")
        print(mgr.call_tool("echo", {"message": "hello from mcp_agent"}))
        print("\n--- tools/call add ---\n")
        print(mgr.call_tool("add", {"a": 10, "b": 32}))
    finally:
        mgr.close()


def demo_with_llm() -> None:
    os.environ["GROK_MCP_SERVERS"] = _echo_server_config()
    agent = create_agent(verbose=True, stream=True)
    try:
        print(f"\U0001f50c MCP Agent (v{__version__})\n")
        goal = (
            "1. Call mcp_list_tools and report which MCP tools exist. "
            "2. Call mcp_call_tool with name=echo and arguments {\"message\":\"hi MCP\"}. "
            "3. Call mcp_call_tool with name=add and arguments {\"a\":7,\"b\":8}. "
            "Summarize the MCP results."
        )
        print(agent.run(goal))
    finally:
        agent.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-llm", action="store_true", help="Talk to MCP directly, skip the agent")
    args = parser.parse_args()
    if args.no_llm:
        demo_no_llm()
    else:
        demo_with_llm()


if __name__ == "__main__":
    main()
