# WeCom Bot MCP Server

[![codecov](https://codecov.io/gh/loonghao/wecom-bot-mcp-server/branch/main/graph/badge.svg)](https://codecov.io/gh/loonghao/wecom-bot-mcp-server)
[![PyPI version](https://badge.fury.io/py/wecom-bot-mcp-server.svg)](https://badge.fury.io/py/wecom-bot-mcp-server)
[![Python Version](https://img.shields.io/pypi/pyversions/wecom-bot-mcp-server.svg)](https://pypi.org/project/wecom-bot-mcp-server/)
[![Downloads](https://pepy.tech/badge/wecom-bot-mcp-server)](https://pepy.tech/project/wecom-bot-mcp-server)
[![smithery badge](https://smithery.ai/badge/wecom-bot-mcp-server)](https://smithery.ai/server/wecom-bot-mcp-server)

A WeCom (WeChat Work) bot server implemented with FastMCP, supporting message sending via webhook.

[中文文档](README_zh.md) | English

<a href="https://glama.ai/mcp/servers/amr2j23lbk"><img width="380" height="200" src="https://glama.ai/mcp/servers/amr2j23lbk/badge" alt="WeCom Bot Server MCP server" /></a>

## Features

- **FastMCP Integration**: Built on FastMCP framework for robust message handling
- **Message Formats**: Support for text and Markdown message formats
- **Asynchronous Processing**: Efficient async message sending with retry mechanism
- **Message History**: Built-in message history tracking and retrieval
- **Error Handling**: Comprehensive error handling with automatic retries
- **Type Safety**: Complete type hints for better development experience
- **Comprehensive Testing**: Extensive unit test coverage
- **Easy Integration**: Simple webhook-based integration with WeCom
- **Configurable**: Flexible configuration through environment variables
- **Production Ready**: Built-in logging and monitoring capabilities

## Installation

### Installing via Smithery (Recommended)

To install WeCom Bot Server for Claude Desktop automatically via [Smithery](https://smithery.ai/server/wecom-bot-mcp-server):

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

### Using pip

```bash
pip install wecom-bot-mcp-server
```

### Using uv

```bash
uv pip install wecom-bot-mcp-server
```

## Quick Start

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

3. Use in code:

```python
from wecom_bot_mcp_server.server import main, send_message, get_message_history

# Start server
if __name__ == "__main__":
    main()

# Send messages
await send_message("Hello, WeCom!")

# Send markdown message
await send_message("**Bold** and *italic* text supported")

# Get message history
history = get_message_history()
```

## Advanced Features

### Retry Mechanism

The server implements an exponential backoff retry mechanism for failed requests:
- Maximum retry attempts: 3
- Initial wait time: 1 second
- Maximum wait time: 10 seconds

### Message History

Message history tracking includes:
- Message content
- Timestamp
- Delivery status
- Error information (if any)

### Error Handling

Comprehensive error handling for:
- Network timeouts
- API errors
- Invalid message formats
- Configuration issues

## Client Configuration

### Claude Desktop Configuration

After installing via Smithery, the WeCom Bot Server will be automatically configured for Claude Desktop. You only need to set your webhook URL in the environment variables:

```bash
# Windows PowerShell
$env:WECOM_WEBHOOK_URL="your WeCom bot webhook URL"
```

### Cline Configuration

Configure the Cline MCP settings file in VSCode:
```
C:\Users\<username>\AppData\Roaming\Code\User\globalStorage\rooveterinaryinc.roo-cline\settings\cline_mcp_settings.json
```

Add the following configuration:

```json
{
  "mcpServers": {
    "wecom-bot-server": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
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
- `command`: Uses uvx to run the server
- `args`: Specifies the server package to run
- `env.WECOM_WEBHOOK_URL`: Your WeCom bot webhook URL
- `alwaysAllow`: List of allowed operations without confirmation
- `disabled`: Enable/disable the server

## Development

1. Clone repository:

```bash
git clone https://github.com/loonghao/wecom-bot-mcp-server.git
cd wecom-bot-mcp-server
```

2. Run tests:

```bash
pytest tests/ --cov=wecom_bot_mcp_server
```

3. Code quality checks:

```bash
ruff check .
ruff format .
mypy src/wecom_bot_mcp_server --strict
```

## Requirements

- Python >= 3.10
- FastMCP >= 0.4.1
- httpx >= 0.24.1

## License

[MIT License](LICENSE)

## Contributing

We welcome contributions! Please feel free to submit issues and pull requests.

### How to Contribute

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

Please make sure to update tests as appropriate and follow the existing coding style.
