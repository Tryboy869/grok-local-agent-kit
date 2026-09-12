"""CLI extras for the plugin sandbox (v0.25)."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v025", False):
        return

    @cli.command("sandbox")
    @click.argument("action", type=click.Choice(["status", "skipped"]))
    def sandbox_cmd(action):
        """Show Python plugin sandbox policy."""
        from .plugins import discover_plugins, py_plugin_allowlist, py_plugins_allowed, skipped_py_plugins

        if action == "status":
            console.print(f"allow_py={py_plugins_allowed()}")
            allow = sorted(py_plugin_allowlist())
            console.print(f"allowlist={allow or '(empty)'}")
            console.print("hint: set GROK_AGENT_ALLOW_PY_PLUGINS=1 or GROK_AGENT_PY_PLUGIN_ALLOWLIST=stem")
            return
        discover_plugins()
        skipped = skipped_py_plugins()
        if not skipped:
            console.print("no skipped python plugins")
            return
        for path in skipped:
            console.print(str(path))

    cli._grok_v025 = True
