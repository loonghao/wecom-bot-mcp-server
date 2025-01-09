# WeCom Bot MCP Server

[![Python Package](https://github.com/loonghao/wecom-bot-mcp-server/actions/workflows/python-package.yml/badge.svg)](https://github.com/loonghao/wecom-bot-mcp-server/actions/workflows/python-package.yml)
[![codecov](https://codecov.io/gh/loonghao/wecom-bot-mcp-server/branch/main/graph/badge.svg)](https://codecov.io/gh/loonghao/wecom-bot-mcp-server)
[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![Downloads](https://pepy.tech/badge/wecom-bot-mcp-server)](https://pepy.tech/project/wecom-bot-mcp-server)
[![smithery badge](https://smithery.ai/badge/wecom-bot-mcp-server)](https://smithery.ai/server/wecom-bot-mcp-server)

基于 FastMCP 实现的企业微信机器人服务器，支持通过 Webhook 发送消息。

中文 | [English](README.md)

<a href="https://glama.ai/mcp/servers/amr2j23lbk"><img width="380" height="200" src="https://glama.ai/mcp/servers/amr2j23lbk/badge" alt="WeCom Bot Server MCP server" /></a>

## 特性

- **FastMCP 集成**：基于 FastMCP 框架实现，提供强大的消息处理能力
- **消息格式**：支持文本和 Markdown 格式消息
- **异步处理**：高效的异步消息发送机制，支持自动重试
- **消息历史**：内置消息历史记录和检索功能
- **错误处理**：全面的错误处理机制，支持自动重试
- **类型安全**：完整的类型提示，提供更好的开发体验
- **完整测试**：全面的单元测试覆盖
- **易于集成**：基于 Webhook 的简单集成方式
- **灵活配置**：通过环境变量进行灵活配置
- **生产就绪**：内置日志和监控功能

## 安装

### 通过 Smithery 安装（推荐）

通过 [Smithery](https://smithery.ai/server/wecom-bot-mcp-server) 为 Claude Desktop 自动安装 WeCom Bot Server：

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

### 使用 pip 安装

```bash
pip install wecom-bot-mcp-server
```

## 快速开始

1. 设置环境变量：

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL="你的企业微信机器人 Webhook URL"

# Linux/macOS
export WECOM_WEBHOOK_URL="你的企业微信机器人 Webhook URL"
```

2. 运行服务器：

```bash
# 安装后可以直接运行命令
wecom-bot-mcp-server
```

3. 在代码中使用：

```python
from wecom_bot_mcp_server.server import main, send_message, get_message_history

# 启动服务器
if __name__ == "__main__":
    main()

# 发送消息
await send_message("Hello, WeCom!")

# 发送 Markdown 格式消息
await send_message("**粗体** 和 *斜体* 文本支持")

# 获取消息历史
history = get_message_history()
```

## 高级特性

### 重试机制

服务器实现了指数退避重试机制：
- 最大重试次数：3次
- 初始等待时间：1秒
- 最大等待时间：10秒

### 消息历史

消息历史记录包含：
- 消息内容
- 时间戳
- 发送状态
- 错误信息（如果有）

### 错误处理

全面的错误处理机制，包括：
- 网络超时
- API 错误
- 无效消息格式
- 配置问题

## 客户端配置

### Claude Desktop 配置

通过 Smithery 安装后，WeCom Bot Server 将自动为 Claude Desktop 配置。你只需要在环境变量中设置 webhook URL：

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL="你的企业微信机器人 Webhook URL"
```

### Cline 配置

在 VSCode 中配置 Cline MCP 设置文件：
```
C:\Users\<用户名>\AppData\Roaming\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json
```

添加以下配置：

```json
{
  "mcpServers": {
    "wecom-bot-server": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "<你的企业微信机器人 Webhook URL>"
      },
      "alwaysAllow": [
        "send_message"
      ],
      "disabled": false
    }
  }
}
```

配置说明：
- `command`: 使用 uvx 运行服务器
- `args`: 指定要运行的服务器包
- `env.WECOM_WEBHOOK_URL`: 你的企业微信机器人 Webhook URL
- `alwaysAllow`: 无需确认即可执行的操作列表
- `disabled`: 启用/禁用服务器

## 开发

1. 克隆仓库：

```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. 运行测试：

```bash
pytest tests/ --cov=wecom_bot_mcp_server
```

3. 代码质量检查：

```bash
ruff check .
ruff format .
mypy src/wecom_bot_mcp_server --strict
```

## 要求

- Python >= 3.10
- FastMCP >= 0.4.1
- httpx >= 0.24.1

## 许可证

[MIT License](LICENSE)

## 贡献

我们欢迎各种形式的贡献！请随时提交 Issue 和 Pull Request。

### 如何贡献

1. Fork 仓库
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

请确保适当更新测试，并遵循现有的代码风格。
