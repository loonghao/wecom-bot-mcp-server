# Configuration Overview

WeCom Bot MCP Server can be configured through environment variables and MCP client configuration files.

## Quick Reference

| Variable | Description | Required |
|----------|-------------|----------|
| `WECOM_WEBHOOK_URL` | Default bot webhook URL | Yes (if no WECOM_BOTS) |
| `WECOM_BOTS` | JSON config for multiple bots | No |
| `WECOM_BOT_{NAME}_URL` | Individual bot URLs | No |
| `MCP_LOG_LEVEL` | Log level (DEBUG/INFO/WARNING/ERROR) | No |
| `MCP_LOG_FILE` | Custom log file path | No |

## Configuration Priority

When multiple configuration methods are used:

1. **WECOM_WEBHOOK_URL** → Creates a "default" bot
2. **WECOM_BOTS** → Adds/overrides bots from JSON
3. **WECOM_BOT_{NAME}_URL** → Adds bots if not already defined

## Sections

- [Environment Variables](./environment) - All available environment variables
- [MCP Clients](./mcp-clients) - Configuration for different MCP clients
- [Multi-Bot Setup](./multi-bot) - Configure multiple bots
