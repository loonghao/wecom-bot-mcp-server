# Getting Started

WeCom Bot MCP Server is a [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) compliant server that enables AI assistants to send messages to WeCom (Enterprise WeChat) groups.

## What is MCP?

The Model Context Protocol (MCP) is an open standard that allows AI assistants to interact with external tools and services. By implementing MCP, this server enables AI assistants like Claude to send messages, files, and images to WeCom groups.

## Features

- **Multiple Message Types**: Send text, markdown, images, and files
- **@Mention Support**: Mention users by ID or phone number
- **Multi-Bot Support**: Configure and use multiple WeCom bots
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **MCP Compatible**: Works with Claude Desktop, Cline, Windsurf, and more

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.10+** installed on your system
2. **WeCom Bot Webhook URL** from your WeCom group settings

### Getting Your Webhook URL

1. Open your WeCom group
2. Click the group settings (three dots in the top right)
3. Select "Group Bots"
4. Click "Add Bot" or select an existing bot
5. Copy the Webhook URL

::: warning Security Note
Keep your webhook URL secure. Anyone with this URL can send messages to your group.
:::

## Next Steps

- [Installation Guide](./installation) - Detailed installation instructions
- [Quick Start](./quick-start) - Send your first message
- [Configuration](../config/) - Configure environment variables and MCP clients
