"""Logger configuration for WeCom Bot MCP Server.

This module provides logging configuration for the WeCom Bot MCP Server.
It sets up both console and file logging with appropriate formatting.
"""

# Import built-in modules
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Import third-party modules
from platformdirs import PlatformDirs


# Create a bootstrap console logger for setup debugging
def _get_bootstrap_logger() -> logging.Logger:
    """Create a simple console logger for debugging setup process."""
    bootstrap_logger = logging.getLogger("logger_setup")
    if not bootstrap_logger.handlers:  # Avoid adding handlers multiple times
        bootstrap_logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter(
            "%(asctime)s - SETUP - %(levelname)s - %(message)s"
        ))
        bootstrap_logger.addHandler(handler)
    return bootstrap_logger


def _get_log_level() -> int:
    """Get log level from environment variable or return default.

    Returns:
        int: Logging level (e.g., logging.DEBUG, logging.INFO)
    """
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    return getattr(logging, level_name, logging.INFO)


# Constants
APP_NAME = "wecom-bot-mcp-server"
APP_AUTHOR = "mcp"

def setup_logger(name: str) -> logging.Logger:
    """Setup and configure logger with both console and file output.

    Args:
        name: Logger name

    Returns:
        logging.Logger: Configured logger instance
    """
    # Get log level from environment variable
    log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
    log_level = getattr(logging, log_level_str, logging.INFO)

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicate logs
    logger.handlers.clear()

    # Create formatters
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    formatter = logging.Formatter(log_format)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Get platform-specific log directory
    dirs = PlatformDirs(APP_NAME, APP_AUTHOR)
    log_dir = Path(dirs.user_log_dir)

    try:
        # Create logs directory if it doesn't exist
        log_dir.mkdir(parents=True, exist_ok=True)

        # Create file handler
        log_file = log_dir / f"{name}.log"
        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Log initial messages
        logger.info("Logger setup completed - This is an info message")
        logger.debug("Logger debug level enabled")
        logger.info(f"Log file location: {log_file.absolute()}")
    except Exception as e:
        logger.error(f"Failed to setup file logging: {e}", exc_info=True)
        logger.warning("Continuing with console logging only")

    return logger
