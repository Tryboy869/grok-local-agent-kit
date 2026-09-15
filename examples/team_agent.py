#!/usr/bin/env python3
"""Multi-agent team with a shared blackboard.

Default path is LLM-free (deterministic handlers).
Pass --llm to wrap create_agent().run as each member handler.
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit.team import DEFAULT_MEMBERS, Member, Team


def _llm_handler(name: str, instruction: str):
    from grok_local_agent_kit import create_agent

    agent = create_agent(use_router=True, verbose=False)

    def _fn(board, goal: str) -> str:
        prompt = (
            f"You are team member '{name}'. {instruction}\n"
            f"Goal: {goal}\n\nBlackboard:\n{board.dump(16)}\n\n"
            "Do your part in 4 sentences or less. Do not repeat the whole board."
        )
        return agent.run(prompt)

    return _fn


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("goal", nargs="?", default="Explain how to run this kit offline.")
    parser.add_argument("--llm", action="store_true", help="Wire each member to create_agent().")
    parser.add_argument("--rounds", type=int, default=1)
    args = parser.parse_args()

    if args.llm:
        members = [
            Member(m.name, m.instruction, _llm_handler(m.name, m.instruction))
            for m in DEFAULT_MEMBERS.values()
        ]
        team = Team(members=members)
    else:
        team = Team()

    print(team.status())
    print(team.run(args.goal, rounds=args.rounds))


if __name__ == "__main__":
    main()
