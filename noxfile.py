"""Nox configuration file for WeCom Bot MCP Server.

This module configures Nox sessions for development tasks like testing, linting, and building.
"""

# Import built-in modules
import argparse
import os
from pathlib import Path
import shutil
import sys
import zipfile

ROOT = os.path.dirname(__file__)
THIS_ROOT = Path(ROOT)
PACKAGE_NAME = "wecom_bot_mcp_server"

# Ensure project is importable
if ROOT not in sys.path:
    sys.path.append(ROOT)

# Import third-party modules
import nox


def _assemble_env_paths(*paths):
    """Assemble environment paths separated by a semicolon.

    Args:
        *paths: Paths to be assembled.

    Returns:
        str: Assembled paths separated by a semicolon.

    """
    return ";".join(paths)


@nox.session
def lint(session):
    """Run linting checks."""
    session.install("ruff", "mypy", "isort")
    session.install("-e", ".")

    # Install missing type stubs
    session.run("mypy", "--install-types", "--non-interactive")

    # Run ruff checks
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")

    # Run isort checks
    session.run("isort", "--check-only", ".")

    # Run mypy checks
    session.run("mypy", f"src/{PACKAGE_NAME}", "--strict")


@nox.session
def lint_fix(session):
    """Fix linting issues."""
    session.install("ruff", "mypy", "isort")
    session.install("-e", ".")

    # Fix code style
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")
    # Fix imports
    session.run("isort", ".")


@nox.session
def pytest(session):
    """Run pytest with coverage."""
    # Install test dependencies
    session.install("pytest", "pytest-cov", "pytest-asyncio", "pillow", "svglib", "reportlab", "httpx", "pyfakefs")
    session.install("-e", ".")

    # Get pytest arguments
    pytest_args = session.posargs or ["tests/"]

    session.run(
        "pytest",
        *pytest_args,
        "--cov=wecom_bot_mcp_server",
        "--cov-report=xml:coverage.xml",
        "--cov-report=term-missing",
    )


@nox.session
def build(session):
    """Build the package."""
    session.install("uv")
    session.run("uv", "build")


@nox.session
def publish(session):
    """Build and publish the package to PyPI."""
    session.install("uv", "twine")
    session.run("uv", "build")
    session.run("twine", "upload", "dist/*")
