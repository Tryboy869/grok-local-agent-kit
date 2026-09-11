from pathlib import Path
from tempfile import TemporaryDirectory

from grok_local_agent_kit.sqlite_vec_store import active_backend, describe, knn, sqlite_vec_available
from grok_local_agent_kit.vector_memory import vremember


def test_describe_mentions_backend():
    text = describe()
    assert "backend=" in text
    assert active_backend() in {"hash", "sqlite-vec", "hash-fallback"}


def test_knn_ranks_related_note_first():
    with TemporaryDirectory() as tmp:
        db = Path(tmp) / "v.db"
        vremember("cats sit on keyboards and interrupt coding", db_path=db)
        vremember("the stock market closed mixed on friday", db_path=db)
        rows = knn("cats on keyboards coding", limit=2, db_path=db)
        assert rows
        assert "cats" in rows[0][3]


def test_sqlite_vec_probe_is_boolean():
    assert sqlite_vec_available() in {True, False}
