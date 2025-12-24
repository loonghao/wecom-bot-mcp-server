# MCP 客户端配置

本指南涵盖各种 MCP 兼容客户端的配置。

## Claude Desktop

Claude Desktop 是 Anthropic 官方支持 MCP 的桌面应用程序。

### 配置文件位置

| 平台 | 路径 |
|------|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

### 基本配置

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

### 多机器人配置

```json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default",
        "WECOM_BOTS": "{\"alert\": {\"name\": \"告警机器人\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=alert\"}, \"ci\": {\"name\": \"CI 机器人\", \"webhook_url\": \"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ci\"}}"
      }
    }
  }
}
```

## Windsurf

Windsurf 是支持 MCP 的 AI 驱动 IDE。

### 配置文件位置

```
~/.windsurf/config.json
```

### 配置

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

## Cline (VSCode 插件)

Cline 是提供 AI 编码辅助和 MCP 支持的 VSCode 插件。

### 配置步骤

1. 安装 [Cline 插件](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
2. 打开 VSCode 设置（`Ctrl+,` / `Cmd+,`）
3. 搜索 "Cline MCP"
4. 点击 "在 settings.json 中编辑"

### 配置

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

## Cursor

Cursor 是支持 MCP 的 AI 优先代码编辑器。

### 配置文件位置

```
~/.cursor/mcp.json
```

### 配置

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

## 常见问题

### 服务器无法启动

1. **检查 uvx 是否安装**：运行 `uvx --version`
2. **检查 Python 版本**：需要 Python 3.10+
3. **验证 webhook URL**：确保 URL 有效且以 `https://` 开头

### 服务器无法连接

1. **重启客户端**：配置更改后重启 MCP 客户端
2. **检查日志**：查看客户端开发者控制台的错误
3. **验证 JSON 语法**：使用 JSON 验证器检查配置

### 消息发送失败

1. **检查 webhook URL**：用 curl 或 Postman 测试 URL
2. **检查网络**：确保可以访问 `qyapi.weixin.qq.com`
3. **启用调试日志**：设置 `MCP_LOG_LEVEL=DEBUG`

## 验证

配置后，验证服务器是否正常工作：

1. 问 AI 助手："有哪些 MCP 工具可用？"
2. 应该看到 `send_message`、`send_wecom_file`、`send_wecom_image` 和 `list_wecom_bots`
3. 尝试发送测试消息："发送 'Hello from MCP!' 到企业微信"
