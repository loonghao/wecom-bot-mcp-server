# Multi-Bot Support

WeCom Bot MCP Server supports configuring and using multiple bots, allowing you to route messages to different groups or use different bots for different purposes.

## Why Multiple Bots?

- **Separate concerns**: Use different bots for alerts, CI/CD notifications, and team updates
- **Multiple groups**: Send messages to different WeCom groups
- **Access control**: Different teams can have their own bots

## Configuration Methods

### Method 1: JSON Configuration (Recommended)

Configure all bots in a single JSON environment variable:

::: code-group

```bash [Linux/macOS]
export WECOM_BOTS='{
  "alert": {
    "name": "Alert Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "description": "For system alerts"
  },
  "ci": {
    "name": "CI Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy",
    "description": "For CI/CD notifications"
  },
  "team": {
    "name": "Team Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz",
    "description": "For team updates"
  }
}'
```

```powershell [Windows PowerShell]
$env:WECOM_BOTS = '{"alert": {"name": "Alert Bot", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx", "description": "For system alerts"}, "ci": {"name": "CI Bot", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy", "description": "For CI/CD notifications"}}'
```

:::

### Method 2: Individual Environment Variables

Set separate environment variables for each bot:

```bash
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy"
export WECOM_BOT_NOTIFY_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz"
```

Bot IDs are derived from the variable name (lowercase): `WECOM_BOT_ALERT_URL` → `alert`

### Method 3: Combined Mode

Use `WECOM_WEBHOOK_URL` as the default bot and add more bots:

```bash
# Default bot
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default"

# Additional bots
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci"
```

## MCP Client Configuration

### Claude Desktop / Windsurf / Cline

```json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default",
        "WECOM_BOTS": "{\"alert\": {\"name\": \"Alert Bot\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert\"}, \"ci\": {\"name\": \"CI Bot\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci\"}}"
      }
    }
  }
}
```

## Using Multiple Bots

### With AI Assistant

The AI assistant automatically knows about available bots. You can specify which bot to use:

```
USER: "Send a critical alert to the alert bot: Server CPU is above 90%"
ASSISTANT: [Uses send_message with bot_id="alert"]

USER: "Send build success notification to the CI bot"
ASSISTANT: [Uses send_message with bot_id="ci"]

USER: "What WeCom bots are available?"
ASSISTANT: [Uses list_wecom_bots tool to show all bots]
```

### With Python API

```python
from wecom_bot_mcp_server import send_message, send_wecom_file, send_wecom_image

# Send to default bot
await send_message("Hello!", msg_type="text")

# Send to specific bot
await send_message(
    content="⚠️ High CPU usage detected!",
    msg_type="markdown",
    bot_id="alert"
)

# Send file to CI bot
await send_wecom_file("/path/to/report.pdf", bot_id="ci")

# Send image to team bot
await send_wecom_image("/path/to/chart.png", bot_id="team")
```

### List Available Bots

```python
from wecom_bot_mcp_server.bot_config import list_available_bots, get_bot_registry

# List all bots
bots = list_available_bots()
for bot in bots:
    print(f"Bot: {bot['id']} - {bot['name']} - {bot['description']}")

# Check if a bot exists
registry = get_bot_registry()
if registry.has_bot("alert"):
    print("Alert bot is configured")

# Get bot count
print(f"Total bots: {registry.get_bot_count()}")
```

## Best Practices

1. **Use descriptive names**: Give bots meaningful names and descriptions
2. **Separate concerns**: Use different bots for different purposes
3. **Default bot**: Always configure a default bot for general messages
4. **Document your bots**: Keep track of which bot is for which purpose

## Troubleshooting

### Bot Not Found Error

If you get "Bot 'xxx' not found", check:
1. The bot ID is correct (case-insensitive)
2. The environment variable is set correctly
3. Restart your MCP client after configuration changes

### List Available Bots

Use the `list_wecom_bots` MCP tool or Python API to see all configured bots:

```python
from wecom_bot_mcp_server.bot_config import list_available_bots
print(list_available_bots())
```
