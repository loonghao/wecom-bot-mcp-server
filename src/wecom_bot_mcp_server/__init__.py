"""WeCom Bot MCP Server package."""

# Import local modules
from wecom_bot_mcp_server.__version__ import __version__
from wecom_bot_mcp_server.app import mcp
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.file import send_wecom_file
from wecom_bot_mcp_server.image import send_wecom_image
from wecom_bot_mcp_server.message import MESSAGE_HISTORY_KEY
from wecom_bot_mcp_server.message import send_message
from wecom_bot_mcp_server.message import send_wecom_template_card

__all__ = [
    "MESSAGE_HISTORY_KEY",
    "ErrorCode",
    "WeComError",
    "__version__",
    "mcp",
    "send_message",
    "send_wecom_file",
    "send_wecom_image",
    "send_wecom_template_card",
]
