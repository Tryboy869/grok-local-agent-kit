#!/usr/bin/env python3
"""
Parallel tools + thought/trace demo (no live LLM required).

Shows two tools running in one ReAct turn, on_thought firing, and
export_trace writing .grok/traces/last.json.

Usage:
  python examples/parallel_agent.py
"""

from __future__ import annotations

from grok_local_agent_kit import create_agent, __version__


class ScriptedLLM:
    def __init__(self) -> None:
        self.model = "scripted"
        self.provider = "fake"
        self.base_url = ""
        self._n = 0

    def chat(self, messages, tools=None, tool_choice="auto"):
        self._n += 1
        if self._n == 1:
            return {
                "content": "I'll list files and compute 7*6 in parallel.",
                "tool_calls": [
                    {"id": "t1", "name": "list_files", "arguments": {"path": "."}},
                    {"id": "t2", "name": "calculator", "arguments": {"expression": "7*6"}},
                ],
            }
        return {"content": "Listed the workspace and 7*6 = 42.", "tool_calls": None}

    def stream_chat(self, messages, tools=None):
        yield from []
        return {"content": "Listed the workspace and 7*6 = 42.", "tool_calls": None}

    def ping(self) -> str:
        return "ok — scripted"

    def close(self) -> None:
        return None


def main() -> None:
    agent = create_agent(model="dummy", provider="ollama", verbose=True, parallel_tools=True)
    agent.llm = ScriptedLLM()
    thoughts = []
    agent.on("on_thought", lambda **p: thoughts.append(p.get("text", "")))

    print(f"⇢ Parallel tool agent (v{__version__})\n")
    print(agent.run("List files and multiply 7*6."))
    print("\nthoughts:", thoughts)
    print(agent.export_trace())
    if hasattr(agent, "usage"):
        print(agent.usage.summary())
    agent.close()


if __name__ == "__main__":
    main()
