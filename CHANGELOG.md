## v0.6.16 (2025-10-09)

### Fix

- accept NETWORK_ERROR in integration tests
- correct test expectations to match actual error codes and fixtures
- remove conflicting default and default_factory in Field
- improve testing coverage and remove unnecessary svglib dependency

## v0.6.15 (2025-09-19)

### Fix

- **deps**: update dependency platformdirs to v4.4.0

## v0.6.14 (2025-08-27)

### Fix

- **deps**: update dependency mcp to v1.13.1

## v0.6.13 (2025-08-15)

### Fix

- resolve Gemini CLI parameter schema validation issues

## v0.6.12 (2025-08-14)

### Fix

- **deps**: update dependency mcp to v1.13.0

## v0.6.11 (2025-08-14)

### Fix

- **deps**: update dependency aiohttp to v3.12.15

## v0.6.10 (2025-08-14)

### Fix

- **mcp**: provide JSON-schema-friendly tool params and export string __version__\n\n- Change send_wecom_file/file_path and send_wecom_image/image_path to str to satisfy gemini-cli PR #5694 stricter schema typing\n- Export __version__ from package to ensure server logs a string version\n\nSigned-off-by: Hal <hal.long@outlook.com>

### Refactor

- **types**: avoid parameter type mutation; use local Path vars for mypy --strict\n\n- file.py: file_path_p: Path\n- image.py: image_path_p: Path\n\nSigned-off-by: Hal <hal.long@outlook.com>

## v0.6.9 (2025-08-14)

### Fix

- **deps**: update dependency mcp to v1.12.4

## v0.6.8 (2025-08-07)

### Fix

- sync version numbers to resolve auto-bump tag conflicts
- update FastMCP initialization for compatibility with mcp 1.12.3
- **deps**: update dependency mcp to v1.10.0
- **deps**: update dependency pydantic to v2.11.7
- **deps**: update dependency mcp to v1.9.4
- **deps**: update dependency aiohttp to v3.12.13
- **deps**: update dependency aiohttp to v3.12.12
- **deps**: update dependency mcp to v1.9.3
- **deps**: update dependency mcp to v1.9.2
- **deps**: update dependency aiohttp to v3.12.4
- **deps**: update dependency mcp to v1.9.1
- **deps**: update dependency pydantic to v2.11.5
- **deps**: update dependency aiohttp to v3.12.0
- **deps**: update dependency mcp to v1.9.0
- **deps**: update dependency mcp to v1.8.0
- **deps**: update dependency platformdirs to v4.3.8
- **deps**: update dependency mcp to v1.7.1
- **deps**: update dependency aiohttp to v3.11.18
- **deps**: update dependency pydantic to v2.11.4

## v0.6.7 (2025-04-16)

### Fix

- **deps**: update dependency pillow to v11.2.1

## v0.6.6 (2025-04-09)

### Fix

- **deps**: update dependency pydantic to v2.11.3

## v0.6.5 (2025-04-07)

### Fix

- **deps**: update dependency tenacity to v9.1.2

## v0.6.4 (2025-04-07)

### Fix

- **deps**: update dependency pydantic to v2.11.2

## v0.6.3 (2025-03-30)

### Fix

- **deps**: update dependency pydantic to v2.11.1

## v0.6.2 (2025-03-20)

### Fix

- **deps**: update dependency platformdirs to v4.3.7

## v0.6.1 (2025-03-19)

### Fix

- **deps**: update dependency aiohttp to v3.11.14

## v0.6.0 (2025-03-17)

### Feat

- Add progress reporting, file validation, and pytest fixtures
- **utils**: Add URL validation and improved logging

## v0.5.0 (2025-03-09)

### Feat

- migrate to Poetry and fix Markdown formatting issues

## v0.4.0 (2025-03-01)

### Feat

- Add build and publish instructions

## v0.3.0 (2025-03-01)

### Feat

- Enhance WeCom Bot MCP Server with new features and improvements

## v0.2.0 (2025-02-27)

### Feat

- **wecom_bot_mcp_server**: Add text utilities for handling Chinese characters

## v0.1.0 (2025-01-02)

### Feat

- **src/wecom_bot_mcp_server**: Add WeCom Bot MCP Server package Add a new package for WeCom Bot MCP Server, including a server implementation following the Model Context Protocol (MCP).
