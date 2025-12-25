---
layout: home

hero:
  name: "WeCom Bot MCP Server"
  text: "Enterprise WeChat Bot for AI Assistants"
  tagline: A Model Context Protocol (MCP) compliant server for WeCom Bot
  image:
    src: /logo.png
    alt: WeCom Bot Logo
  actions:
    - theme: brand
      text: Get Started
      link: /guide/getting-started
    - theme: alt
      text: View on GitHub
      link: https://github.com/loonghao/wecom-bot-mcp-server

features:
  - icon: 📝
    title: Multiple Message Types
    details: Support for text, markdown, image, and file messages with @mention capabilities
  - icon: 🤖
    title: Multi-Bot Support
    details: Configure and manage multiple WeCom bots with flexible routing
  - icon: 🔌
    title: MCP Compatible
    details: Works seamlessly with Claude Desktop, Cline, Windsurf, and other MCP clients
  - icon: 🐍
    title: Python Native
    details: Built with Python 3.10+, full type annotations, and Pydantic validation
  - icon: ⚡
    title: Easy Setup
    details: Simple installation via pip, uvx, or Smithery with minimal configuration
  - icon: 🔒
    title: Production Ready
    details: Comprehensive logging, error handling, and retry mechanisms
---

## Quick Installation

::: code-group

```bash [Smithery (Recommended)]
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

```bash [pip]
pip install wecom-bot-mcp-server
```

```bash [uvx]
uvx wecom-bot-mcp-server
```

:::

## Basic Configuration

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

## Multi-Bot Configuration

Configure multiple bots for different purposes (alerts, CI/CD, team updates):

::: code-group

```json [MCP Client Config]
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=default",
        "WECOM_BOTS": "{\"alert\": {\"name\": \"Alert Bot\", \"webhook_url\": \"https://...?key=alert\"}, \"ci\": {\"name\": \"CI Bot\", \"webhook_url\": \"https://...?key=ci\"}}"
      }
    }
  }
}
```

```bash [Environment Variables]
# JSON configuration (recommended)
export WECOM_BOTS='{
  "alert": {"name": "Alert Bot", "webhook_url": "https://...?key=alert"},
  "ci": {"name": "CI Bot", "webhook_url": "https://...?key=ci"}
}'

# Or individual variables
export WECOM_BOT_ALERT_URL="https://...?key=alert"
export WECOM_BOT_CI_URL="https://...?key=ci"
```

:::

::: tip JSON Escape Tools
The `WECOM_BOTS` value requires JSON escaping. Use these online tools to convert your JSON:
- [JSON Escape/Unescape](https://www.freeformatter.com/json-escape.html)
- [JSON String Escape](https://jsontostring.com/)

Use `list_wecom_bots` tool to discover all configured bots. [Learn more →](/guide/multi-bot)
:::
