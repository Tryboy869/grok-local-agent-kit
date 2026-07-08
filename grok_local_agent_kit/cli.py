import argparse
from .agent import create_agent

def main():
    parser = argparse.ArgumentParser(description="Grok Local Agent CLI")
    parser.add_argument("prompt", nargs="+", help="Prompt for the agent")
    args = parser.parse_args()
    agent = create_agent()
    response = agent.chat(" ".join(args.prompt))
    print(response)

if __name__ == "__main__":
    main()