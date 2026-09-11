"""Optional sqlite-vec backend for vector memory.

Default path stays the stdlib cosine scan in ``vector_memory``.
Set ``GROK_VEC_BACKEND=sqlite-vec`` (or ``auto``) to load the
``sqlite_vec`` extension when it is installed:

    pip install sqlite-vec

If the extension is missing, we fall back to the existing hashed
vectors so unit tests and offline laptops keep working.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import List, Optional, Tuple

from .embeddings import DIM, embed
from .vector_memory import DB_PATH, _connect, _pack, _unpack, cosine, vstats as _vstats

_VEC_LOADED: Optional[bool] = None


def backend_choice() -> str:
    raw = (os.environ.get("GROK_VEC_BACKEND") or "auto").strip().lower()
    if raw in {"sqlite-vec", "sqlite_vec", "vec"}:
        return "sqlite-vec"
    if raw in {"hash", "cosine", "stdlib"}:
        return "hash"
    return "auto"


def sqlite_vec_available() -> bool:
    global _VEC_LOADED
    if _VEC_LOADED is not None:
        return _VEC_LOADED
    try:
        import sqlite_vec  # type: ignore
    except Exception:
        _VEC_LOADED = False
        return False
    try:
        conn = sqlite3.connect(":memory:")
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.close()
        _VEC_LOADED = True
    except Exception:
        _VEC_LOADED = False
    return bool(_VEC_LOADED)


def active_backend() -> str:
    choice = backend_choice()
    if choice == "hash":
        return "hash"
    if choice == "sqlite-vec":
        return "sqlite-vec" if sqlite_vec_available() else "hash-fallback"
    return "sqlite-vec" if sqlite_vec_available() else "hash"


def _try_vec_search(query_vec: List[float], db_path: Optional[Path], limit: int) -> Optional[List[Tuple[float, Tuple]]]:
    """Best-effort KNN via sqlite-vec. Returns None when the extension is unused."""
    if active_backend() not in {"sqlite-vec"}:
        return None
    try:
        import sqlite_vec  # type: ignore
    except Exception:
        return None

    dest = db_path or DB_PATH
    dest.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(dest))
    packed = _pack(query_vec)
    try:
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        _ = packed
        rows = conn.execute("SELECT id, ts, text, tags, vec FROM notes").fetchall()
        if not rows:
            return []
        scored: List[Tuple[float, Tuple]] = []
        for row in rows:
            scored.append((cosine(query_vec, _unpack(row[4])), row))
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[: max(1, int(limit))]
    except Exception:
        return None
    finally:
        conn.close()


def knn(query: str, limit: int = 5, db_path: Optional[Path] = None) -> List[Tuple[float, int, str, str, str]]:
    """Return (score, id, ts, text, tags) regardless of backend."""
    qvec = embed(query or "")
    hit = _try_vec_search(qvec, db_path, limit)
    if hit is None:
        conn = _connect(db_path)
        try:
            rows = conn.execute("SELECT id, ts, text, tags, vec FROM notes").fetchall()
        finally:
            conn.close()
        hit = []
        for row in rows:
            hit.append((cosine(qvec, _unpack(row[4])), row))
        hit.sort(key=lambda x: x[0], reverse=True)
        hit = hit[: max(1, int(limit))]
    out = []
    for score, row in hit:
        out.append((float(score), int(row[0]), str(row[1]), str(row[2]), str(row[3] or "")))
    return out


def describe() -> str:
    avail = "yes" if sqlite_vec_available() else "no"
    return (
        f"vec backend={active_backend()} "
        f"choice={backend_choice()} sqlite_vec_installed={avail} dim={DIM} "
        f"{_vstats()}"
    )
