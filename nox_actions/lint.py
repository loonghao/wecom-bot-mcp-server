# Import third-party modules
import nox

from nox_actions.utils import PACKAGE_NAME


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


def lint_fix(session: nox.Session) -> None:
    """Fix linting issues."""
    session.install("ruff", "black", "isort")

    # Fix imports
    session.run("isort", ".")

    # Fix code style
    session.run("ruff", "check", "--fix", ".")
    session.run("ruff", "format", ".")
