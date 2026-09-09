#!/usr/bin/env python3
"""Demo: tool-result cache. Safe to run without an LLM."""

from grok_local_agent_kit.cache import ToolCache, cached_execute
from grok_local_agent_kit.tools import execute_tool, get_default_tools


def main() -> None:
    registry = get_default_tools()
    cache = ToolCache(ttl=30)

    def run(name, args):
        return execute_tool(name, args, registry)

    print("first:", cached_execute("calculator", {"expression": "21*2"}, run, cache))
    print("second (cached):", cached_execute("calculator", {"expression": "21*2"}, run, cache))
    print("stats:", cache.stats())


if __name__ == "__main__":
    main()
