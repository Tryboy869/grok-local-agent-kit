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

    @cli.command("mcp-sse")
    @click.argument("url")
    def mcp_sse_cmd(url):
        """Probe an MCP Streamable HTTP / SSE endpoint with retries."""
        from .mcp_sse import probe_sse_mcp

        console.print(probe_sse_mcp(url))

    @cli.command("vmemory")
    @click.argument("action", type=click.Choice(["remember", "recall", "forget", "stats"]))
    @click.argument("text", required=False, default="")
    def vmemory_cmd(action, text):
        """SQLite vector memory helpers (.grok/memory/vectors.db)."""
        from . import vector_memory as vm

        if action == "remember":
            console.print(vm.vremember(text))
        elif action == "recall":
            console.print(vm.vrecall(text))
        elif action == "forget":
            console.print(vm.vforget(text))
        else:
            console.print(vm.vstats())

    @cli.command("embed-probe")
    @click.argument("text", required=False, default="local agent kit")
    def embed_probe_cmd(text):
        """Show embedding backend + vector length (no LLM)."""
        from .embeddings import backend_name, embed

        vec = embed(text)
        console.print(f"backend={backend_name()} dim={len(vec)} sample={vec[:4]}")

    cli._grok_ext = True
