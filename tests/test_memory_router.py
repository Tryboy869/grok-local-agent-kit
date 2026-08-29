from grok_local_agent_kit.mcp_tools import extend_default_tools
from grok_local_agent_kit.memory import forget, memory_stats, recall, remember
from grok_local_agent_kit.orchestrator import DEFAULT_ROLES, Orchestrator
from grok_local_agent_kit.router import MultiLLMRouter, endpoint_from_env
from grok_local_agent_kit.tools import get_default_tools


def test_memory_roundtrip(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert "Remembered" in remember("alpha note about ollama", "llm")
    assert "ollama" in recall("ollama").lower()
    assert "memory:" in memory_stats()
    assert "Forgot 1" in forget("alpha")
    assert "0 notes" in memory_stats() or "memory: 0" in memory_stats()


def test_default_tools_include_memory():
    schemas, funcs = extend_default_tools(*get_default_tools())
    names = {s["function"]["name"] for s in schemas}
    assert {"remember", "recall", "forget"} <= names
    assert "remember" in funcs
    assert len(funcs) >= 23


def test_endpoint_chain_order():
    chain = endpoint_from_env("ollama")
    assert chain[0].provider == "ollama"
    chain2 = endpoint_from_env("lmstudio")
    assert chain2[0].provider == "openai"


def test_router_constructs():
    r = MultiLLMRouter()
    assert len(r.chain) >= 2
    rows = r.probe()
    assert rows and "status" in rows[0]
    r.close()


def test_orchestrator_no_llm_roles():
    class Dummy:
        def run(self, prompt: str) -> str:
            return "STEP" if "numbered" in prompt.lower() or "Plan" in prompt or "steps" in prompt.lower() else "DONE"

    orch = Orchestrator(lambda: Dummy())
    out = orch.run("demo goal", specialists=["researcher"])
    assert "## Plan" in out
    assert "## researcher" in out
    assert "planner" in DEFAULT_ROLES
