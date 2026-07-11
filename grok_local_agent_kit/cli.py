import sys
import argparse
from .agent import create_agent
from .tools import add_custom_tools

def main():
    parser = argparse.ArgumentParser(description="Grok Local Agent CLI")
    parser.add_argument("command", choices=["chat", "run"], help="Command to run")
    parser.add_argument("prompt", nargs="?", help="Prompt for chat")
    parser.add_argument("--model", default="llama3.2", help="LLM model")
    parser.add_argument("--provider", default="ollama", choices=["ollama", "lmstudio"], help="Provider")
    parser.add_argument("--base-url", help="Base URL for OpenAI compatible")
    
    args = parser.parse_args()
    
    agent = create_agent(args.model, args.provider, args.base_url)
    add_custom_tools(agent)
    
    if args.command == "chat":
        if not args.prompt:
            print("Usage: grok-agent chat <prompt>")
            sys.exit(1)
        response = agent.chat(args.prompt)
        print(response)
    elif args.command == "run":
        print("Running automation agent example...")
        # Can extend for file-based agents

if __name__ == "__main__":
    main()