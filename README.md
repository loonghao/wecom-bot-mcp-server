# WeCom Bot MCP Server

[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![codecov](https://codecov.io/gh/loonghao/wecom-bot-mcp-server/branch/main/graph/badge.svg)](https://codecov.io/gh/loonghao/wecom-bot-mcp-server)
[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![Downloads](https://pepy.tech/badge/wecom-bot-mcp-server)](https://pepy.tech/project/wecom-bot-mcp-server)
[![smithery badge](https://smithery.ai/badge/wecom-bot-mcp-server)](https://smithery.ai/server/wecom-bot-mcp-server)

A WeCom (WeChat Work) bot server implemented with FastMCP, supporting message sending via webhook.

[中文文档](README_zh.md) | English

## Features

- Built on FastMCP framework
- Markdown message format support
- Asynchronous message sending
- Message history tracking
- Complete type hints
- Comprehensive unit tests

<a href="https://glama.ai/mcp/servers/amr2j23lbk"><img width="380" height="200" src="https://glama.ai/mcp/servers/amr2j23lbk/badge" alt="WeCom Bot Server MCP server" /></a>

## Installation

### Installing via Smithery

To install WeCom Bot Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/wecom-bot-mcp-server):

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

Using pip:

```bash
pip install wecom-bot-mcp-server
```

Or using poetry (recommended):

```bash
poetry add wecom-bot-mcp-server
```

## Usage

1. Set environment variable:

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL="your WeCom bot webhook URL"

# Linux/macOS
export WECOM_WEBHOOK_URL="your WeCom bot webhook URL"
```

2. Run the server:

```bash
# Run directly after installation
wecom-bot-mcp-server
```

Or use in code:

```python
from wecom_bot_mcp_server.server import main

# Start server
if __name__ == "__main__":
    main()
```

3. Send messages:

```python
from wecom_bot_mcp_server.server import send_message, get_message_history

# Send a message
await send_message("Hello, WeCom!")

# Get message history
history = get_message_history()
```

## Cline Configuration

1. Install dependency:

```bash
poetry add wecom-bot-mcp-server
```

2. Configure Cline MCP settings:

Configure the Cline MCP settings file in VSCode. File location:
- Windows: `%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`

Add the following configuration:

```json
{
  "mcpServers": {
    "wecom-bot-server": {
      "command": "wecom-bot-mcp-server",
      "args": [],
      "env": {
        "WECOM_WEBHOOK_URL": "<your WeCom bot webhook URL>"
      },
      "alwaysAllow": [
        "send_message"
      ],
      "disabled": false
    }
  }
}
```

Configuration notes:
- `command`: Uses the installed command-line tool
- `env.WECOM_WEBHOOK_URL`: Replace with your actual WeCom bot webhook URL

## Development

1. Clone repository:

```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. Install poetry and dependencies:

```bash
pip install poetry
poetry install --with dev
```

3. Run tests:

```bash
poetry run pytest tests/ --cov=wecom_bot_mcp_server
```

4. Code checks:

```bash
poetry run ruff check .
poetry run ruff format .
poetry run mypy src/wecom_bot_mcp_server --strict
```

## Requirements

- Python >= 3.10
- FastMCP >= 0.4.1
- httpx >= 0.24.1

## License

[MIT License](LICENSE)

## Contributing

Issues and Pull Requests are welcome!

---

# WeCom Bot MCP Server (中文)

[English](#wecom-bot-mcp-server) | 中文

## 特性

- 基于 FastMCP 框架实现
- 支持 Markdown 格式消息
- 异步消息发送
- 消息历史记录
- 完整的类型提示
- 全面的单元测试

## 安装

### 使用 Smithery 安装

通过 [Smithery](https://smithery.ai/server/wecom-bot-mcp-server) 为 Claude Desktop 自动安装 WeCom Bot Server：

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

使用 pip 安装：

```bash
pip install wecom-bot-mcp-server
```

或者使用 poetry 安装（推荐）：

```bash
poetry add wecom-bot-mcp-server
```

## 使用方法

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

或者在代码中使用：

```python
from wecom_bot_mcp_server.server import main

# 启动服务器
if __name__ == "__main__":
    main()
```

3. 发送消息：

```python
from wecom_bot_mcp_server.server import send_message, get_message_history

# 发送消息
await send_message("Hello, WeCom!")

# 获取消息历史
history = get_message_history()
```

## 在 Cline 中配置

1. 安装依赖：

```bash
poetry add wecom-bot-mcp-server
```

2. 配置 Cline MCP 设置：

在 VSCode 中，需要配置 Cline MCP 设置文件。文件位置：
- Windows: `%APPDATA%\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json`

添加以下配置：

```json
{
  "mcpServers": {
    "wecom-bot-server": {
      "command": "wecom-bot-mcp-server",
      "args": [],
      "env": {
        "WECOM_WEBHOOK_URL": "<你的企业微信机器人Webhook URL>"
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
- `command`: 使用安装后的命令行工具
- `env.WECOM_WEBHOOK_URL`: 替换为你的企业微信机器人实际的 Webhook URL

## 开发

1. 克隆仓库：

```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. 安装 poetry 和依赖：

```bash
pip install poetry
poetry install --with dev
```

3. 运行测试：

```bash
poetry run pytest tests/ --cov=wecom_bot_mcp_server
```

4. 代码检查：

```bash
poetry run ruff check .
poetry run ruff format .
poetry run mypy src/wecom_bot_mcp_server --strict
```

## 要求

- Python >= 3.10
- FastMCP >= 0.4.1
- httpx >= 0.24.1

## 许可证

[MIT License](LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request！
