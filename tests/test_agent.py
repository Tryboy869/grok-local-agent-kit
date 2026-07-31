"""Basic unit tests (no live LLM required)."""

from grok_local_agent_kit.agent import create_agent
from grok_local_agent_kit.tools import (
    execute_tool,
    get_default_tools,
    list_files,
    read_file,
    write_file,
    execute_python,
    calculator,
)


def test_get_default_tools():
    schemas, funcs = get_default_tools()
    assert isinstance(schemas, list)
    assert len(schemas) >= 7
    assert "web_search" in funcs
    assert "list_files" in funcs
    assert "execute_python" in funcs
    assert "calculator" in funcs
    assert "mcp_list_resources" in funcs


def test_list_files():
    result = list_files(".")
    assert isinstance(result, str)
    assert len(result) > 0


def test_write_and_read_file(tmp_path):
    target = tmp_path / "test_write.txt"
    msg = write_file(str(target), "hello local agent")
    assert "Successfully" in msg
    content = read_file(str(target))
    assert content == "hello local agent"


def test_execute_python_simple():
    result = execute_python("print(2 + 2)")
    assert "4" in result


def test_execute_python_blocked():
    result = execute_python("import os; os.system('ls')")
    assert "Blocked" in result or "error" in result.lower()


def test_calculator():
    assert calculator("2 + 2") == "4"
    assert "12" in calculator("sqrt(144)") or calculator("sqrt(144)") == "12.0"
    blocked = calculator("__import__('os').system('ls')")
    assert (
        "Blocked" in blocked
        or "error" in blocked.lower()
        or "Calculator error" in blocked
    )


def test_agent_init():
    agent = create_agent(model="dummy", provider="ollama", verbose=False)
    assert agent.llm.model == "dummy"
    assert "web_search" in agent.tool_funcs
    assert "execute_python" in agent.tool_funcs
    assert "calculator" in agent.tool_funcs
    agent.close()


def test_create_agent_lmstudio_alias():
    agent = create_agent(model="dummy", provider="lmstudio", verbose=False)
    assert agent.llm.provider == "openai"
    assert "1234" in agent.llm.base_url
    agent.close()


def test_register_custom_tool():
    agent = create_agent(model="dummy", verbose=False)

    def hello(name: str = "world") -> str:
        return f"Hello {name}"

    agent.register_tool(
        name="hello",
        func=hello,
        description="Say hello",
        parameters={
            "type": "object",
            "properties": {"name": {"type": "string"}},
            "required": [],
        },
    )
    assert "hello" in agent.tool_funcs
    assert agent.tool_funcs["hello"]("Grok") == "Hello Grok"
    agent.close()


def test_execute_tool_unknown():
    _, funcs = get_default_tools()
    result = execute_tool("nonexistent_tool", {}, funcs)
    assert "Unknown tool" in result
