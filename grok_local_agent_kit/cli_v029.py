"""CLI extras for v0.29 — persist team blackboard to JSONL or SQLite."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v029", False):
        return

    @cli.group("board")
    def board_grp():
        """Save / load a team blackboard (JSONL or SQLite)."""

    @board_grp.command("demo")
    @click.option("--goal", default="Persist a local team blackboard.")
    @click.option("--path", default="board.jsonl", show_default=True)
    @click.option("--rounds", default=1, type=int)
    def demo_cmd(goal: str, path: str, rounds: int):
        from .persist import load_board, save_board
        from .team import Team

        board = load_board(path) if Path(path).exists() else None
        team = Team(board=board)
        console.print(f"[bold]{team.status()}[/]")
        console.print(team.run(goal, rounds=rounds))
        dest = save_board(team.board, path)
        console.print(f"[green]saved[/] {dest} ({len(team.board)} posts)")

    @board_grp.command("show")
    @click.argument("path", default="board.jsonl")
    def show_cmd(path: str):
        from .persist import load_board

        if not Path(path).exists():
            console.print(f"[yellow]missing[/] {path}")
            raise SystemExit(1)
        board = load_board(path)
        console.print(board.dump())

    cli._grok_v029 = True
