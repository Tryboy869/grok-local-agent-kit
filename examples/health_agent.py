#!/usr/bin/env python3
"""Offline circuit-breaker board for local LLM backends.

No model is contacted. Use this to decide whether Ollama / LM Studio
should receive traffic after repeated failures.
"""

from __future__ import annotations

import argparse

from grok_local_agent_kit.health import (
    demo_health,
    format_board,
    load_board,
    save_board,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Health board (no LLM)")
    parser.add_argument("--path", default="health.json")
    parser.add_argument("--demo", action="store_true", help="run the canned story")
    parser.add_argument("--trip", default="", help="force a backend open")
    parser.add_argument("--reset", default="", help="close a backend")
    args = parser.parse_args()

    if args.demo:
        print(demo_health(args.path))
        return

    board = load_board(args.path)
    if args.trip:
        board.trip(args.trip, error="cli trip")
        save_board(board, args.path)
    if args.reset:
        board.reset(args.reset)
        save_board(board, args.path)
    print(format_board(board))


if __name__ == "__main__":
    main()
