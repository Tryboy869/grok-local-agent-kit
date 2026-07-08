from grok_local_agent_kit.agent import create_agent

agent = create_agent(model="llama3.2")
print("Chat Agent ready!")
response = agent.chat("Hello! Tell me a fun fact about AI agents.")
print(response)