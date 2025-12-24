# Multi-Bot Configuration

Detailed guide for configuring multiple WeCom bots.

## Configuration Methods

### Method 1: WECOM_BOTS JSON (Recommended)

The most flexible way to configure multiple bots:

```json
{
  "bot_id": {
    "name": "Display Name",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "description": "Optional description for AI context"
  }
}
```

**Full Example:**

::: code-group

```bash [Linux/macOS]
export WECOM_BOTS='{
  "default": {
    "name": "General Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=general",
    "description": "For general announcements"
  },
  "alert": {
    "name": "Alert Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert",
    "description": "For system alerts and critical notifications"
  },
  "ci": {
    "name": "CI/CD Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci",
    "description": "For build, test, and deployment notifications"
  },
  "team-frontend": {
    "name": "Frontend Team",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=frontend",
    "description": "Frontend team group"
  },
  "team-backend": {
    "name": "Backend Team",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=backend",
    "description": "Backend team group"
  }
}'
```

```powershell [Windows PowerShell]
$env:WECOM_BOTS = '{"default": {"name": "General Bot", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=general"}, "alert": {"name": "Alert Bot", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"}, "ci": {"name": "CI/CD Bot", "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci"}}'
```

:::

### Method 2: Individual Environment Variables

For simpler setups or when you can't use JSON:

```bash
# Each variable creates a bot with the ID from the variable name
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci"
export WECOM_BOT_DEVOPS_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=devops"
```

**Naming Rules:**
- Pattern: `WECOM_BOT_{NAME}_URL`
- `{NAME}` becomes the bot ID (converted to lowercase)
- Example: `WECOM_BOT_MY_TEAM_URL` → bot ID: `my_team`

### Method 3: Combined Configuration

Mix `WECOM_WEBHOOK_URL` with other methods:

```bash
# This becomes the "default" bot
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default"

# Additional bots
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert"
export WECOM_BOTS='{"ci": {"name": "CI Bot", "webhook_url": "https://..."}}'
```

## MCP Client Configuration

### Claude Desktop

```json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_BOTS": "{\"alert\": {\"name\": \"Alert Bot\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert\", \"description\": \"For alerts\"}, \"ci\": {\"name\": \"CI Bot\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci\", \"description\": \"For CI/CD\"}}"
      }
    }
  }
}
```

::: tip JSON Escaping
In JSON config files, you need to escape the inner JSON string. Use `\"` for quotes inside the WECOM_BOTS value.
:::

## Bot ID Guidelines

- **Use lowercase**: Bot IDs are case-insensitive and stored as lowercase
- **Use descriptive names**: `alert`, `ci`, `team-frontend` are better than `bot1`, `bot2`
- **Avoid special characters**: Stick to letters, numbers, hyphens, and underscores
- **Reserve "default"**: The `default` bot is used when no `bot_id` is specified

## Descriptions for AI Context

The `description` field helps AI assistants choose the right bot:

```json
{
  "alert": {
    "name": "Alert Bot",
    "webhook_url": "https://...",
    "description": "Use for system alerts, errors, and critical notifications"
  },
  "ci": {
    "name": "CI Bot",
    "webhook_url": "https://...",
    "description": "Use for build results, test reports, and deployment status"
  }
}
```

When you ask the AI "send a build notification", it will intelligently choose the CI bot.

## Loading Priority

When the same bot ID is defined multiple times:

1. **WECOM_WEBHOOK_URL** → `default` bot (loaded first)
2. **WECOM_BOTS** → Can override `default` and add more
3. **WECOM_BOT_{NAME}_URL** → Only adds if not already defined

## Verification

### List All Bots

Ask your AI assistant:
```
What WeCom bots are available?
```

Or use Python:
```python
from wecom_bot_mcp_server.bot_config import list_available_bots
print(list_available_bots())
```

### Check Specific Bot

```python
from wecom_bot_mcp_server.bot_config import get_bot_registry

registry = get_bot_registry()
if registry.has_bot("alert"):
    print("Alert bot is configured")
    print(f"URL: {registry.get_webhook_url('alert')}")
```

## Troubleshooting

### Bot Not Found

```
Error: Bot 'xxx' not found. Available bots: default, alert, ci
```

**Solutions:**
1. Check the bot ID spelling (case-insensitive)
2. Verify the environment variable is set
3. Restart the MCP client

### Invalid JSON

```
Warning: Invalid JSON in WECOM_BOTS
```

**Solutions:**
1. Validate your JSON with a JSON validator
2. Check for proper escaping in config files
3. Use single quotes around the JSON value in shell

### Empty Webhook URL

```
Error: Bot 'xxx' has empty webhook_url
```

**Solutions:**
1. Check the webhook URL is not empty
2. Verify the URL format is correct
3. Ensure no extra whitespace in the URL
