"""CLI extras for workspace packer / file RAG (v0.26)."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v026", False):
        return

    @cli.group("workspace")
    def workspace_grp():
        """Pack or search the current workspace (cwd-safe)."""

    @workspace_grp.command("pack")
    @click.option("--path", default=".", show_default=True)
    def pack_cmd(path: str):
        from .workspace import pack_workspace

        console.print(pack_workspace(path))

    @workspace_grp.command("search")
    @click.argument("query")
    @click.option("--path", default=".", show_default=True)
    @click.option("--top-k", default=5, show_default=True)
    def search_cmd(query: str, path: str, top_k: int):
        from .workspace import search_workspace

        console.print(search_workspace(query, path=path, top_k=top_k))

    cli._grok_v026 = True
