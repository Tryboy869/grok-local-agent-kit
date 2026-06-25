from .agent import Agent
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        agent = Agent()
        print(agent.run(prompt))
    else:
        print("Usage: python -m grok_local_agent_kit.run_agent <prompt>")
