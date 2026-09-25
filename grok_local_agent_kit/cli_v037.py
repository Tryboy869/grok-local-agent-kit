"""CLI extras for v0.37 — HealthBoard wired into MultiLLMRouter."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v037", False):
        return

    from .cli_v036 import register as _reg036

    _reg036(cli)

    @cli.group("route")
    def route_grp():
        """Router + health board (no live LLM required for demo)."""

    @route_grp.command("demo")
    def demo_cmd():
        """Show pick() skipping an open breaker."""
        from .router import demo_routed_health

        console.print(demo_routed_health())

    cli._grok_v037 = True
