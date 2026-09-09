#!/usr/bin/env python3
"""Demo: tool latency telemetry. Safe to run without an LLM."""

from grok_local_agent_kit.telemetry import Telemetry, timed_execute
from grok_local_agent_kit.tools import execute_tool, get_default_tools


def main() -> None:
    registry = get_default_tools()
    tel = Telemetry()

    def run(name, args):
        return execute_tool(name, args, registry)

    print(timed_execute("calculator", {"expression": "7*6"}, run, telemetry=tel))
    print(timed_execute("calculator", {"expression": "1+1"}, run, telemetry=tel))
    print(tel.summary())


if __name__ == "__main__":
    main()
