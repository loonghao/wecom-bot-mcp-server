"""WeCom Bot MCP Server.

This module provides a FastMCP server for interacting with WeCom (WeChat Work) bot.
It supports sending messages and files through WeCom's webhook API.
"""

# Import built-in modules

# Import third-party modules
from loguru import logger

# Import local modules
from wecom_bot_mcp_server import __version__
from wecom_bot_mcp_server.app import APP_NAME
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.log_config import setup_logging

# Re-export tools for easier imports


def main() -> None:
    """Start the MCP server."""
    # Setup logging
    setup_logging()

    logger.info(f"Starting {APP_NAME} v{__version__}")

    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
