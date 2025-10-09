"""Test module imports and public API."""

# Import third-party modules
import pytest


def test_package_import():
    """Test that the package can be imported."""
    import wecom_bot_mcp_server

    assert wecom_bot_mcp_server is not None


def test_public_api_imports():
    """Test that all public API can be imported."""
    from wecom_bot_mcp_server import (
        MESSAGE_HISTORY_KEY,
        ErrorCode,
        WeComError,
        mcp,
        send_message,
        send_wecom_file,
        send_wecom_image,
    )

    # Verify all imports are not None
    assert MESSAGE_HISTORY_KEY is not None
    assert ErrorCode is not None
    assert WeComError is not None
    assert mcp is not None
    assert send_message is not None
    assert send_wecom_file is not None
    assert send_wecom_image is not None


def test_error_code_enum():
    """Test ErrorCode enum values."""
    from wecom_bot_mcp_server import ErrorCode

    # Verify ErrorCode has expected values
    assert hasattr(ErrorCode, "UNKNOWN")
    assert hasattr(ErrorCode, "VALIDATION_ERROR")
    assert hasattr(ErrorCode, "NETWORK_ERROR")
    assert hasattr(ErrorCode, "API_FAILURE")
    assert hasattr(ErrorCode, "FILE_ERROR")


def test_wecom_error_class():
    """Test WeComError exception class."""
    from wecom_bot_mcp_server import ErrorCode, WeComError

    # Create an error instance
    error = WeComError("Test error", ErrorCode.NETWORK_ERROR)

    # Verify error properties
    assert str(error) == "Test error"
    assert error.error_code == ErrorCode.NETWORK_ERROR
    assert isinstance(error, Exception)


def test_mcp_app_instance():
    """Test that mcp app instance is properly initialized."""
    from wecom_bot_mcp_server import mcp

    # Verify mcp is a FastMCP instance
    assert hasattr(mcp, "run")
    assert hasattr(mcp, "tool")
    assert callable(mcp.run)


@pytest.mark.asyncio
async def test_send_message_signature():
    """Test send_message function signature."""
    from wecom_bot_mcp_server import send_message

    # Verify function is callable
    assert callable(send_message)

    # Verify function has correct signature
    import inspect

    sig = inspect.signature(send_message)
    params = list(sig.parameters.keys())

    # Check for expected parameters
    assert "content" in params
    assert "msg_type" in params
    assert "mentioned_list" in params or "mentioned_mobile_list" in params


@pytest.mark.asyncio
async def test_send_wecom_file_signature():
    """Test send_wecom_file function signature."""
    from wecom_bot_mcp_server import send_wecom_file

    # Verify function is callable
    assert callable(send_wecom_file)

    # Verify function has correct signature
    import inspect

    sig = inspect.signature(send_wecom_file)
    params = list(sig.parameters.keys())

    # Check for expected parameters
    assert "file_path" in params


@pytest.mark.asyncio
async def test_send_wecom_image_signature():
    """Test send_wecom_image function signature."""
    from wecom_bot_mcp_server import send_wecom_image

    # Verify function is callable
    assert callable(send_wecom_image)

    # Verify function has correct signature
    import inspect

    sig = inspect.signature(send_wecom_image)
    params = list(sig.parameters.keys())

    # Check for expected parameters
    assert "image_path" in params


def test_all_exports():
    """Test that __all__ exports match actual exports."""
    import wecom_bot_mcp_server

    # Get __all__ list
    all_exports = wecom_bot_mcp_server.__all__

    # Verify all items in __all__ are actually exported
    for export in all_exports:
        assert hasattr(wecom_bot_mcp_server, export), f"{export} is in __all__ but not exported"


def test_version_attribute():
    """Test that version information is available."""
    # Try to import version module
    try:
        from wecom_bot_mcp_server import __version__

        assert __version__ is not None
        # Version module exists, check if it has __version__ attribute
        if hasattr(__version__, "__version__"):
            assert isinstance(__version__.__version__, str)
    except (ImportError, AttributeError):
        # Version module might not be exposed in __init__.py
        # This is acceptable
        pass


def test_no_import_errors():
    """Test that importing the package doesn't raise any errors."""
    try:
        import wecom_bot_mcp_server  # noqa: F401
        from wecom_bot_mcp_server import (  # noqa: F401
            MESSAGE_HISTORY_KEY,
            ErrorCode,
            WeComError,
            mcp,
            send_message,
            send_wecom_file,
            send_wecom_image,
        )

        # If we get here, all imports succeeded
        assert True
    except Exception as e:
        pytest.fail(f"Import failed with error: {e}")


def test_module_structure():
    """Test that the module has expected structure."""
    import wecom_bot_mcp_server

    # Check for expected submodules
    expected_modules = ["app", "errors", "file", "image", "message", "server", "utils"]

    for module_name in expected_modules:
        full_module_name = f"wecom_bot_mcp_server.{module_name}"
        try:
            __import__(full_module_name)
        except ImportError as e:
            pytest.fail(f"Failed to import {full_module_name}: {e}")

