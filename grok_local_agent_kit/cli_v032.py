"""CLI extras for v0.32 — local approval gate."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v032", False):
        return

    @cli.group("approve")
    def approve_grp():
        """Request / decide local approvals (no LLM)."""

    @approve_grp.command("demo")
    @click.option("--path", default="approvals.json", show_default=True)
    def demo_cmd(path: str):
        from .approvals import demo_approvals, load_approvals, save_approvals

        text = demo_approvals()
        console.print(text)
        from .approvals import ApprovalGate

        gate = ApprovalGate(allow=["calculator"], deny=["shell"])
        gate.request("tool", "calculator", actor="demo")
        denied = gate.request("tool", "shell", actor="demo")
        pending = gate.request("handoff", "T001", actor="demo")
        gate.decide(pending.id, "approved")
        dest = save_approvals(gate, path)
        console.print(f"[green]saved[/] {dest} ({denied.status} shell, {pending.status} handoff)")

    @approve_grp.command("show")
    @click.argument("path", default="approvals.json")
    def show_cmd(path: str):
        from .approvals import load_approvals

        if not Path(path).exists():
            console.print(f"[yellow]missing[/] {path}")
            raise SystemExit(1)
        console.print(load_approvals(path).dump())

    cli._grok_v032 = True
