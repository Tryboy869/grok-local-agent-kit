"""CLI extras for v0.28 — multi-agent team blackboard demo (no LLM)."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v028", False):
        return

    @cli.group("team")
    def team_grp():
        """Multi-agent team + shared blackboard."""

    @team_grp.command("demo")
    @click.option("--goal", default="Ship a local agent without an API key.")
    @click.option("--rounds", default=1, type=int)
    def demo_cmd(goal: str, rounds: int):
        from .team import Team

        team = Team()
        console.print(f"[bold]{team.status()}[/]")
        console.print(team.run(goal, rounds=rounds))

    @team_grp.command("status")
    def status_cmd():
        from .team import Team

        console.print(Team().status())

    cli._grok_v028 = True
