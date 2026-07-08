from grok_local_agent_kit.agent import create_agent
import os

agent = create_agent()

# Example automation
print("Automation Agent Demo")
response = agent.chat("Read the README.md file and summarize the key features.")
print(response)

# Or use file tool directly if exposed
if os.path.exists('README.md'):
    print("File exists, agent can read it.")