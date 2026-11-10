#!/usr/bin/env python3
"""
Ready-to-run offline compound agent.

Demonstrates multi-step plans (math → write file, datetime + system info)
using the real Agent tool loop and ScriptedLLM. No local model required.

Usage:
  python examples/ready_compound_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit.offline import run_offline


def main() -> None:
    print("=== grok-local-agent-kit ready compound agent (offline) ===\n")
    root = Path("./_offline_workspace")
    root.mkdir(exist_ok=True)
    (root / "seed.txt").write_text("seed content\n", encoding="utf-8")

    prompts = [
        "list files",
        "what is the current datetime?",
        "get system info",
        "calculate 2**10 + 42 and write the result to result.txt",
        "write a short note about local agents",
    ]

    for i, prompt in enumerate(prompts, 1):
        print(f"--- Step {i}: {prompt} ---")
        result = run_offline(prompt, root, note_name=f"note-{i}.txt")
        print(result.strip()[:600])
        print()

    print("Done. Workspace files:")
    for p in sorted(root.glob("*")):
        if p.is_file():
            print(f"  {p.name} ({p.stat().st_size} B)")
    print("\nFully offline. Start Ollama or LM Studio for live ReAct chat.")


if __name__ == "__main__":
    main()
