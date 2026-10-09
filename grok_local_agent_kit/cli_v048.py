"""CLI extras for v0.48 — session pack brief."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v048", False):
        return

    from .cli_v047 import register as _reg047

    _reg047(cli)

    @cli.command("pack")
    @click.argument("action", default="demo")
    @click.option("--workspace", default=".grok/pack", show_default=True)
    @click.option("--file", "pack_file", default=None, help="JSON pack of goals.")
    @click.option("--probe", is_flag=True, help="Probe Ollama and LM Studio (non-fatal).")
    def pack_cmd(action: str, workspace: str, pack_file: str | None, probe: bool):
        """Run a batch of offline goals and write SESSION.md.

        demo uses the built-in chat, automation, search, and MCP goals.
        run requires --file.
        """
        from pathlib import Path

        from .pack import DEFAULT_GOALS, format_brief, load_pack, run_pack

        root = Path(workspace)
        if action == "demo":
            report = run_pack(DEFAULT_GOALS, root, probe=probe)
        elif action == "run":
            if not pack_file:
                raise click.UsageError("pack run requires --file")
            report = run_pack(load_pack(Path(pack_file)), root, probe=probe)
        else:
            raise click.UsageError("action must be demo or run")
        console.print(format_brief(report))
        console.print(f"[dim]brief: {(root / 'SESSION.md').resolve()}[/]")

    cli._grok_v048 = True
