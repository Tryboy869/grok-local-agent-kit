import argparse
from .agent import Agent

def main():
    parser = argparse.ArgumentParser(description="Grok Local Agent Kit CLI")
    parser.add_argument("command", choices=["chat"])
    parser.add_argument("prompt", nargs="+")
    args = parser.parse_args()
    
    agent = Agent()
    if args.command == "chat":
        print(agent.chat(" ".join(args.prompt)))

if __name__ == "__main__":
    main()