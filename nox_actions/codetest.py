# Import built-in modules

# Import third-party modules
import nox


def pytest(session: nox.Session) -> None:
    """Run pytest with coverage."""
    session.install("pytest", "pytest-cov", "pytest-asyncio")
    session.run(
        "pytest",
        "tests/",
        "--cov=wecom_bot_mcp_server",
        "--cov-report=xml",
        "--cov-report=term-missing",
    )
