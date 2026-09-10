from grok_local_agent_kit.budget import ToolBudget, get_budget, reset_budget, set_budget
from grok_local_agent_kit.cache import get_cache
from grok_local_agent_kit.retry import retry_call
from grok_local_agent_kit.tools import execute_tool, get_default_tools


def test_budget_caps_global_and_per_tool():
    get_cache().enabled = False
    set_budget(ToolBudget(max_calls=3, per_tool={"calculator": 2}))
    reset_budget()
    _, registry = get_default_tools()
    a = execute_tool("calculator", {"expression": "1+1"}, registry)
    b = execute_tool("calculator", {"expression": "2+2"}, registry)
    c = execute_tool("calculator", {"expression": "3+3"}, registry)
    assert "2" in a and "4" in b
    assert "Budget exceeded" in c
    stats = get_budget().stats()
    assert stats["per_tool"]["calculator"] == 2


def test_retry_succeeds_after_failures():
    n = {"i": 0}

    def flaky():
        n["i"] += 1
        if n["i"] < 3:
            raise ValueError("nope")
        return 42

    assert retry_call(flaky, attempts=5, base_delay=0, sleep=lambda _: None) == 42
    assert n["i"] == 3
