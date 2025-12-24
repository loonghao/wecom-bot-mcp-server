# Quick Start

This guide will help you send your first message to WeCom using an AI assistant.

## Step 1: Get Your Webhook URL

1. Open your WeCom group
2. Go to Group Settings → Group Bots → Add Bot
3. Copy the Webhook URL (format: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx`)

## Step 2: Configure Your MCP Client

Add the server to your MCP client configuration:

::: code-group

```json [Claude Desktop (macOS)]
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
      }
    }
  }
}
```

```json [Claude Desktop (Windows)]
// %APPDATA%\Claude\claude_desktop_config.json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
      }
    }
  }
}
```

```json [Windsurf]
// ~/.windsurf/config.json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
      }
    }
  }
}
```

```json [Cline (VSCode)]
// VSCode Settings > Cline > MCP Settings
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
      }
    }
  }
}
```

:::

## Step 3: Restart Your MCP Client

After saving the configuration, restart your AI assistant (Claude Desktop, Cline, etc.) to load the new server.

## Step 4: Send Your First Message

Now you can ask your AI assistant to send messages to WeCom:

### Example Prompts

**Send a simple message:**
```
Send "Hello from AI!" to WeCom
```

**Send a markdown message:**
```
Send a markdown message to WeCom with today's weather forecast
```

**Send with @mentions:**
```
Send a meeting reminder to WeCom and mention user1 and user2
```

**Send a file:**
```
Send the file report.pdf to WeCom
```

## Usage Examples

### Scenario 1: Weather Update
```
USER: "What's the weather in Shenzhen today? Send it to WeCom"
ASSISTANT: "I'll check Shenzhen's weather and send it to WeCom"
[Uses send_message tool to send weather information]
```

### Scenario 2: Meeting Reminder with @mentions
```
USER: "Send a reminder for the 3 PM project review, mention Zhang San and Li Si"
ASSISTANT: "I'll send the meeting reminder"
[Uses send_message with mentioned_list parameter]
```

### Scenario 3: Send an Image
```
USER: "Send this chart image to WeCom"
ASSISTANT: "I'll send the image"
[Uses send_image tool]
```

## Next Steps

- [Message Types](./message-types) - Learn about all supported message types
- [Multi-Bot Support](./multi-bot) - Configure multiple bots
- [Environment Variables](../config/environment) - Advanced configuration options
