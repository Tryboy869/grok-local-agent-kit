"""CLI extras for v0.34 — scriptable approval TUI."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v034", False):
        return

    from .cli_v033 import register as _reg033

    _reg033(cli)
    approve_grp = None
    for cmd in getattr(cli, "commands", {}).values():
        if getattr(cmd, "name", None) == "approve":
            approve_grp = cmd
            break
    if approve_grp is None:

        @cli.group("approve")
        def approve_grp():
            """Local approvals."""

    @approve_grp.command("tui")
    @click.option("--path", default="approvals.json", show_default=True)
    @click.option("--script", default="", help="A003=approved,A004=denied")
    @click.option(
        "--policy",
        default="",
        type=click.Choice(["", "approve-all", "deny-all"]),
        help="Bulk decide every pending item",
    )
    @click.option("--seed", is_flag=True, help="Ignore existing file and seed a demo queue")
    def tui_cmd(path: str, script: str, policy: str, seed: bool):
        """Decide pending approvals (scriptable; no LLM)."""
        from .approve_tui import persist_scripted

        console.print(persist_scripted(path, script=script, policy=policy, seed=seed))

    @approve_grp.command("queue")
    @click.option("--path", default="approvals.json", show_default=True)
    @click.option("--seed", is_flag=True)
    def queue_cmd(path: str, seed: bool):
        """Print the pending queue."""
        from pathlib import Path

        from .approve_tui import format_queue, seed_pending_gate
        from .approvals import load_approvals, save_approvals

        if seed or not Path(path).exists():
            gate = seed_pending_gate()
            save_approvals(gate, path)
        else:
            gate = load_approvals(path)
        console.print(format_queue(gate))

    cli._grok_v034 = True
