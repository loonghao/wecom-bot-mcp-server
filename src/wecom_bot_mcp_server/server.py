"""WeCom Bot MCP Server.

This module provides a FastMCP server for interacting with WeCom (WeChat Work) bot.
It supports sending messages and files through WeCom's webhook API.
"""

# Import built-in modules
import os

# Import third-party modules
from loguru import logger

# Import local modules
from wecom_bot_mcp_server import __version__
from wecom_bot_mcp_server.app import APP_NAME
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.log_config import setup_logging

# Re-export tools for easier imports

_SHELL_FUNCTION_NAMES = ("ml", "module", "scl", "switchml", "which")


def _sanitize_shell_function_env() -> None:
    """Remove exported shell functions that break non-interactive shells."""
    for key in list(os.environ):
        if key.startswith("BASH_FUNC_") and key.endswith("%%"):
            os.environ.pop(key, None)
            continue
        if key.lower() in _SHELL_FUNCTION_NAMES and os.environ.get(key, "").startswith("() {"):
            os.environ.pop(key, None)


def main() -> None:
    """Start the MCP server."""
    _sanitize_shell_function_env()

    # Setup logging
    setup_logging()

    logger.info(f"Starting {APP_NAME} v{__version__}")

    # Run the MCP server
    mcp.run()


if __name__ == "__main__":
    main()
