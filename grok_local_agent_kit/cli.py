"""CLI entrypoint: grok-agent"""

from __future__ import annotations

import click
from rich.console import Console
from rich.markdown import Markdown

from . import __version__
from .agent import create_agent

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="grok-agent")
def cli() -> None:
    """Grok Local Agent Kit — local AI agents with tools."""
    pass


@cli.command()
@click.argument("prompt", required=False)
@click.option("--model", "-m", default="llama3.2", help="Model name")
@click.option(
    "--provider",
    "-p",
    default="ollama",
    type=click.Choice(["ollama", "lmstudio", "openai"]),
    help="LLM provider",
)
@click.option("--base-url", default=None, help="Custom base URL")
@click.option("--verbose", "-v", is_flag=True, help="Show tool calls")
@click.option(
    "--save-history",
    default=None,
    help="Save conversation history to this JSON file on exit",
)
def chat(
    prompt: str | None,
    model: str,
    provider: str,
    base_url: str | None,
    verbose: bool,
    save_history: str | None,
) -> None:
    """Interactive chat or one-shot prompt."""
    agent = create_agent(
        model=model, provider=provider, base_url=base_url, verbose=verbose
    )

    if prompt:
        result = agent.run(prompt)
        console.print(Markdown(result))
        if save_history:
            console.print(agent.save_history(save_history))
        agent.close()
        return

    console.print(
        f"[bold green]Local Agent ready (v{__version__}).[/] "
        "Type 'exit' or Ctrl-C to quit.\n"
        "Special: /save [file], /load [file], /reset, /tools\n"
    )
    try:
        while True:
            user = console.input("[bold cyan]You › [/]")
            stripped = user.strip()
            if stripped.lower() in {"exit", "quit", "q"}:
                break
            if not stripped:
                continue

            # Lightweight interactive commands
            if stripped.startswith("/save"):
                parts = stripped.split(maxsplit=1)
                path = parts[1] if len(parts) > 1 else "agent_history.json"
                console.print(agent.save_history(path))
                continue
            if stripped.startswith("/load"):
                parts = stripped.split(maxsplit=1)
                path = parts[1] if len(parts) > 1 else "agent_history.json"
                console.print(agent.load_history(path))
                continue
            if stripped in {"/reset", "/clear"}:
                agent.reset()
                console.print("[yellow]History cleared.[/]")
                continue
            if stripped in {"/tools", "/list_tools"}:
                from .tools import list_tools as _lt

                console.print(_lt())
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
        agent.close()


@cli.command()
@click.option("--model", "-m", default="llama3.2")
@click.option(
    "--provider",
    "-p",
    default="ollama",
    type=click.Choice(["ollama", "lmstudio", "openai"]),
)
@click.option("--base-url", default=None)
def doctor(model: str, provider: str, base_url: str | None) -> None:
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


if __name__ == "__main__":
    cli()
