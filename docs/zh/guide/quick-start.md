# 快速上手

本指南将帮助您使用 AI 助手向企业微信发送第一条消息。

## 步骤 1：获取 Webhook URL

1. 打开企业微信群组
2. 进入群设置 → 群机器人 → 添加机器人
3. 复制 Webhook URL（格式：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx`）

## 步骤 2：配置 MCP 客户端

将服务器添加到您的 MCP 客户端配置：

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
// VSCode 设置 > Cline > MCP Settings
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

## 步骤 3：重启 MCP 客户端

保存配置后，重启您的 AI 助手（Claude Desktop、Cline 等）以加载新服务器。

## 步骤 4：发送第一条消息

现在您可以让 AI 助手向企业微信发送消息：

### 示例提示词

**发送简单消息：**
```
发送 "Hello from AI!" 到企业微信
```

**发送 Markdown 消息：**
```
发送一条 Markdown 消息到企业微信，包含今天的天气预报
```

**带 @提及：**
```
发送会议提醒到企业微信，并提及 user1 和 user2
```

**发送文件：**
```
把 report.pdf 文件发送到企业微信
```

## 使用示例

### 场景一：天气更新
```
USER: "深圳今天天气怎么样？发送到企业微信"
ASSISTANT: "我会查询深圳天气并发送到企业微信"
[使用 send_message 工具发送天气信息]
```

### 场景二：会议提醒带 @提及
```
USER: "发送下午3点项目评审会议提醒，提及张三和李四"
ASSISTANT: "好的，我来发送会议提醒"
[使用 send_message 工具，带 mentioned_list 参数]
```

### 场景三：发送图片
```
USER: "把这个图表发送到企业微信"
ASSISTANT: "好的，我来发送图片"
[使用 send_image 工具]
```

## 下一步

- [消息类型](./message-types) - 了解所有支持的消息类型
- [多机器人支持](./multi-bot) - 配置多个机器人
- [环境变量](../config/environment) - 高级配置选项
