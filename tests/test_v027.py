from grok_local_agent_kit import __version__
from grok_local_agent_kit.tools import calculator, list_tools
from grok_local_agent_kit.websearch import _format, search_web


def test_version():
    assert __version__ == "0.27.0"


def test_calculator_and_tool_list():
    assert "52" in calculator("21*2 + 10")
    listing = list_tools()
    assert "web_search" in listing
    assert "list_files" in listing


def test_format_rows():
    text = _format([("Hello", "https://example.com", "body")])
    assert "Hello" in text
    assert "https://example.com" in text


def test_search_web_empty_query():
    assert "Error" in search_web("  ")
