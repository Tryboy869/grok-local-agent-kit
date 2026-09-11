#!/usr/bin/env python3
"""Demo: vector memory with optional sqlite-vec, hash fallback always works."""

from pathlib import Path
from tempfile import TemporaryDirectory

from grok_local_agent_kit.sqlite_vec_store import active_backend, describe, knn
from grok_local_agent_kit.vector_memory import vremember


def main() -> None:
    print(describe())
    with TemporaryDirectory() as tmp:
        db = Path(tmp) / "vectors.db"
        print(vremember("Ollama runs Llama models on a laptop", db_path=db))
        print(vremember("LM Studio exposes an OpenAI-compatible HTTP API", db_path=db))
        print(vremember("MCP lets an agent call local stdio tools", db_path=db))
        print("backend:", active_backend())
        for score, rid, _ts, text, _tags in knn("local llama inference", limit=2, db_path=db):
            print(f"  #{rid} {score:.3f} {text}")


if __name__ == "__main__":
    main()
