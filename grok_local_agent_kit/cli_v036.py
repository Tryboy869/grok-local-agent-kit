"""CLI extras for v0.36 — LLM backend circuit breaker / health board."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v036", False):
        return

    from .cli_v035 import register as _reg035

    _reg035(cli)

    @cli.group("health")
    def health_grp():
        """Circuit breaker board for local LLM backends."""

    @health_grp.command("demo")
    @click.option("--path", default="health.json", help="cwd-safe JSON path")
    def demo_cmd(path: str):
        """Run the offline health story and persist the board."""
        from .health import demo_health

        console.print(demo_health(path))

    @health_grp.command("show")
    @click.option("--path", default="health.json", help="cwd-safe JSON path")
    def show_cmd(path: str):
        """Print a persisted health board."""
        from .health import format_board, load_board

        console.print(format_board(load_board(path)))

    @health_grp.command("trip")
    @click.argument("name")
    @click.option("--path", default="health.json")
    @click.option("--error", default="manual trip")
    def trip_cmd(name: str, path: str, error: str):
        """Force a backend open."""
        from .health import format_board, load_board, save_board

        board = load_board(path)
        board.trip(name, error=error)
        save_board(board, path)
        console.print(format_board(board))

    @health_grp.command("reset")
    @click.argument("name")
    @click.option("--path", default="health.json")
    def reset_cmd(name: str, path: str):
        """Close a breaker and clear failures."""
        from .health import format_board, load_board, save_board

        board = load_board(path)
        board.reset(name)
        save_board(board, path)
        console.print(format_board(board))

    cli._grok_v036 = True
