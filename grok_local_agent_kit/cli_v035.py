"""CLI extras for v0.35 — opt-in live-model eval profile."""

from __future__ import annotations

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v035", False):
        return

    from .cli_v034 import register as _reg034

    _reg034(cli)

    eval_grp = None
    for cmd in getattr(cli, "commands", {}).values():
        if getattr(cmd, "name", None) == "eval":
            eval_grp = cmd
            break
    if eval_grp is None:

        @cli.group("eval")
        def eval_grp():
            """Offline + opt-in live eval."""

    @eval_grp.command("live")
    @click.option("--profile", "profile_path", default="", help="JSON profile path")
    @click.option(
        "--live",
        is_flag=True,
        help="Hit a real LLM. Also requires GROK_LIVE_EVAL=1",
    )
    def live_cmd(profile_path: str, live: bool):
        """Run the smoke live-eval profile (stub unless opted in)."""
        from .live_eval import DEFAULT_PROFILE, format_live_report, load_profile, run_profile

        profile = load_profile(profile_path) if profile_path else DEFAULT_PROFILE
        report = run_profile(profile, live=live)
        console.print(format_live_report(report))
        if not report["ok"]:
            raise SystemExit(1)

    @eval_grp.command("demo")
    def demo_cmd():
        """Print the stub live-eval report (no LLM)."""
        from .live_eval import demo_live_eval

        console.print(demo_live_eval())

    cli._grok_v035 = True
