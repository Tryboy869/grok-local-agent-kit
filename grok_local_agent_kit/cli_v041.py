"""CLI extras for v0.41 — catalog-aware router defaults."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v041", False):
        return

    from .cli_v040 import register as _reg040

    _reg040(cli)

    route_grp = None
    commands = getattr(cli, "commands", {}) or {}
    route_grp = commands.get("route")
    if route_grp is None:

        @cli.group("route")
        def route_grp():
            """Router + health board + catalog."""

    @route_grp.command("catalog")
    @click.option("--prefer", default="llama3.2", show_default=True)
    def catalog_cmd(prefer: str):
        """Rewrite router models from Catalog.pick (no live LLM)."""
        from .catalog_route import demo_catalog_route

        console.print(demo_catalog_route(prefer=prefer))

    cli._grok_v041 = True
