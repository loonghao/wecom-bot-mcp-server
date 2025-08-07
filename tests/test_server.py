"""Tests for server module."""

# Import built-in modules
import unittest
from unittest.mock import patch

# Import third-party modules
import pytest

# Import local modules
from wecom_bot_mcp_server.server import main


class TestServer(unittest.TestCase):
    """Test cases for server module."""

    @patch("wecom_bot_mcp_server.server.setup_logging")
    @patch("wecom_bot_mcp_server.server.logger")
    @patch("wecom_bot_mcp_server.server.mcp")
    def test_main(self, mock_mcp, mock_logger, mock_setup_logging):
        """Test main function."""
        # Call function
        main()

        # Assertions
        mock_setup_logging.assert_called_once()
        mock_logger.info.assert_called()  # Check that logger.info was called
        mock_mcp.run.assert_called_once()


class TestFastMCPIntegration(unittest.TestCase):
    """Test cases for FastMCP integration using best practices."""

    def test_fastmcp_initialization(self):
        """Test actual FastMCP initialization without mocking."""
        # Import here to avoid import issues during module loading
        from wecom_bot_mcp_server.app import mcp

        # Test that FastMCP instance is properly initialized
        self.assertIsNotNone(mcp)
        self.assertEqual(mcp.name, "wecom_bot_mcp_server")
        self.assertIsNotNone(mcp.instructions)

        # Test that the instance has the expected attributes
        self.assertTrue(hasattr(mcp, 'run'))
        self.assertTrue(hasattr(mcp, 'name'))
        self.assertTrue(hasattr(mcp, 'instructions'))

    def test_fastmcp_no_initialization_errors(self):
        """Test that FastMCP initialization doesn't raise errors."""
        # This test ensures that the FastMCP API compatibility fix works
        # and that we don't get TypeError about unexpected keyword arguments
        try:
            from wecom_bot_mcp_server.app import mcp
            # If we get here without exceptions, the initialization worked
            self.assertIsNotNone(mcp)
        except TypeError as e:
            if "unexpected keyword argument" in str(e):
                self.fail(f"FastMCP initialization failed with API compatibility error: {e}")
            else:
                raise


if __name__ == "__main__":
    unittest.main()
