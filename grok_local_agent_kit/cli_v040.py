"""CLI extras for v0.40 — local model catalog."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v040", False):
        return

    from .cli_v039 import register as _reg039

    _reg039(cli)

    @cli.group("models")
    def models_grp():
        """Discover local Ollama / LM Studio models."""

    @models_grp.command("demo")
    @click.option("--path", default="catalog.json", show_default=True)
    def demo_cmd(path: str):
        from .catalog import demo_catalog

        console.print(demo_catalog(path))

    @models_grp.command("list")
    def list_cmd():
        from .catalog import format_catalog

        console.print(format_catalog())

    @models_grp.command("refresh")
    @click.option("--path", default="catalog.json", show_default=True)
    def refresh_cmd(path: str):
        from .catalog import write_catalog

        dest = write_catalog(path)
        console.print(f"wrote={dest}")

    cli._grok_v040 = True
