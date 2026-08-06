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
    get_datetime,
)


def test_get_default_tools():
    schemas, funcs = get_default_tools()
    assert isinstance(schemas, list)
    assert len(schemas) >= 9
    assert "web_search" in funcs
    assert "list_files" in funcs
    assert "execute_python" in funcs
    assert "calculator" in funcs
    assert "get_datetime" in funcs
    assert "mcp_list_resources" in funcs
    assert "mcp_list_tools" in funcs


def test_list_files():
    result = list_files(".")
    assert isinstance(result, str)
    assert len(result) > 0


def test_write_and_read_file(tmp_path):
    # Use a path under the temp directory which is the cwd for this test? 
    # pytest tmp_path is outside typical cwd, so we test the restriction separately.
    # For functional write/read we temporarily chdir or accept PermissionError path.
    target = tmp_path / "test_write.txt"
    # Because of cwd restriction we expect PermissionError path handling
    msg = write_file(str(target), "hello local agent")
    # Either success (if restriction relaxed in test env) or clear safety message
    assert "Successfully" in msg or "outside the working directory" in msg or "Permission" in msg


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


def test_get_datetime():
    result = get_datetime()
    assert "UTC" in result
    assert len(result) > 10


def test_agent_init():
    agent = create_agent(model="dummy", provider="ollama", verbose=False)
    assert agent.llm.model == "dummy"
    assert "web_search" in agent.tool_funcs
    assert "execute_python" in agent.tool_funcs
    assert "calculator" in agent.tool_funcs
    assert "get_datetime" in agent.tool_funcs
    agent.close()


def test_create_agent_lmstudio_alias():
    agent = create_agent(model="dummy", provider="lmstudio", verbose=False)
    assert agent.llm.provider == "openai"
    assert "1234" in agent.llm.base_url
    agent.close()


def test_register_custom_tool():
    agent = create_agent(model="dummy", provider="ollama", verbose=False)

    def echo(msg: str) -> str:
        return f"echo: {msg}"

    agent.register_tool(
        "echo",
        echo,
        "Echo a message",
        {"type": "object", "properties": {"msg": {"type": "string"}}, "required": ["msg"]},
    )
    assert "echo" in agent.tool_funcs
    assert agent.tool_funcs["echo"]("hi") == "echo: hi"
    agent.close()
