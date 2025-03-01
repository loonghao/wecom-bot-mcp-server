"""Application configuration for WeCom Bot MCP Server."""

# Import third-party modules
from mcp.server.fastmcp import FastMCP

# Import local modules
from wecom_bot_mcp_server import __version__

# Constants
APP_NAME = "wecom_bot_mcp_server"
APP_DESCRIPTION = "WeCom Bot MCP Server for sending messages and files to WeCom groups."
APP_DEPENDENCIES = [
    "mcp>=1.3.0",
    "notify-bridge>=0.3.0",
    "httpx>=0.28.1",
    "ftfy>=6.3.1",
    "pillow>=10.2.0",
    "platformdirs>=4.2.0",
    "loguru>=0.7.2",
]

# Initialize FastMCP server
mcp = FastMCP(
    name=APP_NAME,
    description=APP_DESCRIPTION,
    version=__version__,
    dependencies=APP_DEPENDENCIES,
)
