"""Show that .py plugins stay inert unless allow_py=True."""

from pathlib import Path
from tempfile import TemporaryDirectory

from grok_local_agent_kit.plugins import apply_plugins, skipped_py_plugins


def main() -> None:
    with TemporaryDirectory() as tmp:
        tools_dir = Path(tmp) / "tools"
        tools_dir.mkdir()
        (tools_dir / "boom.py").write_text(
            "NAME = 'boom'\nDESCRIPTION = 'should not load'\ndef handler(**kw):\n    return 'boom'\n",
            encoding="utf-8",
        )
        (tools_dir / "ok.json").write_text(
            '{"name":"ok","description":"safe json","kind":"json"}',
            encoding="utf-8",
        )
        specs, funcs = apply_plugins([], {}, extra_dirs=[tools_dir])
        print("default load:", list(funcs))
        print("skipped py:", [p.name for p in skipped_py_plugins()])
        specs2, funcs2 = apply_plugins([], {}, extra_dirs=[tools_dir], allow_py=True)
        print("allow_py load:", list(funcs2))


if __name__ == "__main__":
    main()
