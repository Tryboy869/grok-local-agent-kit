"""
Simple interactive chat agent example.
Requires Ollama running + a model pulled (e.g. ollama pull llama3.2)
"""

from grok_local_agent_kit import create_agent

agent = create_agent(model="llama3.2", verbose=True)

print("🚀 Local Chat Agent ready! Type 'exit' to quit.\n")

if __name__ == "__main__":
    while True:
        prompt = input("You: ").strip()
        if prompt.lower() in {"exit", "quit", "q"}:
            break
        if not prompt:
            continue
        response = agent.chat(prompt)
        print(f"\nAgent: {response}\n")
