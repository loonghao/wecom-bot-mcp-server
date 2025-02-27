# WeCom Bot MCP Server

<div align="center">
    <img src="wecom.png" alt="WeCom Bot Logo" width="200"/>
</div>

A Model Context Protocol (MCP) compliant server implementation for WeCom (WeChat Work) bot.

[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![smithery badge](https://smithery.ai/badge/wecom-bot-mcp-server)](https://smithery.ai/server/wecom-bot-mcp-server)

[English](README.md) | [中文](README_zh.md)

<a href="https://glama.ai/mcp/servers/amr2j23lbk"><img width="380" height="200" src="https://glama.ai/mcp/servers/amr2j23lbk/badge" alt="WeCom Bot Server MCP server" /></a>


## Features

- Support for multiple message types:
  - Text messages
  - Markdown messages
  - Image messages (base64)
  - File messages
- @mention support (via user ID or phone number)
- Message history tracking
- Configurable logging system
- Full type annotations
- Pydantic-based data validation

## Quick Start

### Requirements

- Python 3.10+
- WeCom Bot Webhook URL

### Installation

There are several ways to install the WeCom Bot MCP Server:

To install WeCom Bot Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/wecom-bot-mcp-server):

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

2. Using VSCode with [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev):

- Install Cline extension from VSCode marketplace
- Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
- Search for "Cline: Install Package"
- Type "wecom-bot-mcp-server" and press Enter

### Configuration

1. Set required environment variables:
```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "your-webhook-url"

# Optional configurations
$env:MCP_LOG_LEVEL = "DEBUG"  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
```

2. Logging configuration:
- Default log location: `mcp_wecom.log` in system log directory
- Custom log location can be set via `MCP_LOG_FILE` environment variable

### Usage Examples

Using in MCP environment:

```python
# Scenario 1: Send weather information to WeCom
USER: "How's the weather in Shenzhen today? Send it to WeCom"
ASSISTANT: "I'll check Shenzhen's weather and send it to WeCom"

await mcp.send_message(
    content="Shenzhen Weather:\n- Temperature: 25°C\n- Weather: Sunny\n- Air Quality: Good",
    msg_type="markdown"
)

# Scenario 2: Send meeting reminder and @mention relevant people
USER: "Send a reminder for the 3 PM project review meeting, remind Zhang San and Li Si to attend"
ASSISTANT: "I'll send the meeting reminder"

await mcp.send_message(
    content="## Project Review Meeting Reminder\n\nTime: Today 3:00 PM\nLocation: Meeting Room A\n\nPlease be on time!",
    msg_type="markdown",
    mentioned_list=["zhangsan", "lisi"]
)

# Scenario 3: Send a file
USER: "Send this weekly report to the WeCom group"
ASSISTANT: "I'll send the weekly report"

await mcp.send_message(
    content=Path("weekly_report.docx"),
    msg_type="file"
)

## Development

### Prerequisites

- Python 3.10+
- uv (Python package installer)

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. Install dependencies using uv:
```bash
uv venv
uv pip install -e ".[dev]"
```

3. Run tests:
```bash
uvx nox -s test
```

4. Run linting:
```bash
uvx nox -s lint
```

## Project Structure

```
wecom-bot-mcp-server/
├── src/
│   └── wecom_bot_mcp_server/
│       ├── __init__.py
│       └── server.py
├── tests/
│   └── test_server.py
├── docs/
├── pyproject.toml
└── README.md
```

## Log Management

The logging system uses `platformdirs` for cross-platform log file management:

- Windows: `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\logs`
- Linux: `~/.local/share/wecom-bot-mcp-server/logs`
- macOS: `~/Library/Application Support/wecom-bot-mcp-server/logs`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Author: longhao
- Email: hal.long@outlook.com
