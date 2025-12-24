# Environment Variables

Complete reference for all environment variables supported by WeCom Bot MCP Server.

## Bot Configuration

### WECOM_WEBHOOK_URL

The webhook URL for the default bot. This is the simplest configuration for single-bot setups.

```bash
# Linux/macOS
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"

# Windows CMD
set WECOM_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY
```

### WECOM_BOTS

JSON configuration for multiple bots. This is the recommended way to configure multiple bots.

**Format:**
```json
{
  "bot_id": {
    "name": "Human-readable name",
    "webhook_url": "https://...",
    "description": "Optional description"
  }
}
```

**Example:**
```bash
export WECOM_BOTS='{
  "alert": {
    "name": "Alert Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx",
    "description": "For system alerts and notifications"
  },
  "ci": {
    "name": "CI/CD Bot",
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy",
    "description": "For build and deployment notifications"
  }
}'
```

### WECOM_BOT_\{NAME\}_URL

Individual environment variables for each bot. The bot ID is derived from the variable name.

```bash
# Creates bot with id "alert"
export WECOM_BOT_ALERT_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"

# Creates bot with id "ci"
export WECOM_BOT_CI_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=yyy"

# Creates bot with id "devops"
export WECOM_BOT_DEVOPS_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=zzz"
```

## Logging Configuration

### MCP_LOG_LEVEL

Set the logging verbosity level.

| Value | Description |
|-------|-------------|
| `DEBUG` | Detailed debug information |
| `INFO` | General operational information (default) |
| `WARNING` | Warning messages only |
| `ERROR` | Error messages only |
| `CRITICAL` | Critical errors only |

```bash
export MCP_LOG_LEVEL="DEBUG"
```

### MCP_LOG_FILE

Custom path for the log file. If not set, logs are stored in platform-specific directories.

```bash
export MCP_LOG_FILE="/var/log/wecom-bot/mcp.log"
```

**Default log locations:**

| Platform | Default Path |
|----------|--------------|
| Windows | `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\Logs\mcp_wecom.log` |
| Linux | `~/.local/state/hal/wecom-bot-mcp-server/log/mcp_wecom.log` |
| macOS | `~/Library/Logs/hal/wecom-bot-mcp-server/mcp_wecom.log` |

## Configuration Examples

### Single Bot Setup

```bash
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
export MCP_LOG_LEVEL="INFO"
```

### Multi-Bot Setup with JSON

```bash
export WECOM_BOTS='{
  "default": {"name": "General", "webhook_url": "https://...?key=default"},
  "alert": {"name": "Alerts", "webhook_url": "https://...?key=alert"},
  "ci": {"name": "CI/CD", "webhook_url": "https://...?key=ci"}
}'
```

### Multi-Bot Setup with Individual Variables

```bash
export WECOM_WEBHOOK_URL="https://...?key=default"
export WECOM_BOT_ALERT_URL="https://...?key=alert"
export WECOM_BOT_CI_URL="https://...?key=ci"
```

### Production Setup

```bash
export WECOM_WEBHOOK_URL="https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx"
export MCP_LOG_LEVEL="WARNING"
export MCP_LOG_FILE="/var/log/wecom-bot/mcp.log"
```

## Validation

The server validates all configuration on startup:

- Webhook URLs must start with `http://` or `https://`
- Bot IDs are case-insensitive (stored as lowercase)
- Invalid configurations are logged but don't prevent startup

::: warning
If no valid bot configuration is found, the server will start but all message operations will fail with an error.
:::
