#!/usr/bin/env python3
"""Vector memory with optional Ollama embeddings.

Default backend is hashed bag-of-words (offline).
To use a live embedding model:

  ollama pull nomic-embed-text
  GROK_EMBED_BACKEND=ollama python examples/embed_agent.py
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from grok_local_agent_kit.embeddings import backend_name, embed
from grok_local_agent_kit.vector_memory import vrecall, vremember, vstats


def main() -> None:
    print(f"embed backend: {backend_name()}  dim={len(embed('probe'))}")
    with tempfile.TemporaryDirectory() as td:
        db = Path(td) / "v.db"
        print(vremember("Ship grok-local-agent-kit v0.14 with ollama embeddings", "release", db))
        print(vremember("Banana smoothie with oat milk", "food", db))
        print(vrecall("local agent kit release", db_path=db))
        print(vstats(db))


if __name__ == "__main__":
    main()
