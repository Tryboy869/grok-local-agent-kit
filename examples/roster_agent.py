#!/usr/bin/env python3
"""Persist a team roster (who the members are + optional LLM bindings).

No live LLM required unless you pass --llm (then Agent.run is used if present).

    python examples/roster_agent.py
    python examples/roster_agent.py --sqlite
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit.persist import load_board, save_board
from grok_local_agent_kit.roster import (
    MemberSpec,
    default_specs,
    format_roster,
    load_roster,
    save_roster,
    team_from_roster,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("goal", nargs="?", default="Resume a named local team from disk.")
    parser.add_argument("--path", default="roster.json")
    parser.add_argument("--sqlite", action="store_true")
    parser.add_argument("--rounds", type=int, default=1)
    args = parser.parse_args()

    path = "roster.sqlite" if args.sqlite else args.path
    specs = load_roster(path) if Path(path).exists() else default_specs()
    if not any(s.provider for s in specs):
        specs = [
            MemberSpec(
                name=s.name,
                instruction=s.instruction,
                provider="ollama" if s.name == "coordinator" else "",
                model="llama3.2" if s.name == "coordinator" else "",
                role=s.role or s.name,
            )
            for s in specs
        ]
    print(format_roster(specs))
    board = load_board("board.jsonl") if Path("board.jsonl").exists() else None
    team = team_from_roster(specs=specs, board=board)
    print(team.status())
    print(team.run(args.goal, rounds=args.rounds))
    dest = save_roster(specs, path)
    save_board(team.board, "board.jsonl")
    print(f"saved {dest} members={len(specs)}")


if __name__ == "__main__":
    main()
