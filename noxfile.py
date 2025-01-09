# Import built-in modules
from pathlib import Path

# Import third-party modules
import nox


# Constants
PACKAGE_NAME = "wecom_bot_mcp_server"
PROJECT_ROOT = Path(__file__).parent


@nox.session
def tests(session: nox.Session) -> None:
    """Run pytest with coverage."""
    session.install("-e", ".")  # Install the package in editable mode
    session.install("pytest", "pytest-cov", "pytest-asyncio")
    session.run(
        "pytest",
        "tests/",
        "--cov=wecom_bot_mcp_server",
        "--cov-report=xml",
        "--cov-report=term-missing",
    )


@nox.session
def lint(session: nox.Session) -> None:
    """Run linting checks."""
    session.install("ruff", "black", "isort", "mypy")

    # Run ruff checks
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")

    # Run isort checks
    session.run("isort", "--check-only", ".")

    # Run mypy checks
    session.run("mypy", f"src/{PACKAGE_NAME}", "--strict")


@nox.session
def lint_fix(session: nox.Session) -> None:
    """Fix linting issues."""
    session.install("ruff", "black", "isort")

    # Fix imports
    session.run("isort", ".")

    # Fix code style
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")
