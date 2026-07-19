from grok_local_agent_kit.agent import create_agent
from grok_local_agent_kit.tools import add_custom_tools

agent = create_agent(model="llama3.2")
add_custom_tools(agent)

print("🤖 Automation Agent Example")

# Example automation: create files, search, etc.
response = agent.chat("Create a new Python script hello_world.py that prints 'Hello from local agent!'")
print(response)

# Verify
response2 = agent.chat("List files in current dir")
print(response2)
