"""Embedding backends for vector memory.

Default is a hashed bag-of-words vector (stdlib only). When
GROK_EMBED_BACKEND=ollama and a local Ollama daemon is up, notes are
embedded via POST /api/embeddings and stored as-is.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import urllib.error
import urllib.request
from typing import List, Optional

DIM = 256
_TOKEN = re.compile(r"[a-z0-9_]{2,}", re.I)


def hash_embed(text: str, dim: int = DIM) -> List[float]:
    """Deterministic hashed bag-of-words embedding. No network."""
    vec = [0.0] * dim
    toks = [t.lower() for t in _TOKEN.findall(text or "")]
    if not toks:
        return vec
    for tok in toks:
        digest = hashlib.md5(tok.encode("utf-8")).hexdigest()
        idx = int(digest, 16) % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def ollama_embed(
    text: str,
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    timeout: float = 8.0,
) -> List[float]:
    """Call Ollama /api/embeddings. Raises on transport or payload errors."""
    model = model or os.environ.get("GROK_EMBED_MODEL") or "nomic-embed-text"
    base = (base_url or os.environ.get("OLLAMA_HOST") or "http://127.0.0.1:11434").rstrip("/")
    payload = json.dumps({"model": model, "prompt": text or ""}).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/api/embeddings",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    vec = body.get("embedding") or body.get("embeddings")
    if isinstance(vec, list) and vec and isinstance(vec[0], list):
        vec = vec[0]
    if not isinstance(vec, list) or not vec:
        raise ValueError("ollama embeddings response missing embedding[]")
    return [float(x) for x in vec]


def embed(text: str, dim: int = DIM) -> List[float]:
    """Public embed used by vector memory.

    Backend is chosen by GROK_EMBED_BACKEND:
      - hash (default): hashed bag-of-words
      - ollama: live Ollama embeddings, fall back to hash on failure
    """
    backend = (os.environ.get("GROK_EMBED_BACKEND") or "hash").strip().lower()
    if backend in {"ollama", "nomic", "real"}:
        try:
            return ollama_embed(text)
        except Exception:
            return hash_embed(text, dim=dim)
    return hash_embed(text, dim=dim)


def backend_name() -> str:
    return (os.environ.get("GROK_EMBED_BACKEND") or "hash").strip().lower()
