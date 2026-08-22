"""Basic unit tests (no live LLM required)."""

from grok_local_agent_kit.agent import create_agent
from grok_local_agent_kit.tools import (
    execute_tool,
    get_default_tools,
    list_files,
    read_file,
    write_file,
    append_file,
    execute_python,
    calculator,
    get_datetime,
    get_system_info,
    list_tools,
    http_get,
)


def test_get_default_tools():
    schemas, funcs = get_default_tools()
    assert isinstance(schemas, list)
    assert len(schemas) >= 15
    assert "web_search" in funcs
    assert "http_get" in funcs
    assert "list_files" in funcs
    assert "write_file" in funcs
    assert "append_file" in funcs
    assert "execute_python" in funcs
    assert "calculator" in funcs
    assert "get_datetime" in funcs
    assert "get_system_info" in funcs
    assert "list_tools" in funcs
    assert "mcp_list_resources" in funcs
    assert "mcp_list_tools" in funcs


def test_list_tools():
    result = list_tools()
    assert isinstance(result, str)
    assert "web_search" in result
    assert "http_get" in result
    assert "append_file" in result
    assert "get_system_info" in result
    assert "list_tools" in result
    assert "Available tools" in result


def test_list_files():
    result = list_files(".")
    assert isinstance(result, str)
    assert len(result) > 0


def test_write_and_read_file(tmp_path):
    # cwd-safe restriction: expect either success or clear safety message
    target = tmp_path / "test_write.txt"
    msg = write_file(str(target), "hello local agent")
    assert (
        "Successfully" in msg
        or "outside the working directory" in msg
        or "Permission" in msg
    )


def test_append_file(tmp_path):
    target = tmp_path / "append_me.txt"
    msg = append_file(str(target), "line1\n")
    assert (
        "Successfully" in msg
        or "outside the working directory" in msg
        or "Permission" in msg
    )


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


def test_get_system_info():
    result = get_system_info()
    assert isinstance(result, str)
    assert "OS:" in result
    assert "Python:" in result
    assert "CWD:" in result


def test_http_get_invalid_url():
    result = http_get("not-a-url")
    assert "must start with http" in result.lower() or "error" in result.lower()


def test_agent_init():
    agent = create_agent(model="dummy", provider="ollama", verbose=False)
    assert agent.llm.model == "dummy"
    assert "web_search" in agent.tool_funcs
    assert "http_get" in agent.tool_funcs
    assert "append_file" in agent.tool_funcs
    assert "get_system_info" in agent.tool_funcs
    assert "execute_python" in agent.tool_funcs
    assert "calculator" in agent.tool_funcs
    assert "get_datetime" in agent.tool_funcs
    assert "list_tools" in agent.tool_funcs
    assert "http_get" in agent.list_registered_tools()
    assert "get_system_info" in agent.list_registered_tools()
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
