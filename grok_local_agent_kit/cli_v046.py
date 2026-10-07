"""CLI extras for v0.46 — playbook runner and optional live handoff descriptor."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v046", False):
        return

    from .cli_v045 import register as _reg045

    _reg045(cli)

    @cli.command("playbook")
    @click.argument("action", default="demo")
    @click.argument("path", required=False)
    @click.option("--workspace", default=".grok/playbook", show_default=True)
    def playbook_cmd(action: str, path: str | None, workspace: str):
        """Run a local playbook (demo) or a JSON file (run PATH). No LLM required."""
        from pathlib import Path

        from .playbook import demo_playbook, format_report, load_playbook, run_playbook

        root = Path(workspace)
        if action == "demo":
            console.print(demo_playbook(root))
            console.print(f"[dim]report: {(root / 'playbook-report.json').resolve()}[/]")
            return
        if action == "run":
            if not path:
                raise click.UsageError("playbook run needs a JSON path")
            report = run_playbook(load_playbook(Path(path)), root)
            console.print(format_report(report))
            return
        raise click.UsageError("action must be demo or run")

    cli._grok_v046 = True
