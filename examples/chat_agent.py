from grok_local_agent_kit.agent import create_agent
from grok_local_agent_kit.tools import add_custom_tools

# Create and enhance agent
agent = create_agent(model="llama3.2", provider="ollama")
add_custom_tools(agent)

print("🚀 Chat Agent ready! Multi-LLM, tools, MCP support.")
print("Example interaction:")

response = agent.chat("Hello! Who are you and what can you do locally?")
print(response)

# Another example
response2 = agent.chat("Search for latest AI news and summarize.")
print(response2)