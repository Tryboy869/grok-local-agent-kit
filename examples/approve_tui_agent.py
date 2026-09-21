#!/usr/bin/env python3
"""Decide pending approvals without a live LLM.

    python examples/approve_tui_agent.py
    python examples/approve_tui_agent.py --script A003=approved,A004=denied
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit.approve_tui import demo_tui, persist_scripted


def main() -> None:
    p = argparse.ArgumentParser(description="Scriptable approval TUI demo")
    p.add_argument("--path", default="approvals.json")
    p.add_argument("--script", default="A003=approved,A004=denied")
    p.add_argument("--policy", default="", choices=["", "approve-all", "deny-all"])
    args = p.parse_args()
    print(demo_tui())
    print("--- persist ---")
    print(persist_scripted(args.path, script=args.script, policy=args.policy, seed=True))


if __name__ == "__main__":
    main()
