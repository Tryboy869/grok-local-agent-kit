#!/usr/bin/env python3
"""Ready-to-run multi-tool offline agent demo.

Chains several intents: datetime, math, files, search (fixture), system.
Fully offline — no LLM or network required.
"""
from __future__ import annotations

from pathlib import Path
import tempfile

from grok_local_agent_kit.mvp import run_mvp, probe_providers


def main() -> None:
    print("=== Ready Multi-Tool Agent (offline) ===")
    probes = probe_providers()
    print("Multi-LLM probes:", {k: v["status"] for k, v in probes.items()})

    with tempfile.TemporaryDirectory() as tmp:
        ws = Path(tmp)
        goals = [
            "what time is it now",
            "compute sqrt(16) * 3",
            "write a short note: multi-tool demo succeeded",
            "search local AI agents",
            "show system info",
        ]
        for g in goals:
            result = run_mvp(g, ws)
            print(f"\nGoal: {g}")
            print(f"  intent={result['intent']} ok={result['ok']}")
            ans = result['answer']
            print(f"  answer: {ans[:200].strip()}{'...' if len(ans)>200 else ''}")
    print("\nMulti-tool demo complete. Offline-first.")


if __name__ == "__main__":
    main()
