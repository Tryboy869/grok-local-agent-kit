from grok_local_agent_kit.agent import create_agent
from grok_local_agent_kit.tools import add_custom_tools

# Initialize chat agent with Ollama (or LM Studio)
agent = create_agent(model="llama3.2", provider="ollama")
add_custom_tools(agent)

print("🚀 Local Chat Agent Ready! Supports tools, routing, MCP.")

# Interactive example
if __name__ == "__main__":
    while True:
        prompt = input("You: ")
        if prompt.lower() in ['exit', 'quit']:
            break
        response = agent.chat(prompt)
        print(f"Agent: {response}")
