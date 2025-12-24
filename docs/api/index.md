# API Reference

WeCom Bot MCP Server provides two ways to interact with WeCom:

1. **MCP Tools** - For AI assistants (Claude, Cline, etc.)
2. **Python API** - For direct programmatic access

## MCP Tools

When used as an MCP server, the following tools are available to AI assistants:

| Tool | Description |
|------|-------------|
| `send_message` | Send text or markdown messages |
| `send_wecom_file` | Send files |
| `send_wecom_image` | Send images |
| `list_wecom_bots` | List configured bots |

[View MCP Tools Reference →](./mcp-tools)

## Python API

For direct Python usage:

```python
from wecom_bot_mcp_server import (
    send_message,
    send_wecom_file,
    send_wecom_image,
)
from wecom_bot_mcp_server.bot_config import (
    get_bot_registry,
    list_available_bots,
)
```

[View Python API Reference →](./python)

## Quick Examples

### Send a Message (MCP)

Ask your AI assistant:
```
Send "Hello World!" to WeCom
```

### Send a Message (Python)

```python
await send_message("Hello World!", msg_type="text")
```

### Send to Specific Bot

```python
await send_message("Alert!", msg_type="text", bot_id="alert")
```
