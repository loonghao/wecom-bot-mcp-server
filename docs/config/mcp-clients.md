# MCP Client Configuration

This guide covers configuration for various MCP-compatible clients.

## Claude Desktop

Claude Desktop is Anthropic's official desktop application with MCP support.

### Configuration File Location

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

### Basic Configuration

```json
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

### Multi-Bot Configuration

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

### Using pip Installation

If you installed via pip instead of uvx:

```json
{
  "mcpServers": {
    "wecom": {
      "command": "wecom-bot-mcp-server",
      "env": {
        "WECOM_WEBHOOK_URL": "your-webhook-url"
      }
    }
  }
}
```

## Windsurf

Windsurf is an AI-powered IDE with MCP support.

### Configuration File Location

```
~/.windsurf/config.json
```

### Configuration

```json
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

## Cline (VSCode Extension)

Cline is a VSCode extension that provides AI coding assistance with MCP support.

### Configuration Steps

1. Install [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. Open VSCode Settings (`Ctrl+,` / `Cmd+,`)
3. Search for "Cline MCP"
4. Click "Edit in settings.json"

### Configuration

```json
{
  "cline.mcpServers": {
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

### Quick Install via Cline

1. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
2. Search for "Cline: Install Package"
3. Type "wecom-bot-mcp-server"
4. Configure the webhook URL when prompted

## Cursor

Cursor is an AI-first code editor with MCP support.

### Configuration File Location

```
~/.cursor/mcp.json
```

### Configuration

```json
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

## Trae

Trae is an AI assistant with MCP support.

### Configuration

```json
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

## Common Issues

### Server Not Starting

1. **Check uvx is installed**: Run `uvx --version`
2. **Check Python version**: Requires Python 3.10+
3. **Verify webhook URL**: Ensure URL is valid and starts with `https://`

### Server Not Connecting

1. **Restart the client**: After configuration changes, restart your MCP client
2. **Check logs**: Look for errors in the client's developer console
3. **Verify JSON syntax**: Use a JSON validator for your configuration

### Messages Not Sending

1. **Check webhook URL**: Test the URL with curl or Postman
2. **Check network**: Ensure you can reach `qyapi.weixin.qq.com`
3. **Enable debug logging**: Set `MCP_LOG_LEVEL=DEBUG`

## Verification

After configuration, verify the server is working:

1. Ask your AI assistant: "What MCP tools are available?"
2. You should see `send_message`, `send_wecom_file`, `send_wecom_image`, and `list_wecom_bots`
3. Try sending a test message: "Send 'Hello from MCP!' to WeCom"
