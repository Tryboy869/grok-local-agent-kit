"""
Command-line interface for grok-local-agent-kit.
"""

import click
from rich.console import Console
from rich.markdown import Markdown

from .agent import create_agent
from . import __version__

console = Console()


@click.group()
@click.version_option(__version__, prog_name="grok-agent")
def cli() -> None:
    """Grok Local Agent Kit — run powerful AI agents completely offline."""
    pass


@cli.command()
@click.argument("prompt")
@click.option("--model", "-m", default="llama3.2", help="Ollama model to use")
@click.option("--verbose/--quiet", default=True)
def chat(prompt: str, model: str, verbose: bool) -> None:
    """Ask the agent a single question."""
    agent = create_agent(model=model, verbose=verbose)
    answer = agent.run(prompt)
    console.print()
    console.print(Markdown(answer))


@cli.command()
@click.option("--model", "-m", default="llama3.2", help="Ollama model to use")
def repl(model: str) -> None:
    """Interactive chat loop."""
    agent = create_agent(model=model, verbose=False)
    console.print(f"[bold green]Grok Local Agent[/] (model: {model}) — type 'exit' to quit\n")
    while True:
        try:
            prompt = console.input("[bold cyan]You > [/]")
        except (EOFError, KeyboardInterrupt):
            console.print("\nBye!")
            break
        if prompt.strip().lower() in {"exit", "quit", "q"}:
            console.print("Bye!")
            break
        if not prompt.strip():
            continue
        answer = agent.run(prompt)
        console.print()
        console.print(Markdown(answer))
        console.print()


if __name__ == "__main__":
    cli()
