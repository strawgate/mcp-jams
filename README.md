Simple MCP servers made during MCP Jams


## Simple Memory

Run via:

Setup via Roo/Cline (other clients will use a similar but not identical format for the mcpServers part of the JSON.)
```json
{
  "mcpServers": {
    "memory_server": {
      "command": "uvx",
      "args": [
        "--refresh",
        "--from",
        "./memory",
        "mcp-memory"
      ]
    }
  }
}
```

Development:

Navigate to the memory directory and run `uv sync` and `uv run ./main.py` to start the server.

You can also run in VSCode.

To debug in VSCode you should change the transport in the code from `stdio` to `sse` and then use the following MCP Config to connect to the SSE-based server:

```json
{
  "mcpServers": {
    "memory_server": {
      "url": "http://localhost:8000/sse",
      "alwaysAllow": [
        "add_memory",
        "get_memories"
      ]
    }
  }
}
```

Each time you change the code, you need to restart the server. Each time you restart the server you need to "refresh" the connection in roo / vscode / etc or you will get errors.