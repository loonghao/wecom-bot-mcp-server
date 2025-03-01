# WeCom Bot MCP Server

<div align="center">
    <img src="wecom.png" alt="WeCom Bot Logo" width="200"/>
</div>

A Model Context Protocol (MCP) compliant server implementation for WeCom (WeChat Work) bot.

[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
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

## Requirements

- Python 3.10+
- WeCom Bot Webhook URL (obtained from WeCom group settings)

## Installation

There are several ways to install WeCom Bot MCP Server:

### 1. Automated Installation (Recommended)

#### Using Smithery (For Claude Desktop):

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

#### Using VSCode with Cline Extension:

1. Install [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) from VSCode marketplace
2. Open Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
3. Search for "Cline: Install Package"
4. Type "wecom-bot-mcp-server" and press Enter

### 2. Manual Installation

#### Install from PyPI:

```bash
pip install wecom-bot-mcp-server
```

#### Configure MCP manually:

Create or update your MCP configuration file:

```json
// For Windsurf: ~/.windsurf/config.json
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": [
        "wecom-bot-mcp-server"
      ],
      "env": {
        "WECOM_WEBHOOK_URL": "your-webhook-url"
      }
    }
  }
}
```

## Configuration

### Setting Environment Variables

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL = "your-webhook-url"

# Optional configurations
$env:MCP_LOG_LEVEL = "DEBUG"  # Log levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
$env:MCP_LOG_FILE = "path/to/custom/log/file.log"  # Custom log file path
```

### Log Management

The logging system uses `platformdirs` for cross-platform log file management:

- Windows: `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\logs`
- Linux: `~/.local/share/wecom-bot-mcp-server/logs`
- macOS: `~/Library/Application Support/wecom-bot-mcp-server/logs`

## Usage

### Starting the Server

```bash
wecom-bot-mcp-server
```

### Usage Examples (With MCP)

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
```

### Direct API Usage

#### Send Messages

```python
from wecom_bot_mcp_server import mcp

# Send markdown message
await mcp.send_message(
    content="**Hello World!**", 
    msg_type="markdown"
)

# Send text message and mention users
await mcp.send_message(
    content="Hello @user1 @user2",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)
```

#### Send Files

```python
from wecom_bot_mcp_server import send_wecom_file

# Send file
await send_wecom_file("/path/to/file.txt")
```

#### Send Images

```python
from wecom_bot_mcp_server import send_wecom_image

# Send local image
await send_wecom_image("/path/to/image.png")

# Send URL image
await send_wecom_image("https://example.com/image.png")
```

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. Create a virtual environment and install dependencies:
```bash
# Using uv (recommended)
pip install uv
uv venv
uv pip install -e ".[dev]"

# Or using traditional method
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Testing

```bash
# Using uv (recommended)
uvx nox -s pytest

# Or using traditional method
nox -s pytest
```

### Code Style

```bash
# Check code
uvx nox -s lint

# Automatically fix code style issues
uvx nox -s lint_fix
```

### Building and Publishing

```bash
# Build the package
uv build

# Build and publish to PyPI
uv build && twine upload dist/*
```

## Project Structure

```
wecom-bot-mcp-server/
├── src/
│   └── wecom_bot_mcp_server/
│       ├── __init__.py
│       ├── server.py
│       ├── message.py
│       ├── file.py
│       ├── image.py
│       ├── utils.py
│       └── errors.py
├── tests/
│   ├── test_server.py
│   ├── test_message.py
│   ├── test_file.py
│   └── test_image.py
├── docs/
├── pyproject.toml
├── noxfile.py
└── README.md
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

- Author: longhao
- Email: hal.long@outlook.com
