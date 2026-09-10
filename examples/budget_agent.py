#!/usr/bin/env python3
"""Demo: cap tool calls so a looping agent cannot burn the machine."""

from grok_local_agent_kit.budget import ToolBudget, get_budget, set_budget
from grok_local_agent_kit.tools import execute_tool, get_default_tools


def main() -> None:
    from grok_local_agent_kit.cache import get_cache

    get_cache().enabled = False
    set_budget(ToolBudget(max_calls=3, per_tool={"calculator": 2}))
    _, registry = get_default_tools()
    for i in range(5):
        out = execute_tool("calculator", {"expression": f"{i}+1"}, registry)
        print(f"call {i}: {out[:80]}")
    print("stats:", get_budget().stats())


if __name__ == "__main__":
    main()
