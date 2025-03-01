"""Logging configuration for WeCom Bot MCP Server."""

# Import built-in modules
import os
from pathlib import Path
import sys
from typing import Any

# Import third-party modules
from loguru import logger
from platformdirs import user_log_dir

# Import local modules
from wecom_bot_mcp_server.app import APP_NAME


class LoggerWrapper:
    """Wrapper class to provide a logging.Logger-like interface for loguru."""

    def __init__(self, name: str):
        """Initialize logger wrapper with a name.

        Args:
            name: The name of the logger.

        """
        self.name = name

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).error(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).info(msg, *args, **kwargs)

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).debug(msg, *args, **kwargs)

    def warning(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).warning(msg, *args, **kwargs)

    def critical(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).critical(msg, *args, **kwargs)

    def exception(self, msg: str, *args: Any, **kwargs: Any) -> None:
        """Log an exception message.

        Args:
            msg: The message to log.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        """
        logger.bind(name=self.name).exception(msg, *args, **kwargs)


# Constants
LOG_DIR = Path(user_log_dir(APP_NAME))
LOG_FILE = LOG_DIR / "mcp_wecom.log"
LOG_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan> - "
    "<level>{level}</level> - <level>{message}</level>"
)
LOG_LEVEL = os.getenv("MCP_LOG_LEVEL", "DEBUG").upper()


def setup_logging() -> LoggerWrapper:
    """Configure logging settings for the application using loguru.

    Returns:
        LoggerWrapper: Configured logger instance that provides a logging.Logger-like interface

    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Remove any existing handlers
    logger.remove()

    # Add rotating file handler
    logger.add(
        LOG_FILE,
        rotation="2 GB",
        retention="10 days",
        compression="zip",
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        enqueue=True,
        encoding="utf-8",
    )

    # Add console handler
    logger.add(sys.stdout, format=LOG_FORMAT, level=LOG_LEVEL, enqueue=True)

    logger_wrapper = LoggerWrapper("mcp_wechat_server")
    logger_wrapper.info(f"Log file location: {LOG_FILE}")
    return logger_wrapper
