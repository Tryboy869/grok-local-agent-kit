# workflow-demo.gif (storyboard)

Not a binary GIF. Record it with asciinema + agg when you want the README embed.

Command: `grok-agent workflow demo`

| t | frame |
|---|---|
| 0.0s | shell prompt, command typed |
| 2.0s | `list_files` shows `inbox.txt` |
| 4.0s | `write_file` → `automation-note.txt` |
| 7.0s | `web_search` fixture: Ollama + LM Studio lines |
| 10.0s | `mcp_call` JSON echo of the listing |
| 12.0s | `wrote=True` |

Caption: local agent loop, no API key, no daemon. Router (Ollama then LM Studio) is a separate path: `grok-agent route demo`.
