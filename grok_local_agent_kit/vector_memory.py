"""Local bag-of-words vector memory on SQLite (stdlib only).

Stores notes in .grok/memory/vectors.db and ranks them with cosine
similarity over a hashed term-frequency vector. Good enough for
offline recall without pulling sqlite-vec or an embedding model.
"""

from __future__ import annotations

import math
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Tuple

MEMORY_DIR = Path(".grok") / "memory"
DB_PATH = MEMORY_DIR / "vectors.db"
DIM = 256
_TOKEN = re.compile(r"[a-z0-9_]{2,}", re.I)


def _connect(path: Path | None = None) -> sqlite3.Connection:
    dest = path or DB_PATH
    dest.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(dest))
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            text TEXT NOT NULL,
            tags TEXT NOT NULL DEFAULT '',
            vec BLOB NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def _tokens(text: str) -> List[str]:
    return [t.lower() for t in _TOKEN.findall(text or "")]


def embed(text: str, dim: int = DIM) -> List[float]:
    vec = [0.0] * dim
    toks = _tokens(text)
    if not toks:
        return vec
    for tok in toks:
        idx = hash(tok) % dim
        vec[idx] += 1.0
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [x / norm for x in vec]


def _pack(vec: Iterable[float]) -> bytes:
    return ",".join(f"{x:.6f}" for x in vec).encode("utf-8")


def _unpack(blob: bytes) -> List[float]:
    raw = blob.decode("utf-8") if isinstance(blob, (bytes, bytearray)) else str(blob)
    if not raw.strip():
        return [0.0] * DIM
    return [float(p) for p in raw.split(",") if p]


def cosine(a: List[float], b: List[float]) -> float:
    n = min(len(a), len(b))
    if n == 0:
        return 0.0
    return sum(a[i] * b[i] for i in range(n))


def vremember(text: str, tags: str = "", db_path: Path | None = None) -> str:
    text = (text or "").strip()
    if not text:
        return "vremember error: empty note"
    vec = embed(f"{text} {tags}")
    conn = _connect(db_path)
    try:
        conn.execute(
            "INSERT INTO notes (ts, text, tags, vec) VALUES (?, ?, ?, ?)",
            (datetime.now(timezone.utc).isoformat(), text, tags or "", _pack(vec)),
        )
        conn.commit()
        row_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
    finally:
        conn.close()
    return f"Vector-remembered id={row_id} ({len(text)} chars)."


def vrecall(query: str, limit: int = 5, db_path: Path | None = None) -> str:
    query = (query or "").strip()
    if not query:
        return "vrecall error: query required"
    qvec = embed(query)
    conn = _connect(db_path)
    try:
        rows = conn.execute("SELECT id, ts, text, tags, vec FROM notes").fetchall()
    finally:
        conn.close()
    if not rows:
        return "No vector notes yet."
    scored: List[Tuple[float, Tuple]] = []
    for row in rows:
        score = cosine(qvec, _unpack(row[4]))
        scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    picked = scored[: max(1, int(limit))]
    lines = []
    for score, row in picked:
        tags = f" [{row[3]}]" if row[3] else ""
        lines.append(f"- #{row[0]} score={score:.3f} {row[1]}{tags}: {row[2]}")
    return "Vector memory:\n" + "\n".join(lines)


def vforget(query: str, db_path: Path | None = None) -> str:
    query = (query or "").strip().lower()
    if not query:
        return "vforget error: query required"
    conn = _connect(db_path)
    try:
        rows = conn.execute("SELECT id, text, tags FROM notes").fetchall()
        ids = [r[0] for r in rows if query in (r[1] + " " + (r[2] or "")).lower()]
        for i in ids:
            conn.execute("DELETE FROM notes WHERE id = ?", (i,))
        conn.commit()
    finally:
        conn.close()
    return f"Forgot {len(ids)} vector note(s) matching {query!r}."


def vstats(db_path: Path | None = None) -> str:
    conn = _connect(db_path)
    try:
        n = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
    finally:
        conn.close()
    dest = db_path or DB_PATH
    return f"vector memory: {n} notes in {dest}"
