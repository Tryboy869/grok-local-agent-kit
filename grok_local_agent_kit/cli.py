"""CLI entrypoint: grok-agent"""

from __future__ import annotations

import os

import click
from rich.console import Console
from rich.markdown import Markdown

from . import __version__
from .factory import create_agent

console = Console()


def _env_default(key: str, fallback: str) -> str:
    return os.environ.get(key, fallback)


@click.group()
@click.version_option(version=__version__, prog_name="grok-agent")
def cli() -> None:
    """Grok Local Agent Kit — local AI agents with tools."""
    pass


@cli.command()
@click.argument("prompt", required=False)
@click.option("-m", "--model", default=lambda: _env_default("GROK_AGENT_MODEL", "llama3.2"), help="Model name")
@click.option("-p", "--provider", default=lambda: _env_default("GROK_AGENT_PROVIDER", "ollama"), type=click.Choice(["ollama", "lmstudio", "openai"]), help="LLM provider")
@click.option("--base-url", default=lambda: os.environ.get("GROK_AGENT_BASE_URL"), help="Custom base URL")
@click.option("--verbose", "-v", is_flag=True, help="Show tool calls and stream tokens")
@click.option("--stream", is_flag=True, help="Stream final answer tokens")
@click.option("--save-history", default=None, help="Save conversation history JSON on exit")
@click.option("--session", default=None, help="Named session under .grok/sessions/")
@click.option("--attach-mcp", is_flag=True, help="Auto-register discovered MCP tools")
@click.option("--router", is_flag=True, help="Enable MultiLLMRouter fallback")
def chat(prompt, model, provider, base_url, verbose, stream, save_history, session, attach_mcp, router):
    """Interactive chat or one-shot prompt."""
    agent = create_agent(
        model=model,
        provider=provider,
        base_url=base_url,
        verbose=verbose,
        stream=stream or verbose,
        session_name=session or "default",
        attach_mcp=attach_mcp,
        use_router=router,
    )
    if session:
        loaded = agent.load_named_session(session)
        if verbose:
            console.print(f"[dim]{loaded}[/]")
    if prompt:
        result = agent.chat(prompt) if session else agent.run(prompt)
        console.print(Markdown(result))
        if save_history:
            console.print(agent.save_history(save_history))
        if session:
            console.print(agent.save_named_session(session))
        agent.close()
        return
    console.print(
        f"[bold green]Local Agent ready (v{__version__}).[/] Type 'exit' or Ctrl-C to quit.\n"
        "Special: /save /load /session /sessions /reset /tools /mcp /ping /attach-mcp\n"
    )
    try:
        while True:
            user = console.input("[bold cyan]You › [/]")
            stripped = user.strip()
            if stripped.lower() in {"exit", "quit", "q"}:
                break
            if not stripped:
                continue
            if stripped.startswith("/save"):
                parts = stripped.split(maxsplit=1)
                console.print(agent.save_history(parts[1] if len(parts) > 1 else "agent_history.json"))
                continue
            if stripped.startswith("/load"):
                parts = stripped.split(maxsplit=1)
                console.print(agent.load_history(parts[1] if len(parts) > 1 else "agent_history.json"))
                continue
            if stripped in {"/reset", "/clear"}:
                agent.reset()
                console.print("[yellow]History cleared.[/]")
                continue
            if stripped in {"/tools", "/list_tools"}:
                from .tools import list_tools as _lt
                console.print(_lt())
                continue
            if stripped in {"/mcp", "/mcp_status"}:
                from .mcp import get_manager
                console.print(get_manager().describe())
                continue
            if stripped in {"/ping"}:
                console.print(agent.llm.ping())
                continue
            if stripped.startswith("/session"):
                parts = stripped.split(maxsplit=1)
                if len(parts) == 1:
                    console.print(agent.list_named_sessions())
                    console.print(f"current: {agent.session_name}")
                else:
                    console.print(agent.load_named_session(parts[1]))
                continue
            if stripped in {"/sessions"}:
                console.print(agent.list_named_sessions())
                continue
            if stripped in {"/attach-mcp", "/attach_mcp"}:
                console.print(f"Attached: {agent.attach_mcp_tools() or '(none)'}")
                continue
            result = agent.chat(user)
            console.print()
            console.print(Markdown(result))
            console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\nBye!")
    finally:
        if save_history:
            console.print(agent.save_history(save_history))
        if session:
            console.print(agent.save_named_session(session))
        agent.close()


@cli.command()
@click.option("-m", "--model", default=lambda: _env_default("GROK_AGENT_MODEL", "llama3.2"))
@click.option("-p", "--provider", default=lambda: _env_default("GROK_AGENT_PROVIDER", "ollama"), type=click.Choice(["ollama", "lmstudio", "openai"]))
@click.option("--base-url", default=lambda: os.environ.get("GROK_AGENT_BASE_URL"))
def doctor(model, provider, base_url):
    """Check connectivity to local LLM and list available tools."""
    console.print(f"[bold]Checking {provider} / {model} ...[/]")
    agent = create_agent(model=model, provider=provider, base_url=base_url)
    try:
        status = agent.llm.ping()
        if status.startswith("ok"):
            console.print(f"[green]✓ LLM reachable:[/] {status}")
        else:
            console.print(f"[yellow]⚠ LLM status:[/] {status}")
        reply = agent.run("Reply with exactly: OK")
        console.print(f"[green]✓ LLM responded:[/] {reply[:120]}")
        tools = ", ".join(sorted(agent.tool_funcs.keys()))
        console.print(f"[green]✓ Tools registered ({len(agent.tool_funcs)}):[/] {tools}")
        console.print(f"[dim]Version {__version__}[/]")
    except Exception as e:
        console.print(f"[red]✗ Failed:[/] {e}")
    finally:
        agent.close()


@cli.command()
def route():
    """Probe Ollama then LM Studio and print the fallback chain."""
    from .router import MultiLLMRouter, format_probe

    router = MultiLLMRouter()
    try:
        console.print(format_probe(router.probe()))
        ep, _ = router.pick()
        console.print(f"[green]active:[/] {ep.name} / {ep.provider} / {ep.model}")
    finally:
        router.close()


@cli.command()
@click.argument("action", type=click.Choice(["remember", "recall", "forget", "stats"]))
@click.argument("text", required=False, default="")
def memory(action, text):
    """Local JSONL memory helpers (.grok/memory/notes.jsonl)."""
    from . import memory as mem

    if action == "remember":
        console.print(mem.remember(text))
    elif action == "recall":
        console.print(mem.recall(text))
    elif action == "forget":
        console.print(mem.forget(text))
    else:
        console.print(mem.memory_stats())


if __name__ == "__main__":
    cli()
