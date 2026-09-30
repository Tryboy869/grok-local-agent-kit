"""v0.41 — catalog.pick wired into MultiLLMRouter."""

from grok_local_agent_kit.catalog import Catalog, ModelEntry
from grok_local_agent_kit.catalog_route import apply_catalog, demo_catalog_route
from grok_local_agent_kit.router import LLMEndpoint, MultiLLMRouter


def _cat() -> Catalog:
    return Catalog(
        created_at="t",
        backends={"ollama": {"reachable": True}, "lmstudio": {"reachable": True}},
        models=[
            ModelEntry(provider="ollama", name="llama3.2:latest"),
            ModelEntry(provider="ollama", name="mistral:7b"),
            ModelEntry(provider="lmstudio", name="qwen2.5-7b"),
        ],
    )


def test_apply_catalog_rewrites_models():
    chain = [
        LLMEndpoint(name="ollama", provider="ollama", model="placeholder"),
        LLMEndpoint(name="lmstudio", provider="openai", model="local-model"),
    ]
    router = MultiLLMRouter(chain=chain, sticky=False)
    changes = apply_catalog(router, _cat(), prefer="llama3.2")
    assert ("ollama", "placeholder", "llama3.2:latest") in changes
    assert ("lmstudio", "local-model", "qwen2.5-7b") in changes
    assert router.chain[0].model == "llama3.2:latest"
    assert router.chain[1].model == "qwen2.5-7b"


def test_apply_catalog_skips_missing_provider():
    cat = Catalog(
        created_at="t",
        models=[ModelEntry(provider="ollama", name="only-ollama")],
    )
    chain = [
        LLMEndpoint(name="ollama", provider="ollama", model="old"),
        LLMEndpoint(name="lmstudio", provider="openai", model="keep-me"),
    ]
    router = MultiLLMRouter(chain=chain, sticky=False)
    changes = apply_catalog(router, cat)
    assert changes == [("ollama", "old", "only-ollama")]
    assert router.chain[1].model == "keep-me"


def test_apply_catalog_noop_when_same_name():
    chain = [LLMEndpoint(name="ollama", provider="ollama", model="llama3.2:latest")]
    router = MultiLLMRouter(chain=chain, sticky=False)
    changes = apply_catalog(router, _cat(), prefer="llama3.2")
    assert changes == []


def test_demo_catalog_route_text():
    text = demo_catalog_route()
    assert "catalog-route" in text
    assert "llama3.2:latest" in text
    assert "qwen2.5-7b" in text
    assert "placeholder" in text or "llama3.2" in text
