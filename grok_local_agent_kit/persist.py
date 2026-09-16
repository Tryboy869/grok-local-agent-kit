"""Persist a Team blackboard to JSONL or SQLite.

Both formats are local, cwd-safe, and LLM-free. JSONL is the default because
it is easy to tail; SQLite is useful when you want to query by author/kind.
"""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import List, Union

from .team import ALLOWED_KINDS, Blackboard, Post

PathLike = Union[str, Path]


def _safe_path(path: PathLike) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = Path.cwd() / p
    p = p.resolve()
    cwd = Path.cwd().resolve()
    try:
        p.relative_to(cwd)
    except ValueError as exc:
        raise ValueError(f"path escapes workspace: {p}") from exc
    return p


def post_to_dict(post: Post) -> dict:
    return {
        "author": post.author,
        "kind": post.kind,
        "body": post.body,
        "ts": post.ts,
        "tags": list(post.tags),
    }


def post_from_dict(row: dict) -> Post:
    kind = str(row.get("kind") or "note").lower()
    if kind not in ALLOWED_KINDS:
        kind = "note"
    tags = row.get("tags") or []
    if isinstance(tags, str):
        tags = [t for t in tags.split(",") if t]
    return Post(
        author=str(row.get("author") or "unknown"),
        kind=kind,
        body=str(row.get("body") or ""),
        ts=str(row.get("ts") or ""),
        tags=list(tags),
    )


def save_jsonl(board: Blackboard, path: PathLike) -> Path:
    dest = _safe_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    posts = board.recent(n=10_000)
    with dest.open("w", encoding="utf-8") as fh:
        for post in posts:
            fh.write(json.dumps(post_to_dict(post), ensure_ascii=False) + "\n")
    return dest


def load_jsonl(path: PathLike, board: Blackboard | None = None) -> Blackboard:
    src = _safe_path(path)
    board = board or Blackboard()
    if not src.exists():
        return board
    with src.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            board.post_raw(post_from_dict(json.loads(line)))
    return board


def save_sqlite(board: Blackboard, path: PathLike) -> Path:
    dest = _safe_path(path)
    dest.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(dest))
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                kind TEXT NOT NULL,
                body TEXT NOT NULL,
                ts TEXT NOT NULL,
                tags TEXT NOT NULL
            )
            """
        )
        conn.execute("DELETE FROM posts")
        rows = [
            (p.author, p.kind, p.body, p.ts, ",".join(p.tags))
            for p in board.recent(n=10_000)
        ]
        conn.executemany(
            "INSERT INTO posts (author, kind, body, ts, tags) VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()
    return dest


def load_sqlite(path: PathLike, board: Blackboard | None = None) -> Blackboard:
    src = _safe_path(path)
    board = board or Blackboard()
    if not src.exists():
        return board
    conn = sqlite3.connect(str(src))
    try:
        rows = conn.execute(
            "SELECT author, kind, body, ts, tags FROM posts ORDER BY id"
        ).fetchall()
    finally:
        conn.close()
    for author, kind, body, ts, tags in rows:
        board.post_raw(
            Post(
                author=author,
                kind=kind if kind in ALLOWED_KINDS else "note",
                body=body,
                ts=ts,
                tags=[t for t in (tags or "").split(",") if t],
            )
        )
    return board


def save_board(board: Blackboard, path: PathLike) -> Path:
    dest = Path(path)
    suffix = dest.suffix.lower()
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        return save_sqlite(board, dest)
    return save_jsonl(board, dest)


def load_board(path: PathLike, board: Blackboard | None = None) -> Blackboard:
    src = Path(path)
    suffix = src.suffix.lower()
    if suffix in {".db", ".sqlite", ".sqlite3"}:
        return load_sqlite(src, board)
    return load_jsonl(src, board)


def list_posts(board: Blackboard) -> List[Post]:
    return board.recent(n=10_000)
