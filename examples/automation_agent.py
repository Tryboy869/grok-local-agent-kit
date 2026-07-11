from grok_local_agent_kit.agent import create_agent
from grok_local_agent_kit.tools import add_custom_tools
import time

agent = create_agent(model="llama3.2")
add_custom_tools(agent)

print("🤖 Automation Agent - File ops and planning example")

# Example automation loop
task = "Create a report.txt with summary of local AI agents benefits."
response = agent.chat(task)
print("Task response:", response)

# Verify
print("\nFile created check:")
try:
    with open("report.txt", "r") as f:
        print(f.read()[:300])
except:
    print("File not found or error.")