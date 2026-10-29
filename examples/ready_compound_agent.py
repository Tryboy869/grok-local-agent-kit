#!/usr/bin/env python3
"""Ready compound agent demo (v0.62).

Demonstrates improved offline routing that chains tools:
calculate a value then save the result to a file — fully offline.
Also shows read-back and multi-LLM probes.

Usage:
  python examples/ready_compound_agent.py
"""

from __future__ import annotations

from pathlib import Path

from grok_local_agent_kit import __version__
from grok_local_agent_kit.mvp import probe_providers, run_mvp


def main() -> None:
    print(f"⚡ grok-local-agent-kit Ready Compound Agent (v{__version__})")
    print("Math → file write chaining + read-back. Fully offline.\n")

    workspace = Path(".grok/compound-demo")
    workspace.mkdir(parents=True, exist_ok=True)

    print("=== Multi-LLM provider probes ===")
    probes = probe_providers()
    for name, info in probes.items():
        print(f"  {name}: {info.get('status', 'unknown')}")
    print()

    goals = [
        "what time is it?",
        "calculate 2**10 + 42 and save to result.txt",
        "read result.txt",
        "get system info",
        "write a summary note that the compound agent succeeded",
    ]

    for goal in goals:
        print(f"Goal: {goal}")
        result = run_mvp(
            goal,
            workspace,
            search=lambda q: f"[fixture] results for '{q}'",
        )
        intent = result.get("intent", "?")
        ok = result.get("ok", False)
        steps = len(result.get("steps") or [])
        answer = str(result.get("answer", "")).splitlines()[0][:120]
        print(f"  → intent={intent} steps={steps} ok={ok}")
        print(f"  → {answer}")
        print()

    print("✅ Compound agent demo complete.")
    print("Check artifacts in:", workspace.resolve())
    print("  - result.txt should contain the computed value")
    print("Next: attach Ollama/LM Studio for full ReAct, or try enhanced_core_agent.py")


if __name__ == "__main__":
    main()
