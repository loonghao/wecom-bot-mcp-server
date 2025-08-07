"""Application configuration for WeCom Bot MCP Server."""

# Import third-party modules
from mcp.server.fastmcp import FastMCP

# Constants
APP_NAME = "wecom_bot_mcp_server"
APP_DESCRIPTION = "WeCom Bot MCP Server for sending messages and files to WeCom groups."

# Initialize FastMCP server
mcp = FastMCP(
    name=APP_NAME,
    instructions=APP_DESCRIPTION,
)
