"""CLI extras for tool budgets (v0.22)."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v022", False):
        return

    @cli.command("budget")
    @click.argument("action", type=click.Choice(["stats", "reset", "off", "on", "set"]))
    @click.option("--max", "max_calls", type=int, default=None, help="Global cap for `set`.")
    def budget_cmd(action, max_calls):
        """Inspect or reset the in-process tool-call budget."""
        from .budget import get_budget, ToolBudget, set_budget

        b = get_budget()
        if action == "reset":
            b.reset()
            console.print("budget counters reset")
        elif action == "off":
            b.enabled = False
            console.print("budget disabled")
        elif action == "on":
            b.enabled = True
            console.print("budget enabled")
        elif action == "set":
            if max_calls is None:
                console.print("pass --max N")
                return
            set_budget(ToolBudget(max_calls=max_calls, per_tool=b.per_tool, enabled=True))
            console.print(f"budget max_calls={max_calls}")
        else:
            console.print(b.stats())

    cli._grok_v022 = True
