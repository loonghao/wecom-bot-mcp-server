"""
Tests for WeCom Bot MCP Server Implementation

This module contains unit tests for the WeCom bot server implementation.
It tests message sending functionality and message history management.
"""

# Import built-in modules
from unittest.mock import MagicMock, patch

# Import third-party modules
import pytest

from wecom_bot_mcp_server.server import get_message_history, message_history, send_message


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
    """Test successful message sending.

    Tests that:
    1. Message is sent successfully
    2. Message is added to history
    3. Correct response is returned
    """
    test_message = "Test message"

    # Mock successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"errcode": 0, "errmsg": "ok"}

    async def mock_post(*args, **kwargs):
        return mock_response

    with patch("httpx.AsyncClient.post", new=mock_post):
        result = await send_message(test_message)
        assert result == "Message sent successfully"
        assert len(message_history) == 1
        assert message_history[0]["role"] == "assistant"
        assert message_history[0]["content"] == test_message


@pytest.mark.asyncio
async def test_send_message_empty_content() -> None:
    """Test sending empty message content.

    Verifies that attempting to send empty content raises ValueError.
    """
    with pytest.raises(ValueError, match="Message content cannot be empty"):
        await send_message("   ")


@pytest.mark.asyncio
async def test_send_message_api_error() -> None:
    """Test handling of API errors.

    Tests error handling for:
    1. HTTP error response
    2. WeChat API error response
    """
    test_message = "Test message"

    # Mock error response
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    async def mock_post(*args, **kwargs):
        return mock_response

    with patch("httpx.AsyncClient.post", new=mock_post), pytest.raises(ValueError, match="Failed to send message"):
        await send_message(test_message)


def test_get_message_history_empty() -> None:
    """Test getting empty message history."""
    assert get_message_history() == ""


def test_get_message_history_with_messages() -> None:
    """Test getting message history with messages.

    Tests that:
    1. Messages are correctly formatted
    2. Multiple messages are separated by newlines
    """
    message_history.extend(
        [{"role": "assistant", "content": "Message 1"}, {"role": "assistant", "content": "Message 2"}]
    )

    history = get_message_history()
    assert "Message 1" in history
    assert "Message 2" in history
    assert history.count("\n") == 1  # One newline between two messages
