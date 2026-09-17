"""CLI extras for v0.30 — persist team roster + optional LLM bindings."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v030", False):
        return

    @cli.group("roster")
    def roster_grp():
        """Save / load a team roster (JSON or SQLite) with optional LLM bindings."""

    @roster_grp.command("demo")
    @click.option("--goal", default="Bind a local roster and run one offline round.")
    @click.option("--path", default="roster.json", show_default=True)
    @click.option("--rounds", default=1, type=int)
    @click.option("--llm", is_flag=True, help="Wire live Agent.run if a model is listed.")
    def demo_cmd(goal: str, path: str, rounds: int, llm: bool):
        from .persist import load_board, save_board
        from .roster import (
            bind_roster,
            default_specs,
            format_roster,
            load_roster,
            save_roster,
            team_from_roster,
        )

        specs = load_roster(path) if Path(path).exists() else default_specs()
        if not any(s.provider for s in specs):
            specs[0].provider = "ollama"
            specs[0].model = "llama3.2"
        console.print(format_roster(specs))
        board_path = "board.jsonl"
        board = load_board(board_path) if Path(board_path).exists() else None
        if llm:
            members = bind_roster(specs, live=True)
            from .team import Team

            team = Team(members=members, board=board)
        else:
            team = team_from_roster(specs=specs, board=board)
        console.print(f"[bold]{team.status()}[/]")
        console.print(team.run(goal, rounds=rounds))
        dest = save_roster(specs, path)
        save_board(team.board, board_path)
        console.print(f"[green]saved[/] {dest} members={len(specs)} board={board_path}")

    @roster_grp.command("show")
    @click.argument("path", default="roster.json")
    def show_cmd(path: str):
        from .roster import format_roster, load_roster

        if not Path(path).exists():
            console.print(f"[yellow]missing[/] {path}")
            raise SystemExit(1)
        console.print(format_roster(load_roster(path)))

    cli._grok_v030 = True
