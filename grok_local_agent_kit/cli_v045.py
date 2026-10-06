"""CLI extras for v0.45 — offline MVP runner."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v045", False):
        return

    from .cli_v044 import register as _reg044

    _reg044(cli)

    @cli.command("mvp")
    @click.option("--workspace", default=".grok/mvp", show_default=True)
    def mvp_cmd(workspace: str):
        """Run the offline MVP: intent routing, file tools, search, provider table."""
        from pathlib import Path

        from .mvp import demo_mvp, probe_providers

        console.print(demo_mvp(Path(workspace)))
        probes = probe_providers()
        for name, row in probes.items():
            console.print(f"[dim]{name}: {row['status']} ({row['detail']})[/]")

    cli._grok_v045 = True
