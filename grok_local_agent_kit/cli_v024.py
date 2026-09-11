"""CLI extras for plugins and transcripts (v0.24)."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v024", False):
        return

    @cli.command("plugins")
    @click.argument("action", type=click.Choice(["list", "dirs"]))
    def plugins_cmd(action):
        """List discovered drop-in tool plugins."""
        from .plugins import discover_plugins, plugin_dirs

        if action == "dirs":
            for d in plugin_dirs():
                mark = "ok" if d.exists() else "missing"
                console.print(f"{mark}\t{d}")
            return
        found = discover_plugins()
        if not found:
            console.print("no plugins found (put .json/.py in ./tools or ~/.grok-agent/tools)")
            return
        for name, spec, _fn in found:
            desc = spec["function"].get("description", "")
            console.print(f"{name}\t{desc}")

    @cli.command("transcripts")
    @click.argument("action", type=click.Choice(["list", "show", "new"]))
    @click.option("--path", default="", help="Transcript JSONL path.")
    @click.option("--session", default="chat")
    def transcripts_cmd(action, path, session):
        """Local JSONL conversation transcripts."""
        from pathlib import Path
        from . import transcripts as tr

        if action == "new":
            p = tr.new_path(session)
            console.print(str(p))
            return
        if action == "list":
            items = tr.list_transcripts()
            if not items:
                console.print("no transcripts")
                return
            for p in items[:30]:
                console.print(tr.summarize(p))
            return
        target = Path(path) if path else (tr.list_transcripts() or [None])[0]
        if target is None:
            console.print("no transcripts")
            return
        for row in tr.read_transcript(target):
            console.print(f"{row.get('role')}: {row.get('content', '')[:200]}")

    cli._grok_v024 = True
