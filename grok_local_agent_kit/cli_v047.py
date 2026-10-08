"""CLI extras for v0.47 — opt-in ReAct handoff execution."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v047", False):
        return

    from .cli_v046 import register as _reg046

    _reg046(cli)

    @cli.command("handoff")
    @click.argument("action", default="demo")
    @click.option("--workspace", default=".grok/handoff", show_default=True)
    @click.option("--live", is_flag=True, help="Call Agent.run when a provider probe is up.")
    def handoff_cmd(action: str, workspace: str, live: bool):
        """Run the playbook and call ReAct when a provider is up.

        demo uses an offline stand-in. live probes Ollama / LM Studio and
        calls the agent only if one is up.
        """
        from pathlib import Path

        from .playbook import demo_react, format_report, probe_providers, run_playbook, builtin_playbook

        root = Path(workspace)
        if action == "demo" and not live:
            console.print(demo_react(root))
            console.print(f"[dim]report: {(root / 'playbook-report.json').resolve()}[/]")
            return
        if action in {"demo", "live"} or live:
            probes = probe_providers(timeout=0.4)
            report = run_playbook(builtin_playbook(), root, probes=probes, live=True)
            console.print(format_report(report))
            console.print(f"[dim]react_called={report['react_called']}[/]")
            return
        raise click.UsageError("action must be demo or live")

    cli._grok_v047 = True
