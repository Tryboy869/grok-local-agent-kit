#!/usr/bin/env python3
"""Multi-agent orchestrator example.

Uses create_agent for planner + specialists. Pass --no-llm to only print roles.
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit import Orchestrator, create_agent
from grok_local_agent_kit.orchestrator import DEFAULT_ROLES


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("goal", nargs="?", default="Summarize this repo README in 5 bullets.")
    parser.add_argument("--no-llm", action="store_true")
    args = parser.parse_args()

    if args.no_llm:
        print("Roles:")
        for name, role in DEFAULT_ROLES.items():
            print(f"- {name}: {role.instruction}")
        print("\nGoal:", args.goal)
        return

    orch = Orchestrator(lambda: create_agent(use_router=True, verbose=False))
    print(orch.run(args.goal, specialists=["researcher", "operator"]))


if __name__ == "__main__":
    main()
