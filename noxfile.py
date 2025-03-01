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
    session.install("pytest", "pytest-cov", "pytest-asyncio", "pillow", "svglib", "reportlab", "httpx")
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


@nox.session(name="build-exe", reuse_venv=True)
def build_exe(session):
    """Build executable version of the package.

    Args:
        session: Nox session object

    """
    parser = argparse.ArgumentParser(prog="nox -s build-exe --release")
    parser.add_argument("--release", action="store_true")
    parser.add_argument("--version", default="0.5.0", help="Version to use for the zip file")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args(session.posargs)
    build_root = THIS_ROOT / "build"
    session.install("pyoxidizer")
    session.run("pyoxidizer", "build", "install", "--path", THIS_ROOT, "--release")
    for platform_name in os.listdir(build_root):
        platform_dir = build_root / platform_name / "release" / "install"
        print(os.listdir(platform_dir))
        print(f"build {platform_name} -> {platform_dir}")

        if args.test:
            print("run tests")
            vexcle_exe = shutil.which("vexcle", path=platform_dir)
            assert os.path.exists(vexcle_exe)

        if args.release:
            temp_dir = os.path.join(THIS_ROOT, ".zip")
            version = str(args.version)
            print(f"make zip to current version: {version}")
            os.makedirs(temp_dir, exist_ok=True)
            zip_file = os.path.join(temp_dir, f"{PACKAGE_NAME}-{version}-{platform_name}.zip")
            with zipfile.ZipFile(zip_file, "w") as zip_obj:
                for root, _, files in os.walk(platform_dir):
                    for file in files:
                        zip_obj.write(
                            os.path.join(root, file),
                            os.path.relpath(os.path.join(root, file), os.path.join(platform_dir, ".")),
                        )
            print(f"Saving to {zip_file}")


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
