"""Pytest configuration file."""

# Import built-in modules
import os
from pathlib import Path
import sys
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

# Import third-party modules
import aiohttp
from pyfakefs.fake_filesystem_unittest import Patcher
import pytest

# Import local modules
from wecom_bot_mcp_server.errors import WeComError

# Add the src directory to the Python path so tests use the local package
ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


class AsyncContextManagerMock:
    """Helper class for mocking asynchronous context managers."""

    def __init__(self, return_value=None):
        self.return_value = return_value or AsyncMock()
        self.enter_called = False
        self.exit_called = False

    async def __aenter__(self):
        self.enter_called = True
        return self.return_value

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.exit_called = True
        return False


class MockClientResponse(AsyncMock):
    """Mock for aiohttp.ClientResponse with async context manager support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.status = kwargs.get("status", 200)
        self.reason = kwargs.get("reason", "")
        self.headers = kwargs.get("headers", {})
        self.content = AsyncMock()
        self.content.read = AsyncMock(return_value=b"")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


class MockClientSession(AsyncMock):
    """Mock for aiohttp.ClientSession with async context manager support."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = kwargs.get("response", None)

    def get(self, *args, **kwargs):
        return self.response or MockClientResponse()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return False


def create_async_mock_session(response_mock=None):
    """Create a mock aiohttp ClientSession with proper async context manager support.

    Args:
        response_mock: Optional mock response to return from session.get()

    Returns:
        MockClientSession: A properly configured mock session

    """
    # If no response mock is provided, create one
    if response_mock is None:
        response_mock = MockClientResponse()

    # Create a session that returns our response
    session_mock = MockClientSession(response=response_mock)

    return session_mock


@pytest.fixture
def fs():
    """Fixture for pyfakefs."""
    with Patcher() as patcher:
        yield patcher.fs


@pytest.fixture
def mock_notify_bridge():
    """Fixture for mocking NotifyBridge."""
    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as message_mock,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as image_mock,
    ):
        # Setup mock response
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "errmsg": "ok"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response

        # Setup both mocks to return the same instance
        message_mock.return_value.__aenter__.return_value = mock_nb_instance
        image_mock.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_nb_instance


@pytest.fixture
def mock_notify_bridge_error():
    """Fixture for mocking NotifyBridge with error."""
    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as message_mock,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as image_mock,
    ):
        # Setup NotifyBridge instance with error
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.side_effect = Exception("Connection error")

        # Setup both mocks to return the same instance
        message_mock.return_value.__aenter__.return_value = mock_nb_instance
        image_mock.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_nb_instance


@pytest.fixture
def mock_notify_bridge_error_with_context():
    """Fixture for mocking NotifyBridge with error and context."""
    # Setup context
    mock_ctx = AsyncMock()

    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as message_mock,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as image_mock,
    ):
        # Setup NotifyBridge instance with error
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.side_effect = Exception("Connection error")

        # Setup both mocks to return the same instance
        message_mock.return_value.__aenter__.return_value = mock_nb_instance
        image_mock.return_value.__aenter__.return_value = mock_nb_instance

        yield (mock_nb_instance, mock_ctx)


@pytest.fixture
def mock_notify_bridge_api_error():
    """Fixture for mocking NotifyBridge with API error."""
    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as message_mock,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as image_mock,
    ):
        # Setup mock response with API error
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response

        # Setup both mocks to return the same instance
        message_mock.return_value.__aenter__.return_value = mock_nb_instance
        image_mock.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_nb_instance


@pytest.fixture
def mock_notify_bridge_api_error_with_context():
    """Fixture for mocking NotifyBridge with API error and context."""
    # Setup context
    mock_ctx = AsyncMock()

    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as message_mock,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as image_mock,
    ):
        # Setup mock response with API error
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response

        # Setup both mocks to return the same instance
        message_mock.return_value.__aenter__.return_value = mock_nb_instance
        image_mock.return_value.__aenter__.return_value = mock_nb_instance

        yield (mock_nb_instance, mock_ctx)


@pytest.fixture
def mock_notify_bridge_network_error():
    """Fixture for mocking NotifyBridge with network error."""
    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as message_mock,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as image_mock,
    ):
        # Setup NotifyBridge instance with network error
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.side_effect = Exception("Network connection failed")

        # Setup both mocks to return the same instance
        message_mock.return_value.__aenter__.return_value = mock_nb_instance
        image_mock.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_nb_instance


@pytest.fixture
def mock_notify_bridge_network_error_with_context():
    """Fixture for mocking NotifyBridge with network error and context."""
    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as message_mock,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as image_mock,
    ):
        # Setup NotifyBridge instance with network error
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.side_effect = Exception("Network connection failed")

        # Setup both mocks to return the same instance
        message_mock.return_value.__aenter__.return_value = mock_nb_instance
        image_mock.return_value.__aenter__.return_value = mock_nb_instance

        # Create mock context
        mock_ctx = AsyncMock()

        yield mock_nb_instance, mock_ctx


@pytest.fixture
def mock_webhook_url():
    """Fixture for mocking get_bot_registry function."""
    with (
        patch("wecom_bot_mcp_server.message.get_bot_registry") as message_mock,
        patch("wecom_bot_mcp_server.image.get_bot_registry") as image_mock,
    ):
        # Setup mock registry
        mock_registry = MagicMock()
        mock_registry.get_webhook_url.return_value = "https://example.com/webhook"

        # Setup both mocks to return the same registry
        message_mock.return_value = mock_registry
        image_mock.return_value = mock_registry

        yield "https://example.com/webhook"


@pytest.fixture
def mock_image_processing():
    """Fixture for mocking image processing functions."""
    with (
        patch("wecom_bot_mcp_server.image.Path.exists") as exists_mock,
        patch("wecom_bot_mcp_server.image.Image.open") as image_open_mock,
    ):
        # Setup mocks
        exists_mock.return_value = True
        image_open_mock.return_value = MagicMock()

        yield (exists_mock, image_open_mock)


@pytest.fixture
def mock_http_error_response():
    """Fixture for mocking HTTP error response."""
    # Setup mock response with 404 status
    mock_response = MockClientResponse(status=404, reason="Not Found")

    # Create mock session
    mock_session = create_async_mock_session(mock_response)

    # Patch ClientSession
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession", return_value=mock_session):
        yield mock_response


@pytest.fixture
def mock_http_error_response_with_context():
    """Fixture for mocking HTTP error response with context."""
    # Setup mock response with 404 status
    mock_response = MockClientResponse(status=404, reason="Not Found")

    # Create mock session
    mock_session = create_async_mock_session(mock_response)

    # Setup context
    mock_ctx = AsyncMock()

    # Patch ClientSession
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession", return_value=mock_session):
        yield (mock_response, mock_ctx)


@pytest.fixture
def mock_invalid_content_type_response():
    """Fixture for mocking invalid content type response."""
    # Setup mock response with invalid content type
    mock_response = MockClientResponse(status=200, headers={"Content-Type": "text/html"})

    # Create mock session
    mock_session = create_async_mock_session(mock_response)

    # Patch ClientSession
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession", return_value=mock_session):
        yield mock_response


@pytest.fixture
def mock_invalid_content_type_with_context():
    """Fixture for mocking invalid content type response with context."""
    # Setup mock response with invalid content type
    mock_response = MockClientResponse(status=200, headers={"Content-Type": "text/html"})

    # Create mock session
    mock_session = create_async_mock_session(mock_response)

    # Setup context
    mock_ctx = AsyncMock()

    # Patch ClientSession
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession", return_value=mock_session):
        yield (mock_response, mock_ctx)


@pytest.fixture
def mock_network_error():
    """Fixture for mocking network error."""
    # Patch ClientSession to raise a network error
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession") as mock_client_session:
        mock_client_session.side_effect = aiohttp.ClientError("Network error")
        yield mock_client_session


@pytest.fixture
def mock_network_error_with_context():
    """Fixture for mocking network error with context."""
    # Setup context
    mock_ctx = AsyncMock()

    # Patch ClientSession to raise a network error
    with patch("wecom_bot_mcp_server.image.aiohttp.ClientSession") as mock_client_session:
        mock_client_session.side_effect = aiohttp.ClientError("Network error")
        yield (mock_client_session, mock_ctx)


@pytest.fixture
def mock_file_operations():
    """Fixture for mocking file operations."""
    with (
        patch("wecom_bot_mcp_server.file.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.file.Path.is_file") as mock_is_file,
        patch("wecom_bot_mcp_server.file.Path.stat") as mock_stat,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_file.return_value = True

        # Setup stat mock
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 1024
        mock_stat.return_value = mock_stat_result

        yield mock_exists, mock_is_file, mock_stat


@pytest.fixture
def mock_file_api():
    """Fixture for mocking file API operations."""
    with (
        patch("wecom_bot_mcp_server.file.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.file.get_webhook_url") as mock_get_webhook_url,
    ):
        # Setup webhook URL
        mock_get_webhook_url.return_value = "https://example.com/webhook"

        # Setup NotifyBridge response
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "media_id": "test_media_id"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_notify_bridge, mock_get_webhook_url, mock_nb_instance


@pytest.fixture
def mock_file_api_error():
    """Fixture for mocking file API error."""
    with (
        patch("wecom_bot_mcp_server.file.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.file.get_webhook_url") as mock_get_webhook_url,
    ):
        # Setup webhook URL
        mock_get_webhook_url.return_value = "https://example.com/webhook"

        # Setup NotifyBridge response with API error
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 40001, "errmsg": "invalid credential"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_notify_bridge, mock_get_webhook_url, mock_nb_instance


@pytest.fixture
def mock_file_response_failure():
    """Fixture for mocking file response failure."""
    with (
        patch("wecom_bot_mcp_server.file.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.file.get_webhook_url") as mock_get_webhook_url,
    ):
        # Setup webhook URL
        mock_get_webhook_url.return_value = "https://example.com/webhook"

        # Setup NotifyBridge response with failure
        mock_response = MagicMock()
        mock_response.success = False
        mock_response.data = {}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_notify_bridge, mock_get_webhook_url, mock_nb_instance


@pytest.fixture
def mock_file_exists():
    """Fixture for mocking file exists."""
    with (
        patch("wecom_bot_mcp_server.file.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.file.Path.is_file") as mock_is_file,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_file.return_value = True

        yield mock_exists, mock_is_file


@pytest.fixture
def mock_file_not_a_file():
    """Fixture for mocking file that is not a file but a directory."""
    with (
        patch("wecom_bot_mcp_server.file.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.file.Path.is_file") as mock_is_file,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_file.return_value = False

        yield mock_exists, mock_is_file


@pytest.fixture
def mock_file_not_found():
    """Fixture for mocking file not found."""
    with (
        patch("wecom_bot_mcp_server.file.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.file.Path.is_file") as mock_is_file,
    ):
        # Setup mocks
        mock_exists.return_value = False
        mock_is_file.return_value = False

        yield mock_exists, mock_is_file


@pytest.fixture
def mock_file_send():
    """Fixture for mocking file send operations."""
    with patch("wecom_bot_mcp_server.file.NotifyBridge") as mock_notify_bridge:
        # Setup NotifyBridge response
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "media_id": "test_media_id"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_notify_bridge, mock_nb_instance, mock_response


@pytest.fixture
def mock_file_stat():
    """Fixture for mocking file stat operations."""
    with patch("wecom_bot_mcp_server.file.Path.stat") as mock_stat:
        # Setup stat mock
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 2048
        mock_stat.return_value = mock_stat_result

        yield mock_stat, mock_stat_result


@pytest.fixture
def mock_file_with_context():
    """Fixture for mocking file operations with context."""
    with (
        patch("wecom_bot_mcp_server.file.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.file.Path.is_file") as mock_is_file,
        patch("wecom_bot_mcp_server.file.Path.stat") as mock_stat,
        patch("wecom_bot_mcp_server.file.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.file.get_webhook_url") as mock_get_webhook_url,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_get_webhook_url.return_value = "https://example.com/webhook"

        # Setup stat mock
        mock_stat_result = MagicMock()
        mock_stat_result.st_size = 1024
        mock_stat.return_value = mock_stat_result

        # Setup NotifyBridge response
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "media_id": "test_media_id"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        # Create mock context
        mock_ctx = AsyncMock()

        yield (
            mock_exists,
            mock_is_file,
            mock_stat,
            mock_notify_bridge,
            mock_get_webhook_url,
            mock_nb_instance,
            mock_response,
            mock_ctx,
        )


@pytest.fixture
def mock_get_webhook_url():
    """Fixture for mocking get_webhook_url function."""
    with patch("wecom_bot_mcp_server.file.get_webhook_url") as mock_get_webhook_url:
        # Setup mock
        mock_get_webhook_url.return_value = "https://example.com/webhook"

        yield mock_get_webhook_url


@pytest.fixture
def mock_get_webhook_url_error():
    """Fixture for mocking get_webhook_url function with error."""
    with patch("wecom_bot_mcp_server.file.get_webhook_url") as mock_get_webhook_url:
        # Setup mock
        mock_get_webhook_url.side_effect = WeComError("Webhook URL not found")

        yield mock_get_webhook_url


@pytest.fixture
def mock_file_network_error():
    """Fixture for mocking file network error."""
    with (
        patch("wecom_bot_mcp_server.file.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.file.Path.is_file") as mock_is_file,
        patch("wecom_bot_mcp_server.file.get_webhook_url") as mock_get_webhook_url,
        patch("wecom_bot_mcp_server.file.NotifyBridge") as mock_notify_bridge,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_file.return_value = True
        mock_get_webhook_url.return_value = "https://example.com/webhook"

        # Setup NotifyBridge to raise an exception
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.side_effect = Exception("Network connection failed")
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_exists, mock_is_file, mock_get_webhook_url, mock_notify_bridge, mock_nb_instance


@pytest.fixture
def mock_image_send():
    """Fixture for mocking image send operations."""
    with (
        patch("wecom_bot_mcp_server.image.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.image.Image.open") as mock_image_open,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.image.get_bot_registry") as mock_get_bot_registry,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_image_open.return_value = MagicMock()

        # Setup mock registry
        mock_registry = MagicMock()
        mock_registry.get_webhook_url.return_value = "https://example.com/webhook"
        mock_get_bot_registry.return_value = mock_registry

        # Setup NotifyBridge mock with proper response object
        mock_nb_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "errmsg": "ok"}
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_exists, mock_image_open, mock_notify_bridge, mock_get_bot_registry, mock_nb_instance


@pytest.fixture
def mock_image_download():
    """Fixture for mocking image download operations."""
    with (
        patch("wecom_bot_mcp_server.image.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.image.Image.open") as mock_image_open,
        patch("wecom_bot_mcp_server.image.download_image") as mock_download_image,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_image_open.return_value = MagicMock()
        mock_download_image.return_value = "downloaded_image.jpg"

        yield mock_exists, mock_image_open, mock_download_image


@pytest.fixture
def mock_image_not_found():
    """Fixture for mocking image not found."""
    with (
        patch("wecom_bot_mcp_server.image.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.image.Path.is_file") as mock_is_file,
    ):
        # Setup mocks
        mock_exists.return_value = False
        mock_is_file.return_value = False

        yield mock_exists, mock_is_file


@pytest.fixture
def mock_image_not_a_file():
    """Fixture for mocking image that is not a file but a directory."""
    with (
        patch("wecom_bot_mcp_server.image.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.image.Path.is_file") as mock_is_file,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_is_file.return_value = False

        yield mock_exists, mock_is_file


@pytest.fixture
def mock_image_network_error():
    """Fixture for mocking image network error."""
    with (
        patch("wecom_bot_mcp_server.image.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.image.Image.open") as mock_image_open,
        patch("wecom_bot_mcp_server.image.get_bot_registry") as mock_get_bot_registry,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as mock_notify_bridge,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_image_open.return_value = MagicMock()

        # Setup mock registry
        mock_registry = MagicMock()
        mock_registry.get_webhook_url.return_value = "https://example.com/webhook"
        mock_get_bot_registry.return_value = mock_registry

        # Setup NotifyBridge to raise an exception
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.side_effect = Exception("Network connection failed")
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_exists, mock_image_open, mock_get_bot_registry, mock_notify_bridge, mock_nb_instance


@pytest.fixture
def mock_image_with_context():
    """Fixture for mocking image operations with context."""
    with (
        patch("wecom_bot_mcp_server.image.Path.exists") as mock_exists,
        patch("wecom_bot_mcp_server.image.Image.open") as mock_image_open,
        patch("wecom_bot_mcp_server.image.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.image.get_bot_registry") as mock_get_bot_registry,
    ):
        # Setup mocks
        mock_exists.return_value = True
        mock_image_open.return_value = MagicMock()

        # Setup mock registry
        mock_registry = MagicMock()
        mock_registry.get_webhook_url.return_value = "https://example.com/webhook"
        mock_get_bot_registry.return_value = mock_registry

        # Setup NotifyBridge mock
        mock_nb_instance = AsyncMock()
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "errmsg": "ok"}
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        # Create mock context
        mock_ctx = AsyncMock()

        yield mock_exists, mock_image_open, mock_notify_bridge, mock_get_bot_registry, mock_nb_instance, mock_ctx


@pytest.fixture
def mock_message_send():
    """Fixture for mocking message send operations."""
    with (
        patch("wecom_bot_mcp_server.message.NotifyBridge") as mock_notify_bridge,
        patch("wecom_bot_mcp_server.message.get_bot_registry") as mock_get_bot_registry,
    ):
        # Setup mock registry
        mock_registry = MagicMock()
        mock_registry.get_webhook_url.return_value = "https://example.com/webhook"
        mock_get_bot_registry.return_value = mock_registry

        # Setup NotifyBridge response
        mock_response = MagicMock()
        mock_response.success = True
        mock_response.data = {"errcode": 0, "errmsg": "ok"}

        # Setup NotifyBridge instance
        mock_nb_instance = AsyncMock()
        mock_nb_instance.send_async.return_value = mock_response
        mock_notify_bridge.return_value.__aenter__.return_value = mock_nb_instance

        yield mock_notify_bridge, mock_get_bot_registry, mock_nb_instance


@pytest.fixture(autouse=True)
def setup_env(request):
    """Set up environment variables for tests.

    Note: This fixture does NOT apply to e2e tests to avoid overriding
    the real WECOM_WEBHOOK_URL environment variable.
    Also skips for tests that need to control their own environment.
    """
    # Skip this fixture for e2e tests
    if "e2e" in str(request.fspath):
        yield
        return

    # Skip for tests that manage their own environment
    test_cls = getattr(request.node, "cls", None)
    if test_cls is not None:
        if test_cls.__name__ in ("TestMultiBotInstructions", "TestListAvailableBots"):
            yield
            return

    # Save original value if exists
    original_url = os.environ.get("WECOM_WEBHOOK_URL")

    # Set up test environment variables
    os.environ["WECOM_WEBHOOK_URL"] = "https://example.com/webhook/test"
    yield
    # Clean up - restore original or delete
    if original_url is not None:
        os.environ["WECOM_WEBHOOK_URL"] = original_url
    elif "WECOM_WEBHOOK_URL" in os.environ:
        del os.environ["WECOM_WEBHOOK_URL"]


@pytest.fixture(autouse=True)
def clear_message_history():
    """Clear message history before each test."""
    # Import local modules
    from wecom_bot_mcp_server import message

    # Clear message history before test
    message.message_history.clear()
    yield
    # Clear message history after test
    message.message_history.clear()


@pytest.fixture(autouse=True)
def clear_lru_cache():
    """Clear lru_cache for get_webhook_url before each test."""
    # Import local modules
    from wecom_bot_mcp_server.utils import get_webhook_url

    # Clear cache before test
    get_webhook_url.cache_clear()
    yield
    # Clear cache after test
    get_webhook_url.cache_clear()


@pytest.fixture(autouse=True)
def reset_bot_registry(request):
    """Reset global bot registry before each test.

    This ensures test isolation by clearing the singleton registry,
    preventing state leakage between tests.

    Note: Skips for tests that manage their own registry state.
    """
    # Import local modules
    import wecom_bot_mcp_server.bot_config as bot_config

    # Skip for tests that manage their own registry
    test_cls = getattr(request.node, "cls", None)
    if test_cls is not None:
        if test_cls.__name__ in ("TestMultiBotInstructions", "TestListAvailableBots"):
            yield
            return

    # Reset the global registry before test
    bot_config._bot_registry = None
    yield
    # Reset after test as well
    bot_config._bot_registry = None
