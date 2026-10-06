---
layout: home

hero:
  name: "WeCom Bot MCP Server"
  text: "企业微信机器人 AI 助手"
  tagline: 一个遵循 Model Context Protocol (MCP) 的企业微信机器人服务器
  image:
    src: /logo.png
    alt: WeCom Bot Logo
  actions:
    - theme: brand
      text: 快速开始
      link: /zh/guide/getting-started
    - theme: alt
      text: GitHub
      link: https://github.com/loonghao/wecom-bot-mcp-server

features:
  - icon: 📝
    title: 多种消息类型
    details: 支持文本、Markdown、图片和文件消息，以及 @提及功能
  - icon: 🤖
    title: 多机器人支持
    details: 配置和管理多个企业微信机器人，灵活路由消息
  - icon: 🔌
    title: MCP 兼容
    details: 与 Claude Desktop、Cline、Windsurf 等 MCP 客户端无缝集成
  - icon: 🐍
    title: Python 原生
    details: 基于 Python 3.10+ 构建，完整类型注解，Pydantic 数据验证
  - icon: ⚡
    title: 简单配置
    details: 通过 pip、uvx 或 Smithery 简单安装，最小化配置
  - icon: 🔒
    title: 生产就绪
    details: 完善的日志记录、错误处理和重试机制
---

## 快速安装

::: code-group

```bash [Smithery（推荐）]
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

```bash [pip]
pip install wecom-bot-mcp-server
```

```bash [uvx]
uvx wecom-bot-mcp-server
```

:::

## 基本配置

```json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "your-webhook-url"
      }
    }
  }
}
```

## 多机器人配置

配置多个机器人用于不同用途（告警、CI/CD、团队通知）：

::: code-group

```json [MCP 客户端配置]
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default",
        "WECOM_BOTS": "{\"alert\": {\"name\": \"告警机器人\", \"webhook_url\": \"https://...?key=alert\"}, \"ci\": {\"name\": \"CI 机器人\", \"webhook_url\": \"https://...?key=ci\"}}"
      }
    }
  }
}
```

```bash [环境变量]
# JSON 配置（推荐）
export WECOM_BOTS='{
  "alert": {"name": "告警机器人", "webhook_url": "https://...?key=alert"},
  "ci": {"name": "CI 机器人", "webhook_url": "https://...?key=ci"}
}'

# 或使用独立变量
export WECOM_BOT_ALERT_URL="https://...?key=alert"
export WECOM_BOT_CI_URL="https://...?key=ci"
```

:::

::: tip JSON 转义工具
`WECOM_BOTS` 的值需要进行 JSON 转义。可使用以下在线工具转换：
- [JSON Escape/Unescape](https://jsonviewertool.com/json-escape)
- [JSON String Escape](https://jsontostring.com/)

使用 `list_wecom_bots` 工具查看所有已配置的机器人。[了解更多 →](/zh/guide/multi-bot)
:::
