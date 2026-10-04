"""CLI extras for v0.44 — file-backed job ledger."""

from __future__ import annotations

import json

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v044", False):
        return

    from .cli_v043 import register as _reg043

    _reg043(cli)

    @cli.group("jobs")
    def jobs_grp():
        """Run due workflow jobs from a JSON ledger (no daemon)."""

    @jobs_grp.command("demo")
    def demo_cmd():
        """Fire one digest job, then show the second tick is a no-op."""
        from .jobs import demo_jobs

        console.print(demo_jobs())

    @jobs_grp.command("tick")
    @click.argument("path", type=click.Path(exists=True, dir_okay=False))
    @click.option("--workspace", default=".", show_default=True)
    @click.option("--now", type=float, default=None, help="Unix seconds. Default: current time.")
    def tick_cmd(path, workspace, now):
        """Run due jobs and persist jobs-state.json beside the ledger."""
        import time

        from .jobs import load_ledger, tick

        ledger = load_ledger(path)
        result = tick(ledger, workspace, now=time.time() if now is None else now, persist=True)
        console.print(json.dumps(result, indent=2))
        if not result["ok"]:
            raise SystemExit(1)

    cli._grok_v044 = True
