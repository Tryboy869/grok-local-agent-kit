"""CLI extras for v0.38 — persist routed HealthBoard decisions."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v038", False):
        return

    from .cli_v037 import register as _reg037

    _reg037(cli)

    route_grp = None
    for cmd in getattr(cli, "commands", {}).values() if hasattr(cli, "commands") else []:
        if getattr(cmd, "name", None) == "route":
            route_grp = cmd
            break
    if route_grp is None:
        # click Group stores commands on cli.commands
        route_grp = cli.commands.get("route") if hasattr(cli, "commands") else None

    if route_grp is None:

        @cli.group("route")
        def route_grp():
            """Router + health board."""

    @route_grp.command("persist")
    @click.option("--path", default="health.json", show_default=True)
    def persist_cmd(path: str):
        """Write routed health decisions to health.json (fake clients, no LLM)."""
        from .router import demo_persisted_route

        console.print(demo_persisted_route(path))

    cli._grok_v038 = True
