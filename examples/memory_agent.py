#!/usr/bin/env python3
"""Demo local memory tools without requiring a live LLM."""

from grok_local_agent_kit.memory import forget, memory_stats, recall, remember
from grok_local_agent_kit.tools import execute_tool, get_default_tools


def main() -> None:
    print(remember("Preferred model is llama3.2 on Ollama", tags="prefs,llm"))
    print(remember("Workspace safety: file tools stay under cwd", tags="safety"))
    print(recall("ollama"))
    print(memory_stats())
    _, funcs = get_default_tools()
    print(execute_tool("recall", {"query": "cwd"}, funcs))
    print(forget("Preferred model"))
    print(memory_stats())


if __name__ == "__main__":
    main()
