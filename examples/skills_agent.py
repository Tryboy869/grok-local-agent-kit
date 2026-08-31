#!/usr/bin/env python3
"""Load a JSON skill pack and invoke the registered tool (no LLM required)."""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import create_agent, __version__


def main() -> None:
    example_dir = Path(__file__).resolve().parent / "skills"
    agent = create_agent(model="dummy", provider="ollama", verbose=False)
    added = agent.load_skills(str(example_dir))
    print(f"Skills demo v{__version__}")
    print(f"loaded tools: {added}")
    if "greet_workspace" in agent.tool_funcs:
        print(agent.tool_funcs["greet_workspace"](name="grok-local-agent-kit"))
    else:
        print("greet_workspace was not registered")
    agent.close()


if __name__ == "__main__":
    main()
