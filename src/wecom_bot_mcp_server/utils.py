"""Utility functions for WeCom Bot MCP Server."""

# Import built-in modules
from functools import lru_cache
import logging
import os

# Import third-party modules
import ftfy

# Import local modules
from wecom_bot_mcp_server.errors import ErrorCode
from wecom_bot_mcp_server.errors import WeComError


@lru_cache
def get_webhook_url() -> str:
    """Get WeCom webhook URL from environment variable.

    Returns:
        str: WeCom webhook URL

    Raises:
        WeComError: If WECOM_WEBHOOK_URL environment variable is not set

    """
    webhook_url = os.getenv("WECOM_WEBHOOK_URL")
    if not webhook_url:
        raise WeComError("WECOM_WEBHOOK_URL environment variable not set", ErrorCode.VALIDATION_ERROR)
    return webhook_url


def encode_text(text: str) -> str:
    """Encode text for sending to WeCom.

    Uses ftfy to automatically fix text encoding issues and normalize Unicode.
    Escapes special characters for proper JSON handling.

    Args:
        text: Input text that may have encoding issues

    Returns:
        str: Fixed text with proper handling of Unicode characters.

    Raises:
        ValueError: If text encoding fails

    """
    try:
        # Fix text encoding and normalize Unicode
        fixed_text = ftfy.fix_text(text)
        # Escape special characters but don't wrap in quotes
        escaped_text = fixed_text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
        return escaped_text
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error encoding text: {e!s}")
        raise ValueError(f"Failed to encode text: {e!s}") from e
