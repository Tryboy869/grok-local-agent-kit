"""CLI extras for v0.43 — declarative offline workflow runner."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v043", False):
        return

    from .cli_v042 import register as _reg042

    _reg042(cli)

    @cli.group("workflow")
    def workflow_grp():
        """Run a JSON workflow of file / search / MCP steps (no daemon)."""

    @workflow_grp.command("demo")
    def demo_cmd():
        """List, write, fixture search, MCP echo. No Ollama / LM Studio."""
        from .workflow import demo_workflow

        console.print(demo_workflow())

    @workflow_grp.command("run")
    @click.argument("path", type=click.Path(exists=True, dir_okay=False))
    @click.option("--workspace", default=".", show_default=True, help="Workspace root")
    def run_cmd(path, workspace):
        """Execute a workflow JSON file inside a workspace."""
        from .workflow import load_workflow, run_workflow
        import json

        result = run_workflow(load_workflow(path), workspace)
        console.print(json.dumps(result, indent=2, ensure_ascii=False))
        if not result["ok"]:
            raise SystemExit(1)

    cli._grok_v043 = True
