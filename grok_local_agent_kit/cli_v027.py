"""CLI extras for v0.27 — LLM-free tools demo."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v027", False):
        return

    @cli.group("tools")
    def tools_grp():
        """Inspect or demo built-in tools without a live LLM."""

    @tools_grp.command("list")
    def list_cmd():
        from .tools import list_tools

        console.print(list_tools())

    @tools_grp.command("demo")
    def demo_cmd():
        from .tools import calculator, get_system_info, list_files, list_tools

        console.print("[bold]Built-in tools[/]")
        console.print(list_tools())
        console.print("\n[bold]calculator('21*2')[/]")
        console.print(calculator("21*2"))
        console.print("\n[bold]list_files('.')[/]")
        console.print(list_files("."))
        console.print("\n[bold]get_system_info()[/]")
        console.print(get_system_info())

    cli._grok_v027 = True
