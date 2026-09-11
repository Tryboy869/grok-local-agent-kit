"""Write a tiny local transcript then print the summary."""

from grok_local_agent_kit.transcripts import append_turn, new_path, summarize


def main() -> None:
    path = new_path("example")
    append_turn(path, "user", "list files in this workspace")
    append_turn(path, "assistant", "I would call list_files on .")
    append_turn(path, "tool", "FILE  README.md", extra={"tool": "list_files"})
    print(summarize(path))
    print(path)


if __name__ == "__main__":
    main()
