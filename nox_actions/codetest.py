"""Code testing actions for WeCom Bot MCP Server.

This module contains Nox sessions for running tests and generating coverage reports.
"""

# Import third-party modules
import nox


def pytest(session: nox.Session) -> None:
    """Run pytest with coverage."""
    # Install test dependencies
    session.install("pytest", "pytest-cov", "pytest-asyncio", "pillow", "svglib", "reportlab", "httpx")
    session.install(".")
    session.run(
        "pytest",
        "tests/",
        "--cov=wecom_bot_mcp_server",
        "--cov-report=xml:coverage.xml",
        "--cov-report=term-missing",
    )
