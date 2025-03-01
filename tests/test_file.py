"""Tests for file module."""

# Import built-in modules
from pathlib import Path
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.file import _get_webhook_url
from wecom_bot_mcp_server.file import _process_file_response
from wecom_bot_mcp_server.file import _send_file_to_wecom
from wecom_bot_mcp_server.file import _validate_file
from wecom_bot_mcp_server.file import send_wecom_file


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
@patch("wecom_bot_mcp_server.file.Path.stat")
@patch("wecom_bot_mcp_server.file.NotifyBridge")
@patch("wecom_bot_mcp_server.file.get_webhook_url")
async def test_send_wecom_file(mock_get_webhook_url, mock_notify_bridge, mock_stat, mock_is_file, mock_exists):
    """Test send_wecom_file function."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_stat_result = MagicMock()
    mock_stat_result.st_size = 1024
    mock_stat.return_value = mock_stat_result

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "media_id": "test_media_id"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function
    result = await send_wecom_file("test_file.txt")

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "File sent successfully"
    assert result["file_name"] == "test_file.txt"
    assert result["file_size"] == 1024
    assert result["media_id"] == "test_media_id"

    mock_get_webhook_url.assert_called_once()
    mock_nb_instance.send_async.assert_called_once_with(
        "wecom",
        {
            "base_url": "https://example.com/webhook",
            "msg_type": "file",
            "file_path": str(Path("test_file.txt").absolute()),
        },
    )


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
async def test_send_wecom_file_not_found(mock_exists):
    """Test send_wecom_file with non-existent file."""
    # Setup mock
    mock_exists.return_value = False

    # Call function and check exception
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_file("non_existent_file.txt")

    # Assertions
    assert "File not found" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
@patch("wecom_bot_mcp_server.file.get_webhook_url")
@patch("wecom_bot_mcp_server.file.NotifyBridge")
async def test_send_wecom_file_api_error(mock_notify_bridge, mock_get_webhook_url, mock_is_file, mock_exists):
    """Test send_wecom_file with API error."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    # Set success to True because NotifyBridge might successfully send the request
    # but WeCom API returns an error code
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function and check exception
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_file("test_file.txt")

    # Assertions
    # Check if the error message contains "invalid credential", regardless of how it's raised
    assert "invalid credential" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
@patch("wecom_bot_mcp_server.file.get_webhook_url")
@patch("wecom_bot_mcp_server.file.NotifyBridge")
async def test_send_wecom_file_response_failure(mock_notify_bridge, mock_get_webhook_url, mock_is_file, mock_exists):
    """Test send_wecom_file with response failure."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_response = MagicMock()
    mock_response.success = False
    mock_response.data = {}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function and check exception
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_file("test_file.txt")

    # Assertions
    assert "Failed to send file" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
@patch("wecom_bot_mcp_server.file.get_webhook_url")
@patch("wecom_bot_mcp_server.file.NotifyBridge")
async def test_send_wecom_file_exception(mock_notify_bridge, mock_get_webhook_url, mock_is_file, mock_exists):
    """Test send_wecom_file with exception."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.side_effect = Exception("Test exception")
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Call function and check exception
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_file("test_file.txt")

    # Assertions
    assert "Error sending file: Test exception" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
async def test_validate_file_with_string_path(mock_is_file, mock_exists):
    """Test _validate_file with string path."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True

    # Call function
    result = await _validate_file("test_file.txt")

    # Assertions
    assert isinstance(result, Path)
    assert result.name == "test_file.txt"


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
async def test_validate_file_with_path_object(mock_is_file, mock_exists):
    """Test _validate_file with Path object."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True

    # Create Path object
    file_path = Path("test_file.txt")

    # Call function
    result = await _validate_file(file_path)

    # Assertions
    assert result == file_path


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
async def test_validate_file_not_exists(mock_exists):
    """Test _validate_file with non-existent file."""
    # Setup mock
    mock_exists.return_value = False

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _validate_file("non_existent_file.txt")

    # Assertions
    assert "File not found" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
async def test_validate_file_not_a_file(mock_is_file, mock_exists):
    """Test _validate_file with a directory instead of a file."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = False

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _validate_file("directory/")

    # Assertions
    assert "Not a file" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.get_webhook_url")
async def test_get_webhook_url_function(mock_get_webhook_url):
    """Test _get_webhook_url function."""
    # Setup mock
    expected_url = "https://example.com/webhook"
    mock_get_webhook_url.return_value = expected_url

    # Call function
    result = await _get_webhook_url()

    # Assertions
    assert result == expected_url
    mock_get_webhook_url.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.get_webhook_url")
async def test_get_webhook_url_with_error(mock_get_webhook_url):
    """Test _get_webhook_url function with error."""
    # Setup mock
    mock_get_webhook_url.side_effect = WeComError("Webhook URL not found")

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _get_webhook_url()

    # Assertions
    assert "Webhook URL not found" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.NotifyBridge")
async def test_send_file_to_wecom(mock_notify_bridge):
    """Test _send_file_to_wecom function."""
    # Setup mock
    mock_response = MagicMock()
    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Setup test params
    file_path = Path("test_file.txt")
    base_url = "https://example.com/webhook"

    # Call function
    result = await _send_file_to_wecom(file_path, base_url)

    # Assertions
    assert result == mock_response
    mock_nb_instance.send_async.assert_called_once_with(
        "wecom",
        {
            "base_url": base_url,
            "msg_type": "file",
            "file_path": str(file_path.absolute()),
        },
    )


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.stat")
async def test_process_file_response_success(mock_stat):
    """Test _process_file_response with success response."""
    # Setup mocks
    mock_stat_result = MagicMock()
    mock_stat_result.st_size = 2048
    mock_stat.return_value = mock_stat_result

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "media_id": "test_media_id"}

    file_path = Path("test_file.txt")

    # Call function
    result = await _process_file_response(mock_response, file_path)

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "File sent successfully"
    assert result["file_name"] == "test_file.txt"
    assert result["file_size"] == 2048
    assert result["media_id"] == "test_media_id"


@pytest.mark.asyncio
async def test_process_file_response_request_failure():
    """Test _process_file_response with request failure."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = False
    file_path = Path("test_file.txt")

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_file_response(mock_response, file_path)

    # Assertions
    assert "Failed to send file" in str(excinfo.value)


@pytest.mark.asyncio
async def test_process_file_response_api_error():
    """Test _process_file_response with API error."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "Invalid token"}
    file_path = Path("test_file.txt")

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_file_response(mock_response, file_path)

    # Assertions
    assert "WeChat API error" in str(excinfo.value)
    assert "Invalid token" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
@patch("wecom_bot_mcp_server.file.Path.stat")
@patch("wecom_bot_mcp_server.file.NotifyBridge")
@patch("wecom_bot_mcp_server.file.get_webhook_url")
async def test_send_wecom_file_with_context(
    mock_get_webhook_url, mock_notify_bridge, mock_stat, mock_is_file, mock_exists
):
    """Test send_wecom_file function with context."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    mock_stat_result = MagicMock()
    mock_stat_result.st_size = 1024
    mock_stat.return_value = mock_stat_result

    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "media_id": "test_media_id"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    result = await send_wecom_file("test_file.txt", mock_ctx)

    # Assertions
    assert result["status"] == "success"

    # Verify ctx methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
async def test_validate_file_with_context(mock_is_file, mock_exists):
    """Test _validate_file function with context."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    file_path = await _validate_file("test_file.txt", mock_ctx)

    # Assertions
    assert isinstance(file_path, Path)
    assert str(file_path) == "test_file.txt"

    # Context methods should not be called in success case
    mock_ctx.error.assert_not_called()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
async def test_validate_file_not_exists_with_context(mock_exists):
    """Test _validate_file with non-existent file and context."""
    # Setup mocks
    mock_exists.return_value = False

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _validate_file("nonexistent_file.txt", mock_ctx)

    # Assertions
    assert "File not found: nonexistent_file.txt" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.Path.exists")
@patch("wecom_bot_mcp_server.file.Path.is_file")
async def test_validate_file_not_a_file_with_context(mock_is_file, mock_exists):
    """Test _validate_file with a directory instead of a file and context."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = False

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _validate_file("directory", mock_ctx)

    # Assertions
    assert "Not a file: directory" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.get_webhook_url")
async def test_get_webhook_url_with_context(mock_get_webhook_url):
    """Test _get_webhook_url function with context."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    result = await _get_webhook_url(mock_ctx)

    # Assertions
    assert result == "https://example.com/webhook"

    # Context methods should not be called in success case
    mock_ctx.error.assert_not_called()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.get_webhook_url")
async def test_get_webhook_url_with_error_and_context(mock_get_webhook_url):
    """Test _get_webhook_url function with error and context."""
    # Setup mocks to raise WeComError
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
@patch("wecom_bot_mcp_server.file.NotifyBridge")
async def test_send_file_to_wecom_with_context(mock_notify_bridge):
    """Test _send_file_to_wecom function with context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    file_path = Path("test_file.txt")
    result = await _send_file_to_wecom(file_path, "https://example.com/webhook", mock_ctx)

    # Assertions
    assert result == mock_response

    # Check NotifyBridge was called with correct parameters
    mock_nb_instance.send_async.assert_called_once()
    args = mock_nb_instance.send_async.call_args[0]
    assert args[0] == "wecom"
    assert "base_url" in args[1]
    assert "file_path" in args[1]
    assert args[1]["file_path"] == str(file_path.absolute())

    # Context methods should not be called in _send_file_to_wecom
    mock_ctx.report_progress.assert_called_once_with(0.7)
    mock_ctx.info.assert_called_once_with(f"Sending file: {file_path}")


@pytest.mark.asyncio
async def test_process_file_response_success_with_context():
    """Test _process_file_response with success response and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    file_path = Path("test_file.txt")

    # Create mock context
    mock_ctx = AsyncMock()

    # Mock file stats
    with patch.object(Path, "stat") as mock_stat:
        mock_stat.return_value.st_size = 1024

        # Call function
        result = await _process_file_response(mock_response, file_path, mock_ctx)

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "File sent successfully"
    assert result["file_size"] == 1024
    assert result["file_name"] == "test_file.txt"

    # Verify context methods were called
    mock_ctx.report_progress.assert_called_with(1.0)
    mock_ctx.info.assert_called_with("File sent successfully")


@pytest.mark.asyncio
async def test_process_file_response_request_failure_with_context():
    """Test _process_file_response with request failure and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = False

    file_path = Path("test_file.txt")

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_file_response(mock_response, file_path, mock_ctx)

    # Assertions
    assert "Failed to send file" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
async def test_process_file_response_api_error_with_context():
    """Test _process_file_response with API error and context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

    file_path = Path("test_file.txt")

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_file_response(mock_response, file_path, mock_ctx)

    # Assertions
    assert "WeChat API error: invalid credential" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.file.NotifyBridge")
@patch("wecom_bot_mcp_server.file.get_webhook_url")
@patch("wecom_bot_mcp_server.file.Path.is_file")
@patch("wecom_bot_mcp_server.file.Path.exists")
async def test_send_wecom_file_network_error(mock_exists, mock_is_file, mock_get_webhook_url, mock_notify_bridge):
    """Test send_wecom_file with network error."""
    # Setup mocks
    mock_exists.return_value = True
    mock_is_file.return_value = True
    mock_get_webhook_url.return_value = "https://example.com/webhook"

    # Setup NotifyBridge to raise an exception
    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.side_effect = Exception("Network connection failed")
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_file("test_file.txt", mock_ctx)

    # Assertions
    assert "Error sending file: Network connection failed" in str(excinfo.value)
    mock_ctx.error.assert_called_once()
