"""CLI extras for v0.33 — ApprovalGate inside the ReAct tool path."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v033", False):
        return

    from .cli_v032 import register as _reg032

    _reg032(cli)
    approve_grp = None
    for cmd in getattr(cli, "commands", {}).values():
        if getattr(cmd, "name", None) == "approve":
            approve_grp = cmd
            break
    if approve_grp is None:

        @cli.group("approve")
        def approve_grp():
            """Local approvals."""

    @approve_grp.command("react")
    @click.option("--path", default="approvals.json", show_default=True)
    def react_cmd(path: str):
        """Simulate a ReAct tool batch behind the gate (no LLM)."""
        from .approvals import ApprovalGate, save_approvals
        from .react_gate import gated_execute
        from .tools import execute_tool, get_default_tools

        _, funcs = get_default_tools()
        gate = ApprovalGate(
            allow=["calculator", "list_files"],
            deny=["run_shell", "shell"],
            default="pending",
        )

        def _run(name: str, args: dict) -> str:
            return gated_execute(gate, name, execute_tool, name, args, funcs)

        rows = [
            ("calculator", {"expression": "21*2"}),
            ("run_shell", {"command": "echo blocked"}),
            ("web_search", {"query": "local agents"}),
        ]
        for name, args in rows:
            result = _run(name, args)
            preview = result.replace("\n", " ")[:120]
            console.print(f"[bold]{name}[/] → {preview}")
        dest = save_approvals(gate, path)
        console.print(f"[green]saved[/] {dest}")

    cli._grok_v033 = True
