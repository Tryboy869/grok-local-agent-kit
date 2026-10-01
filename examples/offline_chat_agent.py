#!/usr/bin/env python3
"""Chat agent that runs without Ollama or LM Studio.

Uses ScriptedLLM so the real Agent tool loop is exercisable in CI and on a
fresh laptop. Swap `llm=ScriptedLLM()` for a live provider when a daemon is up.
"""

from pathlib import Path
import tempfile

from grok_local_agent_kit.offline import run_offline


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="chat-") as raw:
        root = Path(raw)
        (root / "hello.txt").write_text("hello\n", encoding="utf-8")
        print(run_offline("list files", root))


if __name__ == "__main__":
    main()
