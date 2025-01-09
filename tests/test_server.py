"""
Tests for WeCom Bot MCP Server Implementation

This module contains unit tests for the WeCom bot server implementation.
It tests message sending functionality, retry mechanism, error handling, and notification processing.
"""

# Import built-in modules
import logging
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

# Import third-party modules
from fastmcp import Context  # type: ignore
from pydantic import ValidationError
from tenacity import RetryError

# Import local modules
from wecom_bot_mcp_server.models import Message, MessageHistory
from wecom_bot_mcp_server.server import (
    MAX_RETRIES,
    _send_request,
    get_message_history,
    logger,
    message_history,
    send_message,
)


@pytest.fixture(autouse=True)
def setup_logging():
    """Set up logging configuration for tests."""
    original_level = logger.level
    logger.setLevel(logging.WARNING)
    yield
    logger.setLevel(original_level)


@pytest.fixture(autouse=True)
def setup_environment(monkeypatch) -> None:
    """Set up test environment before each test.

    Sets up required environment variables and cleans up message history.

    Args:
        monkeypatch: pytest fixture for modifying environment
    """
    monkeypatch.setenv("WECHAT_WEBHOOK_URL", "https://mock.wecom.api/webhook")
    yield


@pytest.fixture(autouse=True)
def clear_message_history() -> None:
    """Clear message history before each test."""
    message_history.clear()
    yield


@pytest.mark.asyncio
async def test_send_message_success() -> None:
    """Test successful message sending."""
    test_message = Message(content="Test message", msgtype="markdown")
    test_context = Context(session_id="test_session")

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}

    with patch("httpx.AsyncClient.post", return_value=mock_response):
        result = await send_message(test_message, test_context)
        assert "Message sent successfully" in result
        assert len(message_history) == 1
        assert message_history[0].content == test_message.content


@pytest.mark.asyncio
async def test_send_message_empty_content() -> None:
    """Test sending empty message content."""
    with pytest.raises(ValidationError):  # pydantic validation will raise ValidationError
        Message(content="", msgtype="markdown")


@pytest.mark.asyncio
async def test_send_message_api_error() -> None:
    """Test handling of API errors."""
    test_message = Message(content="Test message", msgtype="markdown")
    test_context = Context(session_id="test_session")

    # Test API error response
    mock_response = MagicMock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {"errcode": 1, "errmsg": "API Error"}

    with patch("httpx.AsyncClient.post", AsyncMock(return_value=mock_response)):
        result = await send_message(test_message, test_context)
        assert "Error: Failed to send message: WeChat API error 1: API Error" in result


@pytest.mark.asyncio
async def test_retry_mechanism() -> None:
    """Test retry mechanism for network failures."""
    test_url = "https://mock.wecom.api/webhook"
    test_payload = {"content": "test"}

    # Test max retries exceeded
    mock_post = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))

    with patch("httpx.AsyncClient.post", mock_post):
        with pytest.raises(RetryError):
            await _send_request(test_url, test_payload)

    # Verify retry attempts
    assert mock_post.call_count == MAX_RETRIES


def test_get_message_history_empty() -> None:
    """Test getting empty message history."""
    assert get_message_history() == "No messages in history"


def test_get_message_history_with_messages() -> None:
    """Test getting message history with messages."""
    test_message = MessageHistory(
        role="user", content="Test message", status="sent", timestamp="2025-01-09T20:09:00+08:00"
    )
    message_history.append(test_message)

    history = get_message_history()
    assert "Test message" in history
    assert "user" in history
    assert "sent" in history
