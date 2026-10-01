"""CLI extras for v0.42 — offline scripted agent loop."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v042", False):
        return

    from .cli_v041 import register as _reg041

    _reg041(cli)

    @cli.group("offline")
    def offline_grp():
        """Run the real tool loop with a scripted LLM (no daemon)."""

    @offline_grp.command("demo")
    def demo_cmd():
        """List files, then write a note. No Ollama / LM Studio."""
        from .offline import demo_offline

        console.print(demo_offline())

    cli._grok_v042 = True
