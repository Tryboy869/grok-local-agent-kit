"""Extra CLI commands registered on import."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_ext", False):
        return

    @cli.command("init")
    @click.option("--path", default="grok-agent.toml", help="Where to write the sample config")
    def init_config(path):
        """Write a starter grok-agent.toml in the current directory."""
        from .config import write_example_config

        dest = write_example_config(path)
        console.print(f"[green]Wrote[/] {dest.resolve()}")

    @cli.command("tools")
    def tools_cmd():
        """List built-in tools (no LLM required)."""
        from .tools import list_tools as _lt

        console.print(_lt())

    @cli.command("mcp-http")
    @click.argument("url")
    def mcp_http_cmd(url):
        """Probe an MCP HTTP JSON-RPC endpoint."""
        from .mcp_http import probe_http_mcp

        console.print(probe_http_mcp(url))

    cli._grok_ext = True
