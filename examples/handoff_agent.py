#!/usr/bin/env python3
"""LLM-free task handoff on the shared blackboard.

    python examples/handoff_agent.py
    python examples/handoff_agent.py --sqlite
"""

from __future__ import annotations

import argparse
from pathlib import Path

from grok_local_agent_kit.handoff import HandoffQueue, load_queue, save_queue
from grok_local_agent_kit.persist import save_board
from grok_local_agent_kit.team import Blackboard


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("title", nargs="?", default="Document the local handoff queue.")
    parser.add_argument("--path", default="handoff.json")
    parser.add_argument("--sqlite", action="store_true")
    args = parser.parse_args()

    path = "handoff.sqlite" if args.sqlite else args.path
    board = Blackboard()
    q = load_queue(path, board=board) if Path(path).exists() else HandoffQueue(board=board)
    task = q.offer(args.title, owner="coordinator")
    q.claim(task.id, "operator")
    q.complete(task.id, note="offline complete")
    print(q.dump())
    print("---")
    print(board.dump())
    dest = save_queue(q, path)
    save_board(board, "board.jsonl")
    print(f"saved {dest}")


if __name__ == "__main__":
    main()
