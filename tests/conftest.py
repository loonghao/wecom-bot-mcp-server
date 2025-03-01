"""Pytest configuration file."""

# Import built-in modules
import os
from pathlib import Path
import sys

# Import third-party modules
import pytest

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(autouse=True)
def setup_env():
    """Set up environment variables for tests."""
    # Set up test environment variables
    os.environ["WECOM_WEBHOOK_URL"] = "https://example.com/webhook/test"
    yield
    # Clean up
    if "WECOM_WEBHOOK_URL" in os.environ:
        del os.environ["WECOM_WEBHOOK_URL"]
