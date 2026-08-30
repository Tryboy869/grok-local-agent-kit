#!/usr/bin/env python3
"""Hooks example — observe every tool call without a live LLM.

Usage:
  python examples/hooks_agent.py
"""

from __future__ import annotations

from grok_local_agent_kit import create_agent, __version__
from grok_local_agent_kit.tools import execute_tool


def main() -> None:
    seen = []
    agent = create_agent(model="dummy", provider="ollama", verbose=False)

    def before(*, name, args, **_):
        seen.append(("before", name))
        print(f"before_tool {name} {args}")

    def after(*, name, result, **_):
        seen.append(("after", name))
        print(f"after_tool  {name} -> {str(result)[:80]}")

    agent.on("before_tool", before)
    agent.on("after_tool", after)

    print(f"Hooks demo v{__version__} (no LLM required)\n")
    agent.hooks.emit("before_tool", name="calculator", args={"expression": "2+2"})
    result = execute_tool("calculator", {"expression": "2+2"}, agent.tool_funcs)
    agent.hooks.emit("after_tool", name="calculator", args={"expression": "2+2"}, result=result)
    agent.hooks.emit("on_final", text="4")
    print(f"\nevents: {seen}")
    agent.close()


if __name__ == "__main__":
    main()
