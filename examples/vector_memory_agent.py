#!/usr/bin/env python3
"""Vector memory demo — no live LLM required.

Stores notes in SQLite and ranks them with a hashed bag-of-words cosine.

Usage:
  python examples/vector_memory_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit.vector_memory import vforget, vrecall, vremember, vstats


def main() -> None:
    db = Path(".grok") / "memory" / "demo-vectors.db"
    print(vremember("Ollama runs llama3.2 locally without API keys", "llm,local", db))
    print(vremember("LM Studio exposes an OpenAI-compatible server on :1234", "llm", db))
    print(vremember("MCP stdio discovers tools and registers mcp_<server>_<tool>", "mcp", db))
    print()
    print(vstats(db))
    print()
    print(vrecall("local llama model", limit=2, db_path=db))
    print()
    print(vforget("LM Studio", db_path=db))
    print(vstats(db))


if __name__ == "__main__":
    main()
