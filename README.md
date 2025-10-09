[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/loonghao-wecom-bot-mcp-server-badge.png)](https://mseep.ai/app/loonghao-wecom-bot-mcp-server)

# WeCom Bot MCP Server

<div align="center">
    <img src="wecom.png" alt="WeCom Bot Logo" width="200"/>
</div>

A Model Context Protocol (MCP) compliant server implementation for WeCom (WeChat Work) bot.

[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![codecov](https://codecov.io/gh/loonghao/wecom-bot-mcp-server/branch/main/graph/badge.svg)](https://app.codecov.io/gh/loonghao/wecom-bot-mcp-server)
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

### 2. Manual Configuration

Add the server to your MCP client configuration file:

```json
// For Claude Desktop on macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
// For Claude Desktop on Windows: %APPDATA%\Claude\claude_desktop_config.json
// For Windsurf: ~/.windsurf/config.json
// For Cline in VSCode: VSCode Settings > Cline > MCP Settings
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

The logging system uses `platformdirs.user_log_dir()` for cross-platform log file management:

- Windows: `C:\Users\<username>\AppData\Local\hal\wecom-bot-mcp-server\Logs`
- Linux: `~/.local/state/hal/wecom-bot-mcp-server/log`
- macOS: `~/Library/Logs/hal/wecom-bot-mcp-server`

The log file is named `mcp_wecom.log` and is stored in the above directory.

You can customize the log level and file path using environment variables:
- `MCP_LOG_LEVEL`: Set to DEBUG, INFO, WARNING, ERROR, or CRITICAL
- `MCP_LOG_FILE`: Set to a custom log file path

## Usage

Once configured, the MCP server runs automatically when your MCP client starts. You can interact with it through natural language in your AI assistant.

### Usage Examples

**Scenario 1: Send weather information to WeCom**
```
USER: "How's the weather in Shenzhen today? Send it to WeCom"
ASSISTANT: "I'll check Shenzhen's weather and send it to WeCom"
[The assistant will use the send_message tool to send the weather information]
```

**Scenario 2: Send meeting reminder and @mention relevant people**
```
USER: "Send a reminder for the 3 PM project review meeting, remind Zhang San and Li Si to attend"
ASSISTANT: "I'll send the meeting reminder"
[The assistant will use the send_message tool with mentioned_list parameter]
```

**Scenario 3: Send a file**
```
USER: "Send this weekly report to the WeCom group"
ASSISTANT: "I'll send the weekly report"
[The assistant will use the send_file tool]
```

**Scenario 4: Send an image**
```
USER: "Send this chart image to WeCom"
ASSISTANT: "I'll send the image"
[The assistant will use the send_image tool]
```

### Available MCP Tools

The server provides the following tools that your AI assistant can use:

1. **send_message** - Send text or markdown messages
   - Parameters: `content`, `msg_type` (text/markdown), `mentioned_list`, `mentioned_mobile_list`

2. **send_file** - Send files to WeCom
   - Parameters: `file_path`

3. **send_image** - Send images to WeCom
   - Parameters: `image_path` (local path or URL)

### For Developers: Direct API Usage

If you want to use this package directly in your Python code (not as an MCP server):

```python
from wecom_bot_mcp_server import send_message, send_wecom_file, send_wecom_image

# Send markdown message
await send_message(
    content="**Hello World!**",
    msg_type="markdown"
)

# Send text message and mention users
await send_message(
    content="Hello @user1 @user2",
    msg_type="text",
    mentioned_list=["user1", "user2"]
)

# Send file
await send_wecom_file("/path/to/file.txt")

# Send image
await send_wecom_image("/path/to/image.png")
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
# Run all tests with coverage
uvx nox -s pytest

# Run import tests only
uvx nox -s test_imports

# Run specific test file
uvx nox -s pytest -- tests/test_message.py

# Run tests with verbose output
uvx nox -s pytest -- -v
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
uvx nox -s build

# Publish to PyPI (requires authentication)
uvx nox -s publish
```

### Continuous Integration

The project uses GitHub Actions for CI/CD:
- **MR Checks**: Runs on all pull requests, tests on Ubuntu, Windows, and macOS with Python 3.10, 3.11, and 3.12
- **Code Coverage**: Uploads coverage reports to Codecov
- **Import Tests**: Ensures the package can be imported correctly after installation

All dependencies are automatically tested during CI to catch issues early.

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
