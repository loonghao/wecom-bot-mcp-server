"""Tests for server module."""

# Import built-in modules
import unittest
from unittest.mock import patch

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


if __name__ == "__main__":
    unittest.main()
