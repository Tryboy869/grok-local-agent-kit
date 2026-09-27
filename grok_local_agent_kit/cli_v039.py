"""CLI extras for v0.39 — kit snapshot."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v039", False):
        return

    from .cli_v038 import register as _reg038

    _reg038(cli)

    @cli.group("snapshot")
    def snapshot_grp():
        """Dump a portable kit snapshot (no live LLM)."""

    @snapshot_grp.command("demo")
    @click.option("--path", default="kit-snapshot.json", show_default=True)
    def demo_cmd(path: str):
        from .snapshot import demo_snapshot

        console.print(demo_snapshot(path))

    @snapshot_grp.command("show")
    def show_cmd():
        from .snapshot import format_snapshot

        console.print(format_snapshot())

    @snapshot_grp.command("write")
    @click.option("--path", default="kit-snapshot.json", show_default=True)
    def write_cmd(path: str):
        from .snapshot import write_snapshot

        dest = write_snapshot(path)
        console.print(f"wrote={dest}")

    cli._grok_v039 = True
