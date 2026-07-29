"""CLI entrypoint: grok-agent"""

from __future__ import annotations

import click
from rich.console import Console
from rich.markdown import Markdown

from .agent import create_agent

console = Console()


@click.group()
@click.version_option(package_name="grok-local-agent-kit")
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
def chat(
    prompt: str | None, model: str, provider: str, base_url: str | None, verbose: bool
) -> None:
    """Interactive chat or one-shot prompt."""
    if provider == "lmstudio":
        provider = "openai"  # same protocol
        base_url = base_url or "http://localhost:1234/v1"

    agent = create_agent(
        model=model, provider=provider, base_url=base_url, verbose=verbose
    )

    if prompt:
        result = agent.run(prompt)
        console.print(Markdown(result))
        agent.close()
        return

    console.print("[bold green]Local Agent ready.[/] Type 'exit' or Ctrl-C to quit.\n")
    try:
        while True:
            user = console.input("[bold cyan]You › [/]")
            if user.strip().lower() in {"exit", "quit", "q"}:
                break
            if not user.strip():
                continue
            result = agent.chat(user)
            console.print()
            console.print(Markdown(result))
            console.print()
    except (KeyboardInterrupt, EOFError):
        console.print("\nBye!")
    finally:
        agent.close()


@cli.command()
@click.option("--model", "-m", default="llama3.2")
@click.option("--provider", "-p", default="ollama")
def doctor(model: str, provider: str) -> None:
    """Check connectivity to local LLM and list available tools."""
    console.print(f"[bold]Checking {provider} / {model} ...[/]")
    agent = create_agent(model=model, provider=provider)
    try:
        reply = agent.run("Reply with exactly: OK")
        console.print(f"[green]✓ LLM responded:[/] {reply[:120]}")
        console.print(f"[green]✓ Tools registered:[/] {', '.join(sorted(agent.tool_funcs.keys()))}")
    except Exception as e:
        console.print(f"[red]✗ Failed:[/] {e}")
    finally:
        agent.close()


if __name__ == "__main__":
    cli()
