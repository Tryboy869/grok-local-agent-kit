"""Basic unit tests (no Ollama required)."""

from grok_local_agent_kit.tools import list_directory, execute_python, Tool
from grok_local_agent_kit.agent import Agent


def test_list_directory():
    result = list_directory(".")
    assert isinstance(result, str)
    assert len(result) > 0


def test_execute_python_simple():
    result = execute_python("print(2 + 2)")
    assert "4" in result


def test_agent_init():
    agent = Agent(model="dummy", verbose=False)
    assert agent.model == "dummy"
    assert "web_search" in agent.tools
    assert "execute_python" in agent.tools


def test_register_custom_tool():
    agent = Agent(model="dummy", verbose=False)

    def hello(name: str = "world") -> str:
        return f"Hello {name}"

    tool = Tool(name="hello", description="Say hello", func=hello)
    agent.register_tool(tool)
    assert "hello" in agent.tools
    assert agent.tools["hello"].func("Grok") == "Hello Grok"
