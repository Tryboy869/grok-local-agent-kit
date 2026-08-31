#!/usr/bin/env python3
"""Hooks example — observe tool calls from the live ReAct loop."""

from __future__ import annotations

from grok_local_agent_kit import create_agent, __version__


class FakeLLM:
    def __init__(self):
        self.calls = 0
        self.model = "fake"
        self.provider = "fake"
        self.base_url = ""

    def chat(self, messages, tools=None, tool_choice="auto"):
        self.calls += 1
        if self.calls == 1:
            return {
                "content": "",
                "tool_calls": [
                    {
                        "id": "c1",
                        "name": "calculator",
                        "arguments": {"expression": "21*2"},
                    }
                ],
            }
        return {"content": "42", "tool_calls": None}

    def close(self):
        return None


def main() -> None:
    seen = []
    agent = create_agent(model="dummy", provider="ollama", verbose=False)
    agent.llm = FakeLLM()

    def before(*, name, args, **_):
        seen.append(("before", name))
        print(f"before_tool {name} {args}")

    def after(*, name, result, **_):
        seen.append(("after", name))
        print(f"after_tool  {name} -> {str(result)[:80]}")

    def final(*, text, **_):
        seen.append(("final", text))
        print(f"on_final {text}")

    agent.on("before_tool", before)
    agent.on("after_tool", after)
    agent.on("on_final", final)

    print(f"Hooks demo v{__version__} (fake LLM, real loop)\n")
    print(agent.run("What is 21*2?"))
    print(f"\nevents: {seen}")
    print(f"trace: {agent.last_trace}")
    agent.close()


if __name__ == "__main__":
    main()
