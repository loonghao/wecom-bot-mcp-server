"""Linting actions for WeCom Bot MCP Server.

This module contains Nox sessions for code linting and formatting.
"""

# Import third-party modules
import nox

# Import local modules
from nox_actions.utils import PACKAGE_NAME


def lint(session: nox.Session) -> None:
    """Run linting checks."""
    session.install("-r", "nox-requirements.txt")

    # Install missing type stubs
    session.run("mypy", "--install-types", "--non-interactive")

    # Run ruff checks
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")

    # Run isort checks
    session.run("isort", "--check-only", ".")

    # Run mypy checks
    session.run("mypy", f"src/{PACKAGE_NAME}", "--strict")


def lint_fix(session: nox.Session) -> None:
    """Fix linting issues."""
    session.install("-r", "nox-requirements.txt")

    # Fix code style
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")
    # Fix imports
    session.run("isort", ".")
