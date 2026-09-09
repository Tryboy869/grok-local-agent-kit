"""CLI extras for cache + telemetry."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v021", False):
        return

    @cli.command("cache")
    @click.argument("action", type=click.Choice(["stats", "clear", "off", "on"]))
    def cache_cmd(action):
        """Inspect or reset the in-process tool cache."""
        from .cache import get_cache

        cache = get_cache()
        if action == "clear":
            n = cache.clear()
            console.print(f"cleared {n} entries")
        elif action == "off":
            cache.enabled = False
            console.print("cache disabled")
        elif action == "on":
            cache.enabled = True
            console.print("cache enabled")
        else:
            console.print(cache.stats())

    @cli.command("telemetry")
    @click.argument("action", type=click.Choice(["stats", "clear"]), default="stats")
    def telemetry_cmd(action):
        """Show tool latency / cache-hit telemetry."""
        from .telemetry import get_telemetry

        tel = get_telemetry()
        if action == "clear":
            console.print(f"cleared {tel.clear()} events")
        else:
            console.print(tel.summary())

    cli._grok_v021 = True
