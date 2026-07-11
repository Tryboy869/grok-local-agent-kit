"""
Advanced tools and MCP integration for grok-local-agent-kit.
"""
from .agent import Agent
import os
from typing import Dict

def add_custom_tools(agent: Agent):
    """Extend with custom tools - example"""
    def list_files(dir_path: str = ".") -> str:
        try:
            return "\n".join(os.listdir(dir_path))
        except Exception as e:
            return str(e)
    
    agent.register_tool(
        name="list_files",
        func=list_files,
        description="List files in a directory",
        parameters={
            "type": "object",
            "properties": {"dir_path": {"type": "string", "description": "Directory path"}},
            "required": []
        }
    )
    print("Custom tools added: list_files, etc.")

# MCP simulation
def mcp_register_context(key: str, value: str):
    """Simulate MCP context registration"""
    print(f"MCP: Registered context {key}")
    return True