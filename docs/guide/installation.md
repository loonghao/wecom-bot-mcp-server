# Installation

There are several ways to install WeCom Bot MCP Server depending on your use case.

## Automated Installation (Recommended)

### Using Smithery

For Claude Desktop users, Smithery provides the easiest installation:

```bash
npx -y @smithery/cli install wecom-bot-mcp-server --client claude
```

### Using Cline Extension

1. Install [Cline Extension](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev) from VSCode marketplace
2. Open Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`)
3. Search for "Cline: Install Package"
4. Type "wecom-bot-mcp-server" and press Enter

## Manual Installation

### Using pip

```bash
pip install wecom-bot-mcp-server
```

### Using uv (Recommended for Python users)

```bash
# Install uv if you haven't
pip install uv

# Run directly without installation
uvx wecom-bot-mcp-server
```

### Using pipx

```bash
pipx install wecom-bot-mcp-server
```

## Docker Installation

```bash
docker pull loonghao/wecom-bot-mcp-server

docker run -e WECOM_WEBHOOK_URL="your-webhook-url" loonghao/wecom-bot-mcp-server
```

## Verify Installation

After installation, verify it works:

```bash
# Check version
wecom-bot-mcp-server --version

# Or using uvx
uvx wecom-bot-mcp-server --version
```

## Next Steps

- [Quick Start](./quick-start) - Configure and send your first message
- [MCP Client Configuration](../config/mcp-clients) - Set up your AI assistant
