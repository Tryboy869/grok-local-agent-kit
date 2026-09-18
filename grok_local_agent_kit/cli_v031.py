"""CLI extras for v0.31 — task handoff queue."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_v031", False):
        return

    @cli.group("handoff")
    def handoff_grp():
        """Offer / claim / complete tasks on a local queue (no LLM)."""

    @handoff_grp.command("demo")
    @click.option("--goal", default="Ship a local handoff without a cloud queue.")
    @click.option("--path", default="handoff.json", show_default=True)
    def demo_cmd(goal: str, path: str):
        from .handoff import demo_handoff, load_queue, save_queue
        from .persist import save_board
        from .team import Blackboard

        board = Blackboard()
        text = demo_handoff(goal)
        console.print(text)
        q = load_queue(path, board=board) if Path(path).exists() else None
        if q is None:
            from .handoff import HandoffQueue

            q = HandoffQueue(board=board)
            q.offer(goal, owner="coordinator")
            t = q.offer("demo follow-up", owner="coordinator")
            q.claim(t.id, "operator")
            q.complete(t.id)
        dest = save_queue(q, path)
        save_board(board, "board.jsonl")
        console.print(f"[green]saved[/] {dest}")

    @handoff_grp.command("show")
    @click.argument("path", default="handoff.json")
    def show_cmd(path: str):
        from .handoff import load_queue

        if not Path(path).exists():
            console.print(f"[yellow]missing[/] {path}")
            raise SystemExit(1)
        console.print(load_queue(path).dump())

    cli._grok_v031 = True
