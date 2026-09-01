from grok_local_agent_kit.mcp_sse import SSEMCPClient
from grok_local_agent_kit.usage import UsageStats, estimate_tokens
from grok_local_agent_kit.vector_memory import cosine, embed, vforget, vrecall, vremember, vstats


def test_embed_and_cosine_ranks_related_text():
    a = embed("ollama local llama model")
    b = embed("run llama locally with ollama")
    c = embed("banana smoothie recipe")
    assert cosine(a, b) > cosine(a, c)


def test_vector_memory_roundtrip(tmp_path):
    db = tmp_path / "v.db"
    assert "Vector-remembered" in vremember("ship the agent kit mvp", "release", db)
    out = vrecall("mvp kit", db_path=db)
    assert "ship the agent kit mvp" in out
    assert "vector memory:" in vstats(db)
    assert "Forgot 1" in vforget("mvp", db)
    assert "0 notes" in vstats(db)


def test_usage_tracker():
    u = UsageStats()
    u.record_prompt([{"role": "user", "content": "hello world"}])
    u.record_completion("hi there")
    u.record_tool()
    d = u.as_dict()
    assert d["llm_calls"] == 1
    assert d["tool_calls"] == 1
    assert d["estimated_prompt_tokens"] >= 1
    assert "usage:" in u.summary()
    assert estimate_tokens("abcd") == 1


def test_sse_client_parses_event_stream():
    c = SSEMCPClient("http://127.0.0.1:9/mcp", max_retries=1)
    parsed = c._parse_sse_body('data: {"result": {"ok": true}}\n\n')
    assert parsed["result"]["ok"] is True
