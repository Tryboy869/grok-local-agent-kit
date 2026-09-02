"""Sandbox + embedding backend tests (no live LLM)."""

import os

from grok_local_agent_kit.embeddings import backend_name, embed, hash_embed
from grok_local_agent_kit.sandbox import execute_python
from grok_local_agent_kit.vector_memory import cosine


def test_sandbox_allows_math():
    out = execute_python("import math\nprint(int(math.sqrt(144)))")
    assert "12" in out


def test_sandbox_blocks_os_and_dunder():
    assert "Blocked" in execute_python("import os")
    assert "Blocked" in execute_python("import subprocess")
    assert "Blocked" in execute_python("print((1).__class__.__bases__)")
    assert "Blocked" in execute_python("eval('1+1')")
    assert "Blocked" in execute_python("open('/etc/passwd')")


def test_sandbox_timeout():
    out = execute_python("while True:\n    pass", timeout=0.3)
    assert "timed out" in out or "error" in out.lower() or "Blocked" in out


def test_hash_embed_is_stable_and_ranks():
    a = hash_embed("local ollama llama agent")
    b = hash_embed("ollama llama local agent")
    c = hash_embed("strawberry cheesecake")
    assert cosine(a, b) > cosine(a, c)
    assert embed("hello") == hash_embed("hello")


def test_backend_name_default():
    old = os.environ.pop("GROK_EMBED_BACKEND", None)
    try:
        assert backend_name() == "hash"
    finally:
        if old is not None:
            os.environ["GROK_EMBED_BACKEND"] = old
