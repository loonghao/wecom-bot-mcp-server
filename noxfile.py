"""Nox configuration file for WeCom Bot MCP Server.

This module configures Nox sessions for development tasks like testing, linting, and building.
"""

# Import built-in modules
import os
import sys

ROOT = os.path.dirname(__file__)

# Ensure project is importable
if ROOT not in sys.path:
    sys.path.append(ROOT)

# Import third-party modules
import nox

# Import local modules
from nox_actions import codetest
from nox_actions import lint

# Register nox sessions
nox.session(lint.lint, name="lint")
nox.session(lint.lint_fix, name="lint-fix")
nox.session(codetest.pytest, name="pytest")
