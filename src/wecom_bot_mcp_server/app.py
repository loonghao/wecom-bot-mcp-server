"""Application configuration for WeCom Bot MCP Server."""

# Import third-party modules
from mcp.server.fastmcp import FastMCP

# Constants
APP_NAME = "wecom_bot_mcp_server"
APP_DESCRIPTION = """WeCom Bot MCP Server for sending messages and files to WeCom groups.

## Multi-Bot Support

This server supports multiple WeCom bot configurations. You can send messages to different
bots by specifying the `bot_id` parameter in send functions.

### Checking Available Bots

Before sending messages, you can call `list_wecom_bots` to see all configured bots:
- Each bot has an `id`, `name`, and optional `description`
- The `default` bot is used when no `bot_id` is specified

### Sending to Specific Bots

When calling `send_message`, `send_wecom_image`, `send_wecom_file`, or template card tools:
- Omit `bot_id` to use the default bot
- Specify `bot_id` to target a specific bot (e.g., `bot_id="alert"` or `bot_id="ci"`)

### Configuration

Bots can be configured via environment variables:
1. `WECOM_WEBHOOK_URL` - Sets the default bot (backward compatible)
2. `WECOM_BOTS` - JSON object for multiple bots:
   `{"alert": {"name": "Alert Bot", "webhook_url": "https://..."}, ...}`
3. `WECOM_BOT_<NAME>_URL` - Individual bot URLs (e.g., `WECOM_BOT_ALERT_URL`)

### Best Practices

- Use descriptive bot names that indicate their purpose (e.g., "CI Notifications", "Alerts")
- When multiple bots are available, always consider which bot is most appropriate
- Use `list_wecom_bots` to discover available bots before sending
"""

# Initialize FastMCP server
mcp = FastMCP(
    name=APP_NAME,
    instructions=APP_DESCRIPTION,
)
