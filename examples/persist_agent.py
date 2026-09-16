#!/usr/bin/env python3
"""Persist a team blackboard to JSONL (default) or SQLite.

No live LLM required.

    python examples/persist_agent.py
    python examples/persist_agent.py --sqlite board.sqlite
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit.persist import load_board, save_board
from grok_local_agent_kit.team import Team


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("goal", nargs="?", default="Remember this team run on disk.")
    parser.add_argument("--path", default="board.jsonl")
    parser.add_argument("--sqlite", action="store_true", help="Write board.sqlite instead.")
    parser.add_argument("--rounds", type=int, default=1)
    args = parser.parse_args()

    path = "board.sqlite" if args.sqlite else args.path
    board = load_board(path) if Path(path).exists() else None
    team = Team(board=board)
    print(team.status())
    print(team.run(args.goal, rounds=args.rounds))
    dest = save_board(team.board, path)
    print(f"saved {dest} posts={len(team.board)}")


if __name__ == "__main__":
    main()
