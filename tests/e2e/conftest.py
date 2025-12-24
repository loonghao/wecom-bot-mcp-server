"""E2E test configuration and fixtures."""

# Import built-in modules
from collections.abc import AsyncGenerator
import os

# Import third-party modules
from mcp.client.session import ClientSession
from mcp.shared.memory import create_connected_server_and_client_session
import pytest

# Import local modules
# Import local modules - import all modules to register tools with mcp
from wecom_bot_mcp_server.app import mcp

# These imports are needed to register the tools with the mcp instance
import wecom_bot_mcp_server.file
import wecom_bot_mcp_server.image
import wecom_bot_mcp_server.message


@pytest.fixture
def anyio_backend():
    """Configure anyio to use asyncio backend."""
    return "asyncio"


@pytest.fixture
async def client_session() -> AsyncGenerator[ClientSession, None]:
    """Create an in-memory MCP client session connected to the server.

    This fixture creates a direct in-memory connection between the MCP client
    and server, allowing for fast and isolated testing without network overhead.

    Yields:
        ClientSession: An initialized MCP client session ready for testing.

    """
    async with create_connected_server_and_client_session(mcp, raise_exceptions=True) as session:
        yield session


@pytest.fixture
def wecom_webhook_url() -> str | None:
    """Get WeCom webhook URL from environment variable.

    Returns:
        str | None: The webhook URL if set, None otherwise.

    """
    return os.environ.get("WECOM_WEBHOOK_URL")


@pytest.fixture
def skip_if_no_webhook(wecom_webhook_url: str | None):
    """Skip test if WECOM_WEBHOOK_URL is not set.

    This fixture is used to conditionally skip real E2E tests
    when the webhook URL is not configured.
    """
    if not wecom_webhook_url:
        pytest.skip("WECOM_WEBHOOK_URL environment variable not set")


def pytest_configure(config):
    """Register custom markers for E2E tests."""
    config.addinivalue_line("markers", "e2e: mark test as end-to-end test")
    config.addinivalue_line("markers", "e2e_real: mark test as real E2E test requiring actual webhook")
