"""Error handling for WeCom Bot MCP Server."""

# Import built-in modules
from enum import Enum
from enum import auto


class ErrorCode(Enum):
    """Error codes for WeCom Bot MCP Server."""

    UNKNOWN = auto()
    VALIDATION_ERROR = auto()
    NETWORK_ERROR = auto()
    API_FAILURE = auto()
    FILE_ERROR = auto()


class WeComError(Exception):
    """Base exception class for WeCom Bot MCP Server."""

    def __init__(self, message: str, error_code: ErrorCode = ErrorCode.UNKNOWN):
        """Initialize WeComError.

        Args:
            message: Error message
            error_code: Error code

        """
        super().__init__(message)
        self.error_code = error_code
