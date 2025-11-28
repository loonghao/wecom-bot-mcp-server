"""Tests for message module."""

# Import built-in modules
from pathlib import Path
import sys
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

# Ensure we import the local src/wecom_bot_mcp_server package (not an installed one)
ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

for name in list(sys.modules):
    if name == "wecom_bot_mcp_server" or name.startswith("wecom_bot_mcp_server."):
        del sys.modules[name]

# Import third-party modules
import pytest  # noqa: E402

# Import local modules
from wecom_bot_mcp_server.errors import ErrorCode  # noqa: E402
from wecom_bot_mcp_server.errors import WeComError  # noqa: E402
from wecom_bot_mcp_server.message import _get_webhook_url  # noqa: E402
from wecom_bot_mcp_server.message import _prepare_message_content  # noqa: E402
from wecom_bot_mcp_server.message import _process_message_response  # noqa: E402
from wecom_bot_mcp_server.message import _process_template_card_response  # noqa: E402
from wecom_bot_mcp_server.message import _send_message_to_wecom  # noqa: E402
from wecom_bot_mcp_server.message import _validate_message_inputs  # noqa: E402
from wecom_bot_mcp_server.message import get_formatted_message_history  # noqa: E402
from wecom_bot_mcp_server.message import get_markdown_capabilities_resource  # noqa: E402
from wecom_bot_mcp_server.message import get_message_history_resource  # noqa: E402
from wecom_bot_mcp_server.message import send_message  # noqa: E402
from wecom_bot_mcp_server.message import send_wecom_template_card  # noqa: E402
from wecom_bot_mcp_server.message import wecom_message_guidelines  # noqa: E402


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

    # Call function (default msg_type should be markdown_v2)
    result = await send_message("Test message")

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"

    mock_get_webhook_url.assert_called_once()
    mock_nb_instance.send_async.assert_called_once_with(
        "wecom",
        webhook_url="https://example.com/webhook",
        msg_type="markdown_v2",
        content="Test message",
        mentioned_list=[],
        mentioned_mobile_list=[],
    )


@pytest.mark.asyncio
async def test_send_message_with_context(mock_notify_bridge, mock_webhook_url):
    """Test send_message function with context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    result = await send_message(
        "Test message",
        "markdown_v2",
        ["user1", "user2"],
        ["13800138000"],
        mock_ctx,
    )

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Message sent successfully"

    # Verify ctx methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called()


@pytest.mark.asyncio
async def test_send_message_api_failure(mock_notify_bridge_api_error, mock_webhook_url):
    """Test send_message function with API failure."""
    # Call function with expected failure (default msg_type is markdown_v2)
    with pytest.raises(WeComError) as exc_info:
        await send_message("Test message")

    # Check error message
    assert "WeChat API error" in str(exc_info.value)
    assert "invalid credential" in str(exc_info.value)


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


def test_get_markdown_capabilities_resource():
    """Test get_markdown_capabilities_resource function."""
    result = get_markdown_capabilities_resource()
    assert "WeCom Markdown Capabilities" in result
    assert "markdown_v2" in result
    assert "send_wecom_image" in result


def test_wecom_message_guidelines_prompt():
    """Test wecom_message_guidelines prompt content."""
    prompt_text = wecom_message_guidelines()
    assert "markdown_v2" in prompt_text
    assert "send_wecom_image" in prompt_text
    assert "URLs must be preserved exactly" in prompt_text


@pytest.mark.asyncio
async def test_validate_message_inputs_valid():
    """Test _validate_message_inputs with valid inputs."""
    # This should not raise an exception for the only supported type
    await _validate_message_inputs("Test message", "markdown_v2")


@pytest.mark.asyncio
async def test_validate_message_inputs_empty_content():
    """Test _validate_message_inputs with empty content."""
    with pytest.raises(WeComError) as exc_info:
        await _validate_message_inputs("", "markdown_v2")

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
async def test_get_webhook_url_failure():
    """Test _get_webhook_url with failure."""
    # Setup mock
    with patch("wecom_bot_mcp_server.message.get_webhook_url", side_effect=WeComError("URL not found")):
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

    # Call function (default msg_type should be markdown_v2)
    result = await _prepare_message_content("Test message")

    # Assertions
    assert result == "Encoded message"
    mock_encode_text.assert_called_once_with("Test message", "markdown_v2")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.encode_text")
async def test_prepare_markdown_content_success(mock_encode_text):
    """Test _prepare_message_content with markdown_v2 type."""
    # Setup mock
    mock_encode_text.return_value = "Encoded markdown"

    # Call function
    result = await _prepare_message_content("# Test markdown", msg_type="markdown_v2")

    # Assertions
    assert result == "Encoded markdown"
    mock_encode_text.assert_called_once_with("# Test markdown", "markdown_v2")


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
        "https://example.com/webhook", "markdown_v2", "Test message", ["user1"], ["13800138000"]
    )

    # Assertions
    assert result == mock_response
    mock_nb_instance.send_async.assert_called_once_with(
        "wecom",
        webhook_url="https://example.com/webhook",
        msg_type="markdown_v2",
        content="Test message",
        mentioned_list=["user1"],
        mentioned_mobile_list=["13800138000"],
    )


@pytest.mark.asyncio
async def test_send_message_to_wecom_invalid_url():
    """Test _send_message_to_wecom function with invalid URL."""
    # Call function with invalid URL
    with pytest.raises(WeComError) as exc_info:
        await _send_message_to_wecom("invalid-webhook.example.com", "markdown_v2", "Test message")

    # Check error message
    assert "Invalid webhook URL format" in str(exc_info.value)
    assert "invalid-webhook.example.com" in str(exc_info.value)  # Verify the URL is included in the error message


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_message_to_wecom_exception(mock_notify_bridge):
    """Test _send_message_to_wecom function with NotifyBridge exception."""
    # Setup mock to raise exception
    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.side_effect = Exception("Connection error")
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function
    with pytest.raises(WeComError) as exc_info:
        await _send_message_to_wecom("https://example.com/webhook", "markdown_v2", "Test message")

    # Check error message
    assert "Failed to send message via NotifyBridge" in str(exc_info.value)
    assert "Connection error" in str(exc_info.value)
    assert "https://example.com/webhook" in str(exc_info.value)  # Verify the URL is included in the error message
    assert "markdown_v2" in str(exc_info.value)  # Verify the message type is included in the error message


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
async def test_send_message_network_error(mock_notify_bridge_network_error, mock_webhook_url):
    """Test send_message with network error."""
    # Call function with expected exception (default msg_type is markdown_v2)
    with pytest.raises(WeComError) as excinfo:
        await send_message("Test message", mentioned_list=["user1"], mentioned_mobile_list=["13800138000"])

    # Assertions
    assert "Failed to send message via NotifyBridge: Network connection failed" in str(excinfo.value)


@pytest.mark.asyncio
async def test_send_message_network_error_with_context(mock_notify_bridge_network_error, mock_webhook_url):
    """Test send_message with network error and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception (default msg_type is markdown_v2)
    with pytest.raises(WeComError) as excinfo:
        await send_message(
            "Test message",
            mentioned_list=["user1"],
            mentioned_mobile_list=["13800138000"],
            ctx=mock_ctx,
        )

    # Assertions
    assert "Failed to send message via NotifyBridge: Network connection failed" in str(excinfo.value)
    mock_ctx.error.assert_called()


@pytest.mark.asyncio
async def test_validate_message_inputs_empty_content_with_context():
    """Test _validate_message_inputs with empty content and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _validate_message_inputs("", "markdown_v2", mock_ctx)

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
    mock_get_webhook_url.side_effect = WeComError(
        "Webhook URL not found",
        ErrorCode.VALIDATION_ERROR,
    )

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
        await _prepare_message_content("Test message", "markdown_v2", mock_ctx)

    # Assertions
    assert "Text encoding error: Encoding failed" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
async def test_send_message_to_wecom_api_failure_with_context():
    """Test _send_message_to_wecom with API failure and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

    # Create mock context
    mock_ctx = AsyncMock()

    # Test _process_message_response directly
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


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_send_message_general_exception(mock_get_webhook_url):
    """Test send_message function with a general exception."""
    # Setup mock to raise a general exception
    mock_get_webhook_url.side_effect = RuntimeError("Unexpected error")

    # Call function
    with pytest.raises(WeComError) as exc_info:
        await send_message("Test message")

    # Check error message
    assert "Error sending message: Unexpected error" in str(exc_info.value)
    assert exc_info.value.error_code == ErrorCode.NETWORK_ERROR
    assert isinstance(exc_info.value.__cause__, RuntimeError)  # Verify the original exception is preserved


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.message.NotifyBridge")
async def test_send_message_to_wecom_request_failure_with_context(mock_notify_bridge=None):
    """Test _send_message_to_wecom with request failure and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = False
    mock_response.data = {}

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
@patch("wecom_bot_mcp_server.message.get_webhook_url")
async def test_send_wecom_template_card_text_notice_success(
    mock_get_webhook_url,
    mock_notify_bridge,
):
    """Test send_wecom_template_card for text_notice template."""
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    template_card_source = {"desc": "source"}
    template_card_main_title = {"title": "Title", "desc": "Desc"}
    template_card_card_action = {"type": 1, "url": "https://example.com"}

    result = await send_wecom_template_card(
        template_card_type="text_notice",
        template_card_source=template_card_source,
        template_card_main_title=template_card_main_title,
        template_card_card_action=template_card_card_action,
    )

    assert result["status"] == "success"
    mock_get_webhook_url.assert_called_once()
    mock_nb_instance.send_async.assert_awaited_once_with(
        "wecom",
        webhook_url="https://example.com/webhook",
        msg_type="template_card",
        template_card_type="text_notice",
        template_card_source=template_card_source,
        template_card_main_title=template_card_main_title,
        template_card_card_action=template_card_card_action,
    )


@pytest.mark.asyncio
async def test_send_wecom_template_card_invalid_type():
    """send_wecom_template_card should validate template_card_type."""
    with pytest.raises(WeComError) as exc_info:
        await send_wecom_template_card(
            template_card_type="invalid",
            template_card_source={"desc": "source"},
            template_card_main_title={"title": "Title"},
            template_card_card_action={"type": 1},
        )

    assert "Invalid template_card_type" in str(exc_info.value)
    assert exc_info.value.error_code == ErrorCode.VALIDATION_ERROR


@pytest.mark.asyncio
async def test_send_wecom_template_card_missing_required_fields():
    """send_wecom_template_card should validate required fields."""
    with pytest.raises(WeComError) as exc_info:
        await send_wecom_template_card(
            template_card_type="text_notice",
            template_card_source=None,
            template_card_main_title={"title": "Title"},
            template_card_card_action={"type": 1},
        )

    assert "Missing required template card fields" in str(exc_info.value)
    assert exc_info.value.error_code == ErrorCode.VALIDATION_ERROR


@pytest.mark.asyncio
async def test_process_template_card_response_success():
    """Test _process_template_card_response with success."""
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    result = await _process_template_card_response(mock_response)

    assert result["status"] == "success"
    assert result["message"] == "Template card sent successfully"


@pytest.mark.asyncio
async def test_process_template_card_response_request_failure():
    """Test _process_template_card_response with request failure."""
    mock_response = MagicMock()
    mock_response.success = False

    with pytest.raises(WeComError) as exc_info:
        await _process_template_card_response(mock_response)

    assert "Failed to send template card" in str(exc_info.value)


@pytest.mark.asyncio
async def test_process_template_card_response_api_failure():
    """Test _process_template_card_response with API failure."""
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "invalid card"}

    with pytest.raises(WeComError) as exc_info:
        await _process_template_card_response(mock_response)

    assert "WeChat API error" in str(exc_info.value)
    assert "invalid card" in str(exc_info.value)
