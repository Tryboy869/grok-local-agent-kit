"""Extra CLI commands registered on import."""

from __future__ import annotations

import os

import click
from rich.console import Console

console = Console()


def register(cli) -> None:
    if getattr(cli, "_grok_ext", False):
        return

    @cli.command("init")
    @click.option("--path", default="grok-agent.toml", help="Where to write the sample config")
    def init_config(path):
        """Write a starter grok-agent.toml in the current directory."""
        from .config import write_example_config

        dest = write_example_config(path)
        console.print(f"[green]Wrote[/] {dest.resolve()}")

    @cli.command("tools")
    def tools_cmd():
        """List built-in tools (no LLM required)."""
        from .tools import list_tools as _lt

        console.print(_lt())

    @cli.command("mcp-http")
    @click.argument("url")
    def mcp_http_cmd(url):
        """Probe an MCP HTTP JSON-RPC endpoint."""
        from .mcp_http import probe_http_mcp

        console.print(probe_http_mcp(url))

    @cli.command("mcp-sse")
    @click.argument("url")
    def mcp_sse_cmd(url):
        """Probe an MCP Streamable HTTP / SSE endpoint with retries."""
        from .mcp_sse import probe_sse_mcp

        console.print(probe_sse_mcp(url))

    @cli.command("vmemory")
    @click.argument("action", type=click.Choice(["remember", "recall", "forget", "stats"]))
    @click.argument("text", required=False, default="")
    def vmemory_cmd(action, text):
        """SQLite vector memory helpers (.grok/memory/vectors.db)."""
        from . import vector_memory as vm

        if action == "remember":
            console.print(vm.vremember(text))
        elif action == "recall":
            console.print(vm.vrecall(text))
        elif action == "forget":
            console.print(vm.vforget(text))
        else:
            console.print(vm.vstats())

    @cli.command("embed-probe")
    @click.argument("text", required=False, default="local agent kit")
    def embed_probe_cmd(text):
        """Show embedding backend + vector length (no LLM)."""
        from .embeddings import backend_name, embed

        vec = embed(text)
        console.print(f"backend={backend_name()} dim={len(vec)} sample={vec[:4]}")

    @cli.command("trace")
    @click.option("--path", default=".grok/traces/last.json")
    def trace_cmd(path):
        """Print the last exported trace if present."""
        from pathlib import Path

        p = Path(path)
        if p.exists():
            console.print(p.read_text(encoding="utf-8")[:4000])
        else:
            console.print(
                "No trace file yet. After a run call agent.export_trace() "
                "or use examples/parallel_agent.py. Default path: .grok/traces/last.json"
            )

    @cli.command("replay")
    @click.option("--path", default=".grok/traces/last.json")
    @click.option("--run", is_flag=True, help="Re-execute tools found in the trace")
    def replay_cmd(path, run):
        """Summarize (and optionally re-run) an exported ReAct trace."""
        from pathlib import Path

        from .replay import replay_file, summarize_trace, load_trace

        p = Path(path)
        if not p.exists():
            console.print(f"[yellow]No trace at {p}. Try examples/replay_agent.py[/]")
            return
        if run:
            report = replay_file(p, dry_run=False)
            console.print(report["summary"])
            console.print(report["tools"])
        else:
            console.print(summarize_trace(load_trace(p)))

    @cli.command("serve")
    @click.option("--host", default="127.0.0.1", help="Bind address (default loopback)")
    @click.option("--port", default=8765, type=int)
    @click.option("--router", is_flag=True, help="Enable MultiLLMRouter fallback")
    @click.option("--token", default=lambda: os.environ.get("GROK_AGENT_SERVE_TOKEN", ""), help="Optional bearer token")
    def serve_cmd(host, port, router, token):
        """Run a local HTTP API: GET /health, POST /v1/chat."""
        from .factory import create_agent
        from .serve import run_forever

        def factory():
            return create_agent(use_router=router)

        run_forever(host, port, factory, token=token or None)

    @cli.command("plan")
    @click.argument("action", type=click.Choice(["add", "list", "done", "clear"]))
    @click.argument("text", required=False, default="")
    def plan_cmd(action, text):
        """Workspace planner stored in .grok/plan.json."""
        from . import planner as pl

        if action == "add":
            console.print(pl.plan_add(text))
        elif action == "list":
            console.print(pl.plan_list(text or "all"))
        elif action == "done":
            console.print(pl.plan_done(int(text or "0")))
        else:
            console.print(pl.plan_clear(done_only=True))

    cli._grok_ext = True
