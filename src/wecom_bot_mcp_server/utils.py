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

    This function maintains backward compatibility. For multi-bot support,
    use `get_webhook_url_for_bot()` from `bot_config` module.

    Returns:
        str: WeCom webhook URL

    Raises:
        WeComError: If WECOM_WEBHOOK_URL environment variable is not set
        or if URL does not include http:// or https:// protocol

    """
    webhook_url = os.getenv("WECOM_WEBHOOK_URL")
    if not webhook_url:
        raise WeComError("WECOM_WEBHOOK_URL environment variable not set", ErrorCode.VALIDATION_ERROR)

    # Validate URL protocol
    if not webhook_url.startswith("http://") and not webhook_url.startswith("https://"):
        raise WeComError(
            f"WECOM_WEBHOOK_URL must start with 'http://' or 'https://'. Got: '{webhook_url}'",
            ErrorCode.VALIDATION_ERROR,
        )

    return webhook_url


def get_webhook_url_for_bot(bot_id: str | None = None) -> str:
    """Get webhook URL for a specific bot.

    This function supports multi-bot configuration while maintaining
    backward compatibility with single-bot setups.

    Args:
        bot_id: Bot identifier. If None or empty, returns the default bot's URL.
            For single-bot setups, this parameter is ignored.

    Returns:
        str: The webhook URL for the specified bot

    Raises:
        WeComError: If bot is not found or no bots are configured

    """
    # Import here to avoid circular imports
    # Import local modules
    from wecom_bot_mcp_server.bot_config import get_bot_registry

    return get_bot_registry().get_webhook_url(bot_id)


def encode_text(text: str, msg_type: str = "text") -> str:
    """Encode text for sending to WeCom.

    Uses ftfy to automatically fix text encoding issues and normalize Unicode.
    Escapes special characters for proper JSON handling.

    Args:
        text: Input text that may have encoding issues
        msg_type: Message type (text, markdown, etc.)

    Returns:
        str: Fixed text with proper handling of Unicode characters.

    Raises:
        ValueError: If text encoding fails

    """
    try:
        logger = logging.getLogger(__name__)
        logger.debug(f"Encoding {msg_type} message: {text[:100]}{'...' if len(text) > 100 else ''}")

        # Fix text encoding and normalize Unicode
        fixed_text = ftfy.fix_text(text)

        # For markdown messages, preserve newlines and tabs
        if msg_type.lower() in {"markdown", "markdown_v2"}:
            # Only escape backslashes and double quotes, preserve newlines and tabs
            escaped_text = fixed_text.replace("\\", "\\\\").replace('"', '\\"')
            logger.debug("Markdown encoding preserved newlines and tabs")
        else:
            # For other message types, escape all special characters
            escaped_text = (
                fixed_text.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\t", "\\t")
            )
            logger.debug("Text encoding escaped all special characters")

        logger.debug(f"Encoded result: {escaped_text[:100]}{'...' if len(escaped_text) > 100 else ''}")
        # Return the escaped text directly without adding extra quotes
        return escaped_text
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Error encoding {msg_type} text: {e!s}")
        raise ValueError(f"Failed to encode {msg_type} text: {e!s}") from e
