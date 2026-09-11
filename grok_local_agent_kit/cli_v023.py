"""CLI extras for sqlite-vec / vector backend (v0.23)."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v023", False):
        return

    @cli.command("vec")
    @click.argument("action", type=click.Choice(["info", "search", "remember"]))
    @click.option("--query", default="", help="Text to embed / search.")
    @click.option("--limit", default=5, type=int)
    def vec_cmd(action, query, limit):
        """Inspect the vector backend or run a local KNN search."""
        from .sqlite_vec_store import describe, knn
        from .vector_memory import vremember

        if action == "info":
            console.print(describe())
            return
        if action == "remember":
            if not query.strip():
                console.print("pass --query TEXT")
                return
            console.print(vremember(query))
            return
        if not query.strip():
            console.print("pass --query TEXT")
            return
        rows = knn(query, limit=limit)
        if not rows:
            console.print("no notes")
            return
        for score, rid, ts, text, tags in rows:
            tag = f" [{tags}]" if tags else ""
            console.print(f"#{rid} {score:.3f} {ts}{tag}: {text}")

    cli._grok_v023 = True
