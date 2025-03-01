"""Tests for message module."""

# Import built-in modules
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.message import _get_webhook_url
from wecom_bot_mcp_server.message import _prepare_message_content
from wecom_bot_mcp_server.message import _process_message_response
from wecom_bot_mcp_server.message import _send_message_to_wecom
from wecom_bot_mcp_server.message import _validate_message_inputs
from wecom_bot_mcp_server.message import get_formatted_message_history
from wecom_bot_mcp_server.message import get_message_history_resource
from wecom_bot_mcp_server.message import send_message


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_send_message(mock_get_webhook_url, mock_notify_bridge):
    """Test send_message function."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function
    result = await send_message("Test message", "text")

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"

    mock_get_webhook_url.assert_called_once()
    mock_nb_instance.send_async.assert_called_once_with(
        "wecom",
        {
            "base_url": "https://example.com/webhook",
            "msg_type": "text",
            "content": "Test message",
            "mentioned_list": [],
            "mentioned_mobile_list": [],
        },
    )


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_send_message_with_context(mock_get_webhook_url, mock_notify_bridge):
    """Test send_message function with context."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    result = await send_message("Test message", "markdown", ["user1", "user2"], ["13800138000"], mock_ctx)

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"

    # Verify ctx methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_send_message_api_failure(mock_get_webhook_url, mock_notify_bridge):
    """Test send_message function with API failure."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "Invalid token"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function with expected failure
    with pytest.raises(WeComError) as exc_info:
        await send_message("Test message", "markdown")

    # Check error message
    assert "WeChat API error" in str(exc_info.value)
    assert "Invalid token" in str(exc_info.value)


@patch("wecom_bot_mcp_server.message.message_history")
def test_get_formatted_message_history_empty(mock_message_history):
    """Test get_formatted_message_history with empty history."""
    # Setup mock
    mock_message_history.__bool__.return_value = False

    # Call function
    result = get_formatted_message_history()

    # Assertions
    assert result == "No message history available."


@patch("wecom_bot_mcp_server.message.message_history")
def test_get_formatted_message_history(mock_message_history):
    """Test get_formatted_message_history with some messages."""
    # Setup mock
    mock_message_history.__bool__.return_value = True
    mock_message_history.__iter__.return_value = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there!"},
    ]

    # Call function
    result = get_formatted_message_history()

    # Assertions
    assert "# Message History" in result
    assert "## 1. User" in result
    assert "Hello" in result
    assert "## 2. Assistant" in result
    assert "Hi there!" in result


@patch("wecom_bot_mcp_server.message.get_formatted_message_history")
def test_get_message_history_resource(mock_get_formatted_history):
    """Test get_message_history_resource function."""
    # Setup mock
    mock_get_formatted_history.return_value = "Formatted history"

    # Call function
    result = get_message_history_resource()

    # Assertions
    assert result == "Formatted history"
    mock_get_formatted_history.assert_called_once()


@pytest.mark.asyncio
async def test_validate_message_inputs_valid():
    """Test _validate_message_inputs with valid inputs."""
    # Both of these should not raise exceptions
    await _validate_message_inputs("Test message", "text")
    await _validate_message_inputs("Test message", "markdown")


@pytest.mark.asyncio
async def test_validate_message_inputs_empty_content():
    """Test _validate_message_inputs with empty content."""
    with pytest.raises(WeComError) as exc_info:
        await _validate_message_inputs("", "text")

    assert "Message content cannot be empty" in str(exc_info.value)


@pytest.mark.asyncio
async def test_validate_message_inputs_invalid_type():
    """Test _validate_message_inputs with invalid message type."""
    with pytest.raises(WeComError) as exc_info:
        await _validate_message_inputs("Test message", "invalid_type")

    assert "Invalid message type" in str(exc_info.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_get_webhook_url_success(mock_get_webhook_url):
    """Test _get_webhook_url with success."""
    # Setup mock
    expected_url = "https://example.com/webhook"
    mock_get_webhook_url.return_value = expected_url

    # Call function
    result = await _get_webhook_url()

    # Assertions
    assert result == expected_url
    mock_get_webhook_url.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_get_webhook_url_failure(mock_get_webhook_url):
    """Test _get_webhook_url with failure."""
    # Setup mock
    mock_get_webhook_url.side_effect = WeComError("URL not found")

    # Call function with expected failure
    with pytest.raises(WeComError) as exc_info:
        await _get_webhook_url()

    # Check error message
    assert "URL not found" in str(exc_info.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.encode_text")
async def test_prepare_message_content_success(mock_encode_text):
    """Test _prepare_message_content with success."""
    # Setup mock
    mock_encode_text.return_value = "Encoded message"

    # Call function
    result = await _prepare_message_content("Test message")

    # Assertions
    assert result == "Encoded message"
    mock_encode_text.assert_called_once_with("Test message")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.encode_text")
async def test_prepare_message_content_failure(mock_encode_text):
    """Test _prepare_message_content with encoding failure."""
    # Setup mock
    mock_encode_text.side_effect = ValueError("Encoding error")

    # Call function with expected failure
    with pytest.raises(WeComError) as exc_info:
        await _prepare_message_content("Test message")

    # Check error message
    assert "Text encoding error" in str(exc_info.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_message_to_wecom(mock_notify_bridge):
    """Test _send_message_to_wecom function."""
    # Setup mock
    mock_response = MagicMock()
    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function
    result = await _send_message_to_wecom(
        "https://example.com/webhook", "markdown", "Test message", ["user1"], ["13800138000"]
    )

    # Assertions
    assert result == mock_response
    mock_nb_instance.send_async.assert_called_once_with(
        "wecom",
        {
            "base_url": "https://example.com/webhook",
            "msg_type": "markdown",
            "content": "Test message",
            "mentioned_list": ["user1"],
            "mentioned_mobile_list": ["13800138000"],
        },
    )


@pytest.mark.asyncio
async def test_process_message_response_success():
    """Test _process_message_response with success."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    # Call function
    result = await _process_message_response(mock_response)

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"


@pytest.mark.asyncio
async def test_process_message_response_request_failure():
    """Test _process_message_response with request failure."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = False

    # Call function with expected failure
    with pytest.raises(WeComError) as exc_info:
        await _process_message_response(mock_response)

    # Check error message
    assert "Failed to send message" in str(exc_info.value)


@pytest.mark.asyncio
async def test_process_message_response_api_failure():
    """Test _process_message_response with API failure."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "Invalid token"}

    # Call function with expected failure
    with pytest.raises(WeComError) as exc_info:
        await _process_message_response(mock_response)

    # Check error message
    assert "WeChat API error" in str(exc_info.value)
    assert "Invalid token" in str(exc_info.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.get_webhook_url")
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_message_network_error(mock_notify_bridge, mock_get_webhook_url):
    """Test send_message with network error."""
    # Setup mock webhook URL
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    # Setup NotifyBridge to raise an exception
    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.side_effect = Exception("Network connection failed")
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await send_message("Test message", "text", mock_ctx)

    # Assertions
    assert "Network connection failed" in str(excinfo.value)
    # Error is called in the _send_message_to_wecom function, not directly in send_message


@pytest.mark.asyncio
async def test_validate_message_inputs_empty_content_with_context():
    """Test _validate_message_inputs with empty content and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _validate_message_inputs("", "text", mock_ctx)

    # Assertions
    assert "Message content cannot be empty" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
async def test_validate_message_inputs_invalid_type_with_context():
    """Test _validate_message_inputs with invalid message type and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _validate_message_inputs("Test message", "invalid_type", mock_ctx)

    # Assertions
    assert "Invalid message type: invalid_type" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_get_webhook_url_with_context_and_error(mock_get_webhook_url):
    """Test _get_webhook_url with context and error."""
    # Setup mock to raise WeComError
    mock_get_webhook_url.side_effect = WeComError("Webhook URL not found", "VALIDATION_ERROR")

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _get_webhook_url(mock_ctx)

    # Assertions
    assert "Webhook URL not found" in str(excinfo.value)
    mock_ctx.error.assert_called_once_with("Webhook URL not found")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.encode_text")
async def test_prepare_message_content_with_context_and_error(mock_encode_text):
    """Test _prepare_message_content with context and encoding error."""
    # Setup mock to raise ValueError
    mock_encode_text.side_effect = ValueError("Encoding failed")

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _prepare_message_content("Test message", mock_ctx)

    # Assertions
    assert "Text encoding error: Encoding failed" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_message_to_wecom_request_failure_with_context(mock_notify_bridge):
    """Test _send_message_to_wecom with request failure and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = False
    mock_response.data = {}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create mock context
    mock_ctx = AsyncMock()

    # Test _process_message_response directly since _send_message_to_wecom no longer raises exceptions
    with pytest.raises(WeComError) as excinfo:
        await _process_message_response(mock_response, mock_ctx)

    # Assertions
    assert "Failed to send message" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_message_to_wecom_api_failure_with_context(mock_notify_bridge):
    """Test _send_message_to_wecom with API failure and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create mock context
    mock_ctx = AsyncMock()

    # Test _process_message_response directly since _send_message_to_wecom no longer raises exceptions
    with pytest.raises(WeComError) as excinfo:
        await _process_message_response(mock_response, mock_ctx)

    # Assertions
    assert "WeChat API error: invalid credential" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
async def test_process_message_response_with_context():
    """Test _process_message_response with success and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with the correct number of arguments
    result = await _process_message_response(mock_response, mock_ctx)

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"

    # Verify context methods were called
    mock_ctx.report_progress.assert_called_with(1.0)
    mock_ctx.info.assert_called_with("Message sent successfully")
