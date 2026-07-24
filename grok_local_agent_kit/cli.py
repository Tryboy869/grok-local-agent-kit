import click
from .agent import create_agent

@click.group()
def cli():
    pass

@cli.command()
@click.argument('prompt')
def chat(prompt):
    agent = create_agent()
    print(agent.run(prompt))

if __name__ == '__main__':
    cli()