import sys
from .agent import create_agent

def main():
    if len(sys.argv) < 3 or sys.argv[1] != 'chat':
        print('Usage: grok-agent chat <prompt>')
        sys.exit(1)
    agent = create_agent()
    response = agent.chat(' '.join(sys.argv[2:]))
    print(response)

if __name__ == "__main__":
    main()