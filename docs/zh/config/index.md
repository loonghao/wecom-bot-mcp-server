# 配置概述

WeCom Bot MCP Server 可以通过环境变量和 MCP 客户端配置文件进行配置。

## 快速参考

| 变量 | 描述 | 必需 |
|------|------|------|
| `WECOM_WEBHOOK_URL` | 默认机器人 webhook URL | 是（如无 WECOM_BOTS） |
| `WECOM_BOTS` | 多机器人 JSON 配置 | 否 |
| `WECOM_BOT_{NAME}_URL` | 单独机器人 URL | 否 |
| `MCP_LOG_LEVEL` | 日志级别 | 否 |
| `MCP_LOG_FILE` | 自定义日志文件路径 | 否 |

## 配置优先级

当使用多种配置方式时：

1. **WECOM_WEBHOOK_URL** → 创建 "default" 机器人
2. **WECOM_BOTS** → 从 JSON 添加/覆盖机器人
3. **WECOM_BOT_{NAME}_URL** → 如果未定义则添加机器人

## 章节

- [环境变量](./environment) - 所有可用的环境变量
- [MCP 客户端](./mcp-clients) - 不同 MCP 客户端的配置
- [多机器人配置](./multi-bot) - 配置多个机器人
