"""Tests for image module."""

# Import built-in modules
from pathlib import Path
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import mock_open
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.errors import WeComError
from wecom_bot_mcp_server.image import _get_webhook_url
from wecom_bot_mcp_server.image import _process_image_path
from wecom_bot_mcp_server.image import _process_image_response
from wecom_bot_mcp_server.image import _send_image_to_wecom
from wecom_bot_mcp_server.image import download_image
from wecom_bot_mcp_server.image import send_wecom_image


@pytest.mark.asyncio
async def test_send_wecom_image_local(mock_image_send, fs):
    """Test send_wecom_image function with local file."""
    # Unpack fixtures
    mock_exists, mock_pil_open, mock_notify_bridge, mock_get_webhook_url, mock_nb_instance = mock_image_send

    # Create test image file
    fs.create_file("test_image.jpg", contents=b"\x89PNG\r\n\x1a\n")

    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}
    mock_nb_instance.send_async.return_value = mock_response

    # Call function
    result = await send_wecom_image("test_image.jpg")

    # Assertions
    assert result["status"] == "success"
    assert result["image_path"] == "test_image.jpg"

    # Verify NotifyBridge was called correctly
    mock_nb_instance.send_async.assert_called_once()


@pytest.mark.asyncio
async def test_send_wecom_image_with_context(mock_notify_bridge, mock_webhook_url, mock_image_processing):
    """Test send_wecom_image function with context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}
    mock_notify_bridge.return_value.__aenter__.return_value.send_async.return_value = mock_response

    # Call function
    result = await send_wecom_image("test_image.jpg", mock_ctx)

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Image sent successfully"
    assert "test_image.jpg" in result["image_path"]

    # Verify context methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called()


@pytest.mark.asyncio
async def test_send_wecom_image_with_fixtures(mock_webhook_url, mock_notify_bridge, mock_image_processing):
    """Test send_wecom_image function using fixtures from conftest."""
    # Call function
    result = await send_wecom_image("test_image.jpg")

    # Assertions
    assert result["status"] == "success"
    assert "message" in result
    assert "image_path" in result


@pytest.mark.asyncio
async def test_send_wecom_image_not_found(mock_image_not_found):
    """Test send_wecom_image function with non-existent file."""
    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_image("non_existent_image.jpg")

    # Assertions
    assert "Image file not found" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.aiohttp.ClientSession")
@patch("builtins.open", new_callable=mock_open)
@patch("wecom_bot_mcp_server.image.os.makedirs")
async def test_download_image(mock_makedirs, mock_file_open, mock_client_session):
    """Test download_image function."""
    # Setup mocks
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "image/jpeg"}
    mock_response.read = AsyncMock(return_value=b"image_data")

    # Create a mock session.get result
    mock_get_cm = AsyncMock()
    mock_get_cm.__aenter__.return_value = mock_response

    # Create a mock session object
    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_get_cm)

    # Create a mock ClientSession context manager
    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session

    # Set ClientSession to return the mock context manager
    mock_client_session.return_value = mock_session_cm

    # Call function
    result = await download_image("https://example.com/image.jpg")

    # Assertions
    assert isinstance(result, Path)
    mock_session.get.assert_called_once_with("https://example.com/image.jpg")
    mock_file_open.assert_called_once()
    mock_file_open().write.assert_called_once_with(b"image_data")


@pytest.mark.asyncio
async def test_send_wecom_image_url(mock_image_download, fs):
    """Test send_wecom_image function with URL."""
    # Unpack fixtures
    mock_exists, mock_pil_open, mock_download = mock_image_download

    # Setup additional mocks for NotifyBridge and webhook
    with (
        patch("wecom_bot_mcp_server.image.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.image.get_webhook_url") as mock_get_webhook_url,
    ):
        # Setup mocks
        mock_get_webhook_url.return_value = "https://example.com/webhook"
        # Fix Windows path issue
        downloaded_path = Path("tmp/downloaded_image.jpg")
        mock_download.return_value = downloaded_path

        # Create the downloaded image file
        fs.create_file(downloaded_path, contents=b"\x89PNG\r\n\x1a\n")

        # Setup NotifyBridge mock
        mock_nb_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "errmsg": "ok"}
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        # Call function
        result = await send_wecom_image("https://example.com/image.jpg")

        # Assertions
        assert result["status"] == "success"
        # Convert Path object to string to match the actual return value
        assert result["image_path"] == str(downloaded_path)

        # Verify NotifyBridge was called correctly
        mock_nb_instance.send_async.assert_called_once_with(
            "wecom",
            {
                "base_url": "https://example.com/webhook",
                "msg_type": "image",
                "image": str(downloaded_path.absolute()),
            },
        )


@pytest.mark.asyncio
async def test_process_image_path_local_file(fs):
    """Test _process_image_path with a local file."""
    # Create a test image file
    fs.create_file("test_image.jpg", contents=b"\x89PNG\r\n\x1a\n")

    # Setup additional mock for Image.open
    with patch("wecom_bot_mcp_server.image.Image.open") as mock_pil_open:
        # Mock PIL open success
        mock_pil_open.return_value = MagicMock()

        # Call function
        result = await _process_image_path("test_image.jpg")

        # Assertions
        assert isinstance(result, Path)
        assert result.name == "test_image.jpg"
        mock_pil_open.assert_called_once()


@pytest.mark.asyncio
async def test_process_image_path_file_not_found(mock_image_not_a_file):
    """Test _process_image_path with non-existent file."""
    # Setup mock
    mock_exists = mock_image_not_a_file[0]
    mock_exists.return_value = False

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_image_path("non_existent_image.jpg")

    # Assertions
    assert "Image file not found" in str(excinfo.value)


@pytest.mark.asyncio
async def test_process_image_path_not_a_file(mock_image_not_a_file):
    """Test _process_image_path with a directory."""
    # Setup additional mock for Image.open
    with patch("wecom_bot_mcp_server.image.Image.open") as mock_pil_open:
        # Mock PIL open failure, which is the actual check used in the source code
        mock_pil_open.side_effect = Exception("Cannot identify image file")

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await _process_image_path("directory")

        # Assertions
        assert "Invalid image format" in str(excinfo.value)


@pytest.mark.asyncio
async def test_process_image_path_invalid_image(mock_image_not_a_file):
    """Test _process_image_path with an invalid image file."""
    # Setup additional mock for Image.open
    with patch("wecom_bot_mcp_server.image.Image.open") as mock_pil_open:
        # Mock PIL open failure for invalid image
        mock_pil_open.side_effect = Exception("Invalid image file")

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await _process_image_path("invalid_image.txt")

        # Assertions
        assert "Invalid image format" in str(excinfo.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.download_image")
@patch("wecom_bot_mcp_server.image.Path.exists")
@patch("wecom_bot_mcp_server.image.Image.open")
async def test_process_image_path_url(mock_pil_open, mock_exists, mock_download):
    """Test _process_image_path with a URL."""
    # Setup mocks
    downloaded_path = Path("tmp/downloaded_image.jpg")
    mock_download.return_value = downloaded_path
    mock_exists.return_value = True

    # Mock image opening function
    mock_image = MagicMock()
    mock_pil_open.return_value = mock_image

    # Call function
    result = await _process_image_path("https://example.com/image.jpg")

    # Assertions
    assert result == downloaded_path
    mock_download.assert_called_once_with("https://example.com/image.jpg", None)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.get_webhook_url")
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
@patch("wecom_bot_mcp_server.image.get_webhook_url")
async def test_get_webhook_url_with_context(mock_get_webhook_url):
    """Test _get_webhook_url function with context."""
    # Setup mock
    expected_url = "https://example.com/webhook"
    mock_get_webhook_url.return_value = expected_url

    # Create mock context
    mock_ctx = MagicMock()

    # Call function
    result = await _get_webhook_url(mock_ctx)

    # Assertions
    assert result == expected_url
    mock_get_webhook_url.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.get_webhook_url")
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
async def test_send_image_to_wecom(fs):
    """Test _send_image_to_wecom function."""
    # Create a test image file
    image_path = Path("test_image.jpg")
    fs.create_file(image_path, contents=b"\x89PNG\r\n\x1a\n")
    base_url = "https://example.com/webhook"

    # Setup NotifyBridge mock
    with patch("wecom_bot_mcp_server.image.NotifyBridge") as mock_notify_bridge:
        mock_nb_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "errmsg": "ok"}
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        # Call function
        result = await _send_image_to_wecom(image_path, base_url)

        # Assertions
        assert result == mock_response
        mock_nb_instance.send_async.assert_called_once_with(
            "wecom",
            {
                "base_url": base_url,
                "msg_type": "image",
                "image": str(image_path.absolute()),
            },
        )


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.NotifyBridge")
async def test_send_image_to_wecom_exception(mock_notify_bridge):
    """Test _send_image_to_wecom function with exception."""
    # Setup mock
    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.side_effect = Exception("Test exception")
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Setup test params
    image_path = Path("test_image.jpg")
    base_url = "https://example.com/webhook"

    # Call function with expected exception
    with pytest.raises(Exception) as excinfo:
        await _send_image_to_wecom(image_path, base_url)

    # Assertions
    assert "Test exception" in str(excinfo.value)


@pytest.mark.asyncio
async def test_process_image_response_success():
    """Test _process_image_response with success response."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    image_path = Path("test_image.jpg")

    # Call function
    result = await _process_image_response(mock_response, image_path)

    # Assertions
    assert result["status"] == "success"
    assert result["message"] == "Image sent successfully"
    assert result["image_path"] == str(image_path)


@pytest.mark.asyncio
async def test_process_image_response_request_failure():
    """Test _process_image_response with request failure."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = False
    mock_response.data = {}

    image_path = Path("test_image.jpg")

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_image_response(mock_response, image_path)

    # Assertions
    assert "Failed to send image" in str(excinfo.value)


@pytest.mark.asyncio
async def test_process_image_response_api_error():
    """Test _process_image_response with API error."""
    # Setup mock response
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "Invalid token"}

    image_path = Path("test_image.jpg")

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_image_response(mock_response, image_path)

    # Assertions
    assert "WeChat API error" in str(excinfo.value)
    assert "Invalid token" in str(excinfo.value)


@pytest.mark.asyncio
async def test_process_image_response_with_context():
    """Test _process_image_response with context."""
    # Setup mocks
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 0, "errmsg": "ok"}

    image_path = Path("test_image.jpg")

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    result = await _process_image_response(mock_response, image_path, mock_ctx)

    # Assertions
    assert result["status"] == "success"

    # Verify context methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called_with("Image sent successfully")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.aiohttp.ClientSession")
async def test_download_image_with_context(mock_client_session):
    """Test download_image function with context."""
    # Setup mocks
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "image/jpeg"}
    mock_response.read = AsyncMock(return_value=b"image_data")

    # Create a mock session.get result
    mock_get_cm = AsyncMock()
    mock_get_cm.__aenter__.return_value = mock_response

    # Create a mock session object
    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_get_cm)

    # Setup the context manager correctly
    mock_session_cm = MagicMock()
    mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session_cm.__aexit__ = AsyncMock(return_value=None)
    mock_client_session.return_value = mock_session_cm

    # Create mock context
    mock_ctx = AsyncMock()

    # Mock open to avoid actual file writing
    with patch("builtins.open", new_callable=mock_open):
        with patch("wecom_bot_mcp_server.image.os.makedirs"):
            # Call function
            result = await download_image("https://example.com/image.jpg", mock_ctx)

    # Assert context methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called_with("Downloading image from https://example.com/image.jpg")

    # Other assertions
    assert isinstance(result, Path)
    mock_session.get.assert_called_once_with("https://example.com/image.jpg")


@pytest.mark.asyncio
async def test_download_image_network_error(mock_network_error_with_context):
    """Test download_image with network error."""
    # Unpack the fixture
    _, mock_ctx = mock_network_error_with_context

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await download_image("https://example.com/image.jpg", mock_ctx)

    # Assertions
    assert "Failed to download image: Network error" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.Path.exists")
@patch("wecom_bot_mcp_server.image.Image.open")
async def test_process_image_path_with_context(mock_pil_open, mock_exists):
    """Test _process_image_path with context."""
    # Setup mocks
    mock_exists.return_value = True
    mock_pil_open.return_value = MagicMock()  # Valid image

    # Setup context
    mock_ctx = AsyncMock()

    # Call function
    result = await _process_image_path("test.jpg", mock_ctx)

    # Assertions
    assert isinstance(result, Path)
    mock_pil_open.assert_called_once()
    # No download should be attempted for local file
    mock_exists.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.Path.exists")
@patch("wecom_bot_mcp_server.image.download_image")
async def test_process_image_path_url_with_download_error(mock_download, mock_exists):
    """Test _process_image_path with URL that has download error."""
    # Setup mock to raise WeComError during download
    mock_download.side_effect = WeComError("Download failed", "FILE_ERROR")

    # Create mock context
    mock_ctx = AsyncMock()

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await _process_image_path("https://example.com/image.jpg", mock_ctx)

    # Assertions
    assert "Download failed" in str(excinfo.value)
    mock_ctx.error.assert_called_once()
    mock_download.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.Path.exists")
@patch("wecom_bot_mcp_server.image.get_webhook_url")
async def test_get_webhook_url_with_error_and_context(mock_get_webhook_url, mock_exists):
    """Test _get_webhook_url with error and context."""
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
@patch("wecom_bot_mcp_server.image.Path.exists")
@patch("wecom_bot_mcp_server.image.Image.open")
@patch("wecom_bot_mcp_server.image.NotifyBridge")
@patch("wecom_bot_mcp_server.image.get_webhook_url")
async def test_send_wecom_image_with_context(mock_get_webhook_url, mock_notify_bridge, mock_pil_open, mock_exists):
    """Test send_wecom_image function with context."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"
    mock_exists.return_value = True
    mock_pil_open.return_value = MagicMock()  # Valid image

    # Setup NotifyBridge to raise exception
    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.side_effect = Exception("Connection error")
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Setup context
    mock_ctx = AsyncMock()

    # Call function
    with pytest.raises(WeComError) as exc_info:
        await send_wecom_image("test.jpg", ctx=mock_ctx)

    # Check error message
    assert "Error sending image: Connection error" in str(exc_info.value)

    # Verify context methods were called
    mock_ctx.error.assert_called_with("Error sending image: Connection error")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.NotifyBridge")
@patch("wecom_bot_mcp_server.image._get_webhook_url")
@patch("wecom_bot_mcp_server.image.Path.exists")
@patch("wecom_bot_mcp_server.image.Image.open")
async def test_send_wecom_image_with_api_error_and_context(
    mock_pil_open, mock_exists, mock_get_webhook_url, mock_notify_bridge
):
    """Test send_wecom_image function with API error and context."""
    # Setup mocks
    mock_get_webhook_url.return_value = "https://example.com/webhook"
    mock_exists.return_value = True
    mock_pil_open.return_value = MagicMock()  # Valid image

    # Setup NotifyBridge mock response with API error
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

    mock_nb_instance = AsyncMock()
    mock_nb_instance.send_async.return_value = mock_response
    mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

    # Setup context
    mock_ctx = AsyncMock()

    # Call function
    with pytest.raises(WeComError) as exc_info:
        await send_wecom_image("test.jpg", mock_ctx)

    # Check error message
    assert "WeChat API error: invalid credential" in str(exc_info.value)

    # Verify context methods were called
    assert mock_ctx.error.called


@pytest.mark.asyncio
async def test_send_wecom_image_with_context(mock_notify_bridge, mock_webhook_url, mock_image_processing):
    """Test send_wecom_image function with context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Call function
    result = await send_wecom_image("test_image.jpg", mock_ctx)

    # Assertions
    assert result["status"] == "success"

    # Verify context methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called()


@pytest.mark.asyncio
async def test_send_wecom_image_with_notify_bridge_error(
    mock_notify_bridge_error, mock_webhook_url, mock_image_processing
):
    """Test send_wecom_image function with NotifyBridge error."""
    # Call function
    with pytest.raises(WeComError) as exc_info:
        await send_wecom_image("test.jpg")

    # Check error message
    assert "Error sending image: Connection error" in str(exc_info.value)
    assert "Connection error" in str(exc_info.value)


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.aiohttp.ClientSession")
async def test_download_image_http_error(mock_client_session):
    """Test download_image with HTTP error."""
    # Setup mocks
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.read = AsyncMock(return_value=b"error_data")

    # Create a mock session.get result
    mock_get_cm = AsyncMock()
    mock_get_cm.__aenter__.return_value = mock_response

    # Create a mock session object
    mock_session = AsyncMock()
    mock_session.get = MagicMock(return_value=mock_get_cm)

    # Create a mock ClientSession context manager
    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session

    # Set ClientSession to return the mock context manager
    mock_client_session.return_value = mock_session_cm

    # Call function with a URL that will result in a 404
    with pytest.raises(WeComError) as excinfo:
        await download_image("https://example.com/not-found.jpg")

    # Assertions
    assert "Failed to download image: HTTP 404" in str(excinfo.value)


@pytest.mark.asyncio
async def test_download_image_invalid_content_type_no_context():
    """Test download_image with invalid content type without context."""
    # Setup mock response with invalid content type
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession") as mock_session_class:
        # Create a mock session
        mock_session = MagicMock()

        # Setup the response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.read = AsyncMock(return_value=b"invalid data")

        # Setup the get method to return a context manager that returns the mock response
        mock_get_cm = MagicMock()
        mock_get_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_get_cm)

        # Setup session context manager
        mock_session_cm = MagicMock()
        mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session_cm

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await download_image("https://example.com/image.jpg")

        # Assertions
        assert "Invalid content type: text/html" in str(excinfo.value)


@pytest.mark.asyncio
async def test_send_wecom_image_with_api_error(mock_image_send, fs):
    """Test send_wecom_image function with API error."""
    # Create test image file
    fs.create_file("/test/image.jpg", contents=b"test image content")

    # Unpack fixtures
    _, _, mock_notify_bridge, _, mock_nb_instance = mock_image_send

    # Setup mock response with API error
    mock_response = MagicMock()
    mock_response.success = True
    mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}
    mock_nb_instance.send_async.return_value = mock_response

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await send_wecom_image("/test/image.jpg")

    # Assertions
    assert "WeChat API error: invalid credential" in str(excinfo.value)


@pytest.mark.asyncio
async def test_send_wecom_image_with_context(mock_image_with_context):
    """Test send_wecom_image function with context."""
    # Unpack fixtures
    _, _, _, _, _, mock_ctx = mock_image_with_context

    # Call function
    result = await send_wecom_image("test_image.jpg", mock_ctx)

    # Assertions
    assert result["status"] == "success"

    # Verify context methods were called
    mock_ctx.report_progress.assert_called()
    mock_ctx.info.assert_called()


@pytest.mark.asyncio
async def test_send_wecom_image_with_notify_bridge_error_and_context(
    mock_notify_bridge_error_with_context, mock_webhook_url, mock_image_processing
):
    """Test send_wecom_image function with NotifyBridge error and context."""
    # Unpack the fixture
    _, mock_ctx = mock_notify_bridge_error_with_context

    # Call function
    with pytest.raises(WeComError) as exc_info:
        await send_wecom_image("test.jpg", ctx=mock_ctx)

    # Check error message
    assert "Error sending image: Connection error" in str(exc_info.value)

    # Verify context methods were called
    mock_ctx.error.assert_called_with("Error sending image: Connection error")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.aiohttp.ClientSession")
async def test_download_image_http_error_with_context(mock_client_session):
    """Test download_image with HTTP error and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Create a proper async context manager for ClientSession
    mock_session = AsyncMock()
    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session
    mock_client_session.return_value = mock_session_cm

    # Setup the response
    mock_response = AsyncMock()
    mock_response.status = 404
    mock_response.read = AsyncMock(return_value=b"not found")

    # Create a proper async context manager for the response
    mock_response_cm = AsyncMock()
    mock_response_cm.__aenter__.return_value = mock_response

    # Setup the get method to return the mock response context manager
    mock_session.get.return_value = mock_response_cm

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await download_image("https://example.com/not-found.jpg", mock_ctx)

    # Assertions
    assert "Failed to download image: HTTP 404" in str(excinfo.value)
    mock_ctx.error.assert_called_once()
    mock_session.get.assert_called_once_with("https://example.com/not-found.jpg")


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.aiohttp.ClientSession")
async def test_download_image_invalid_content_type_with_context(mock_client_session):
    """Test download_image with invalid content type and context."""
    # Setup mock context
    mock_ctx = AsyncMock()

    # Create a proper async context manager for ClientSession
    mock_session = AsyncMock()
    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session
    mock_client_session.return_value = mock_session_cm

    # Setup the response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.read = AsyncMock(return_value=b"invalid data")

    # Create a proper async context manager for the response
    mock_response_cm = AsyncMock()
    mock_response_cm.__aenter__.return_value = mock_response

    # Setup the get method to return the mock response context manager
    mock_session.get.return_value = mock_response_cm

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await download_image("https://example.com/image.jpg", mock_ctx)

    # Assertions
    assert "Invalid content type: text/html" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
async def test_send_wecom_image_with_api_error_and_context():
    """Test send_wecom_image function with API error and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Setup mock for image processing
    with patch("wecom_bot_mcp_server.image._process_image_path") as mock_process_image:
        # Return a valid path
        mock_process_image.return_value = Path("test.jpg")

        # Setup mock for webhook URL
        with patch("wecom_bot_mcp_server.image._get_webhook_url") as mock_get_webhook_url:
            mock_get_webhook_url.return_value = "https://example.com/webhook"

            # Setup mock for sending image
            with patch("wecom_bot_mcp_server.image._send_image_to_wecom") as mock_send_image:
                # Create a mock response with API error
                mock_response = MagicMock()
                mock_response.success = True
                mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}
                mock_send_image.return_value = mock_response

                # Call function with expected exception
                with pytest.raises(WeComError) as excinfo:
                    await send_wecom_image("test.jpg", mock_ctx)

                # Assertions
                assert "WeChat API error: invalid credential" in str(excinfo.value)


@pytest.mark.asyncio
async def test_send_wecom_image_with_webhook_error(mock_image_processing):
    """Test send_wecom_image function with webhook error."""
    # Patch get_webhook_url to raise WeComError
    with patch("wecom_bot_mcp_server.image.get_webhook_url") as mock_get_webhook_url:
        mock_get_webhook_url.side_effect = WeComError("WECOM_WEBHOOK_URL environment variable not set")

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await send_wecom_image("test.jpg")

        # Assertions
        assert "WECOM_WEBHOOK_URL environment variable not set" in str(excinfo.value)


@pytest.mark.asyncio
async def test_send_wecom_image_with_webhook_error_and_context(mock_image_processing):
    """Test send_wecom_image function with webhook error and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Patch get_webhook_url to raise WeComError
    with patch("wecom_bot_mcp_server.image.get_webhook_url") as mock_get_webhook_url:
        mock_get_webhook_url.side_effect = WeComError("WECOM_WEBHOOK_URL environment variable not set")

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await send_wecom_image("test.jpg", mock_ctx)

        # Assertions
        assert "WECOM_WEBHOOK_URL environment variable not set" in str(excinfo.value)
        mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
@patch("wecom_bot_mcp_server.image.aiohttp.ClientSession")
async def test_download_image_invalid_content_type_with_context(mock_client_session):
    """Test download_image with invalid content type and context."""
    # Setup mock context
    mock_ctx = AsyncMock()

    # Create a proper async context manager for ClientSession
    mock_session = AsyncMock()
    mock_session_cm = AsyncMock()
    mock_session_cm.__aenter__.return_value = mock_session
    mock_client_session.return_value = mock_session_cm

    # Setup the response
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.headers = {"Content-Type": "text/html"}
    mock_response.read = AsyncMock(return_value=b"invalid data")

    # Create a proper async context manager for the response
    mock_response_cm = AsyncMock()
    mock_response_cm.__aenter__.return_value = mock_response

    # Setup the get method to return the mock response context manager
    mock_session.get.return_value = mock_response_cm

    # Call function with expected exception
    with pytest.raises(WeComError) as excinfo:
        await download_image("https://example.com/image.jpg", mock_ctx)

    # Assertions
    assert "Invalid content type: text/html" in str(excinfo.value)
    mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
async def test_send_wecom_image_with_webhook_error_and_context(mock_image_processing):
    """Test send_wecom_image function with webhook error and context."""
    # Create mock context
    mock_ctx = AsyncMock()

    # Patch get_webhook_url to raise WeComError
    with patch("wecom_bot_mcp_server.image.get_webhook_url") as mock_get_webhook_url:
        mock_get_webhook_url.side_effect = WeComError("WECOM_WEBHOOK_URL environment variable not set")

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await send_wecom_image("test.jpg", mock_ctx)

        # Assertions
        assert "WECOM_WEBHOOK_URL environment variable not set" in str(excinfo.value)
        assert mock_ctx.error.called


@pytest.mark.asyncio
async def test_download_image_invalid_content_type_with_context():
    """Test download_image with invalid content type and context."""
    # Setup mock context
    mock_ctx = AsyncMock()

    # Setup mock response with invalid content type
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession") as mock_session_class:
        # Create a mock session
        mock_session = MagicMock()

        # Setup the response
        mock_response = MagicMock()
        mock_response.status = 200
        mock_response.headers = {"Content-Type": "text/html"}
        mock_response.read = AsyncMock(return_value=b"invalid data")

        # Setup the get method to return a context manager that returns the mock response
        mock_get_cm = MagicMock()
        mock_get_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_get_cm)

        # Setup session context manager
        mock_session_cm = MagicMock()
        mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session_cm

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await download_image("https://example.com/image.jpg", mock_ctx)

        # Assertions
        assert "Invalid content type: text/html" in str(excinfo.value)
        mock_ctx.error.assert_called_once()


@pytest.mark.asyncio
async def test_download_image_http_error_with_context():
    """Test download_image with HTTP error and context."""
    # Setup mock context
    mock_ctx = AsyncMock()

    # Setup mock response with HTTP error
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession") as mock_session_class:
        # Create a mock session
        mock_session = MagicMock()

        # Setup the response
        mock_response = MagicMock()
        mock_response.status = 404
        mock_response.read = AsyncMock(return_value=b"not found")

        # Setup the get method to return a context manager that returns the mock response
        mock_get_cm = MagicMock()
        mock_get_cm.__aenter__ = AsyncMock(return_value=mock_response)
        mock_get_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session.get = MagicMock(return_value=mock_get_cm)

        # Setup session context manager
        mock_session_cm = MagicMock()
        mock_session_cm.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session_cm.__aexit__ = AsyncMock(return_value=None)
        mock_session_class.return_value = mock_session_cm

        # Call function with expected exception
        with pytest.raises(WeComError) as excinfo:
            await download_image("https://example.com/not-found.jpg", mock_ctx)

        # Assertions
        assert "Failed to download image: HTTP 404" in str(excinfo.value)
        mock_ctx.error.assert_called_once()
        mock_session.get.assert_called_once_with("https://example.com/not-found.jpg")
