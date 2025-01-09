"""WeCom Bot MCP Server Implementation

This module provides a server implementation for WeCom bot that follows the Model Context Protocol (MCP).
It handles message communication with WeCom webhook API and maintains message history.
"""

# Import built-in modules
import logging
import os
import sys
import traceback
from datetime import datetime
from typing import Annotated, Any, Callable, Dict, ParamSpec, TypeVar, cast

import httpx

# Import third-party modules
from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from mcp.shared.exceptions import McpError
from pydantic import Field
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

# Import local modules
from wecom_bot_mcp_server.constants import (
    INITIAL_WAIT_SECONDS,
    LOGGER_NAME,
    MAX_RETRIES,
    MAX_WAIT_SECONDS,
    REQUEST_TIMEOUT,
)
from wecom_bot_mcp_server.logger import setup_logger
from wecom_bot_mcp_server.models import Message, MessageHistory

# Type variables
T = TypeVar("T")
P = ParamSpec("P")


# Setup logging
logger = setup_logger(LOGGER_NAME)

# Set fastmcp and mcp loggers to WARNING level to suppress INFO messages
for logger_name in ["fastmcp", "mcp"]:
    module_logger = logging.getLogger(logger_name)
    module_logger.setLevel(logging.WARNING)

# Load environment variables
load_dotenv()


# Initialize FastMCP with settings
mcp = FastMCP(
    "WeCom Bot Server",
)


# Store message history
message_history: list[MessageHistory] = []


def retry_decorator(func: Callable[P, T]) -> Callable[P, T]:
    """Type-safe retry decorator wrapper."""
    decorated = retry(
        stop=stop_after_attempt(MAX_RETRIES),
        wait=wait_exponential(multiplier=INITIAL_WAIT_SECONDS, max=MAX_WAIT_SECONDS),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPError)),
        before_sleep=lambda retry_state: logger.debug(
            "Request failed (attempt %d/%d): %s",
            retry_state.attempt_number,
            MAX_RETRIES,
            str(retry_state.outcome.exception()),
        ),
    )(func)
    return cast(Callable[P, T], decorated)


@retry_decorator
async def _send_request(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Send HTTP request with retry logic.

    Args:
        url: The webhook URL to send request to
        payload: The request payload

    Returns:
        Dict[str, Any]: Response data from the API

    Raises:
        ValueError: If the request fails after all retries
        httpx.TimeoutException: If the request times out
        httpx.HTTPError: If there's an HTTP error
    """
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            logger.debug("Sending request to %s with payload: %s", url, payload)
            response = await client.post(url, json=payload)
            logger.debug(
                "Response received - Status: %d, Content: %s",
                response.status_code,
                response.text,
            )

            if response.status_code != 200:
                error_msg = f"HTTP error {response.status_code}: {response.text}"
                logger.warning(error_msg)
                raise ValueError(error_msg)

            response_data = cast(Dict[str, Any], response.json())
            if response_data.get("errcode") != 0:
                error_msg = (
                    f"WeChat API error {response_data.get('errcode')}: "
                    f"{response_data.get('errmsg', 'Unknown error')}"
                )
                logger.warning(error_msg)
                raise ValueError(error_msg)

            logger.debug("Request successful")
            return response_data

    except (httpx.TimeoutException, httpx.HTTPError) as e:
        logger.debug("HTTP request failed: %s", str(e))
        raise
    except ValueError:
        raise
    except Exception as e:
        logger.error("Unexpected error during request: %s", str(e))
        raise


@mcp.tool(description="Send a message to WeCom group/chat via webhook")  # type: ignore
async def send_message(
    message: Annotated[Message, Field(description="Message to send")],
    context: Annotated[Context, Field(description="MCP context object")],
) -> str:
    """Send a message to WeCom using the configured webhook URL.

    This function sends a message to WeCom using the configured webhook URL.
    The message will be formatted as markdown and added to message history.

    Args:
        message: The message to send, containing content and message type
        context: MCP context object (required by MCP framework but not used in this implementation)

    Returns:
        str: Success message if the message was sent successfully,
             or error message if there was an error.
    """
    webhook_url = os.getenv("WECHAT_WEBHOOK_URL")
    if not webhook_url:
        error_msg = "WECHAT_WEBHOOK_URL environment variable is not set"
        logger.error(error_msg)
        return f"Error: {error_msg}"

    # Construct payload with proper key
    msgtype = message.msgtype
    payload = {"msgtype": msgtype, msgtype: {"content": message.content}}

    try:
        await _send_request(webhook_url, payload)
        success_msg = "Message sent successfully"
        logger.info(success_msg)

        # Update message history with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message_history.append(
            MessageHistory(role="assistant", content=message.content, status="sent", timestamp=timestamp)
        )

        return success_msg
    except ValueError as e:
        error_msg = f"Failed to send message: {str(e)}"
        logger.warning(error_msg)
        return f"Error: {error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error while sending message: {str(e)}"
        logger.error(error_msg)
        return f"Error: {error_msg}"


@mcp.resource("resource://message-history", description="Get message history as a formatted string")  # type: ignore
def get_message_history() -> str:
    """Get message history as a formatted string.

    This function returns the message history as a newline-separated string,
    where each line contains the role, content, status and timestamp of a message.

    Returns:
        str: Formatted message history string. Empty string if no messages.
    """
    logger.debug("Retrieving message history - Length: %d", len(message_history))
    if not message_history:
        logger.info("Message history is empty")
        return "No messages in history"

    history = "\n".join(f"{msg.role}: {msg.content} ({msg.status}) at {msg.timestamp}" for msg in message_history)
    logger.debug("Message history retrieved successfully")
    return history


def main() -> None:
    """Entry point for the WeCom Bot MCP Server.

    This function starts the FastMCP server for handling WeCom bot messages.
    """
    try:
        logger.info("Starting WeCom Bot MCP Server...")
        mcp.run()
    except McpError as e:
        logger.error("MCP error: %s", str(e), exc_info=True)
        sys.exit(1)
    except Exception as e:
        logger.critical(
            "Failed to start server: %s\n%s",
            str(e),
            traceback.format_exc(),
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
