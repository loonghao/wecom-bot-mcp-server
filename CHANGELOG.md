## v0.11.2 (2026-07-30)

### Fix

- pin mcp>=1.3.0,<2.0.0 and sanitize shell function env vars

## [0.12.0](https://github.com/loonghao/wecom-bot-mcp-server/compare/v0.11.2...v0.12.0) (2026-09-25)


### Features

* Add build and publish instructions ([5bd0c74](https://github.com/loonghao/wecom-bot-mcp-server/commit/5bd0c74e9a57fd83161b4b96e531357f89ef9420))
* add environment variables to control logging behavior ([97c0563](https://github.com/loonghao/wecom-bot-mcp-server/commit/97c05632bb68c4f3b57edfac369925a184365bd2))
* add markdown type selection and E2E testing framework ([5705a47](https://github.com/loonghao/wecom-bot-mcp-server/commit/5705a4705beee85f50d3957cee4b9a06bbcc2ba1))
* Add progress reporting, file validation, and pytest fixtures ([5e378a6](https://github.com/loonghao/wecom-bot-mcp-server/commit/5e378a686d808180736b9c173d9da4749f2fcb76))
* add template card tools and remove upload_wecom_media ([31eb270](https://github.com/loonghao/wecom-bot-mcp-server/commit/31eb27071f7b9175e48147b64a405626fa7c27bb))
* enforce markdown_v2 only for WeCom messages ([c15cb3e](https://github.com/loonghao/wecom-bot-mcp-server/commit/c15cb3e254b7d1f8b3d4952b98d9c0c6e08295b9))
* Enhance WeCom Bot MCP Server with new features and improvements ([7aa6007](https://github.com/loonghao/wecom-bot-mcp-server/commit/7aa60070adfc644966e40373fbb4228e771c5c17))
* migrate to Poetry and fix Markdown formatting issues ([2a2a7ac](https://github.com/loonghao/wecom-bot-mcp-server/commit/2a2a7acdfae4a92ba572e4f6a01c68800df87728))
* **prompts:** enhance MCP prompts for intelligent [@mention](https://github.com/mention) user detection ([2f7ef74](https://github.com/loonghao/wecom-bot-mcp-server/commit/2f7ef74f9e9b36e28f3ae654fd8c94be36b10e13))
* **src/wecom_bot_mcp_server:** Add WeCom Bot MCP Server package ([4a52d62](https://github.com/loonghao/wecom-bot-mcp-server/commit/4a52d62ffdbce71e3b1a62699e2bdab898e23b7f))
* **utils:** Add URL validation and improved logging ([a2b553e](https://github.com/loonghao/wecom-bot-mcp-server/commit/a2b553e1aad8a17a13573b88c2eb33f90f9e0666))
* **wecom_bot_mcp_server:** Add text utilities for handling Chinese characters ([6911443](https://github.com/loonghao/wecom-bot-mcp-server/commit/6911443d2f977363959bcb686f017c2fa36d54ba))


### Bug Fixes

* accept NETWORK_ERROR in integration tests ([d5363d4](https://github.com/loonghao/wecom-bot-mcp-server/commit/d5363d43337db888300ad4688b0ced0881287164))
* add configure-pages step for GitHub Pages deployment ([6bfaf3b](https://github.com/loonghao/wecom-bot-mcp-server/commit/6bfaf3bf64a5eb06b60ab91bad31f75837a32b99))
* add path confinement to prevent arbitrary file exfiltration via send_wecom_file (CWE-22) ([e6761e7](https://github.com/loonghao/wecom-bot-mcp-server/commit/e6761e719da441b6be88138c89d6633c71c04fc3)), closes [#158](https://github.com/loonghao/wecom-bot-mcp-server/issues/158)
* correct test expectations to match actual error codes and fixtures ([6e6901b](https://github.com/loonghao/wecom-bot-mcp-server/commit/6e6901bb0ec09c294215b6dd647adc21c63d2d5a))
* **deps:** update dependency aiohttp to v3.11.14 ([905828d](https://github.com/loonghao/wecom-bot-mcp-server/commit/905828dd5c07e42932ff66bd23d1318790850303))
* **deps:** update dependency aiohttp to v3.11.18 ([f737df0](https://github.com/loonghao/wecom-bot-mcp-server/commit/f737df0752a137377c1b8fbe5df5a5021fca91ae))
* **deps:** update dependency aiohttp to v3.12.0 ([62c1d56](https://github.com/loonghao/wecom-bot-mcp-server/commit/62c1d561b45f2ad5d8211bdebdef646cc0506f80))
* **deps:** update dependency aiohttp to v3.12.12 ([c5140d0](https://github.com/loonghao/wecom-bot-mcp-server/commit/c5140d0d0f65f4ed1b7530d8064fec6b57e3ffdb))
* **deps:** update dependency aiohttp to v3.12.13 ([6404216](https://github.com/loonghao/wecom-bot-mcp-server/commit/64042167a93cf3799755fc93fe239b61c28f6c10))
* **deps:** update dependency aiohttp to v3.12.15 ([aa690ee](https://github.com/loonghao/wecom-bot-mcp-server/commit/aa690ee012c212ace4cd0cf1a1968d9b862e342b))
* **deps:** update dependency aiohttp to v3.12.4 ([0f87c49](https://github.com/loonghao/wecom-bot-mcp-server/commit/0f87c49262e1440497e1e92e0e05555458962f5f))
* **deps:** update dependency mcp to v1.10.0 ([e17e4ce](https://github.com/loonghao/wecom-bot-mcp-server/commit/e17e4ceea0abbc53841b33d8e568e2692434f8c3))
* **deps:** update dependency mcp to v1.12.4 ([18ca4d6](https://github.com/loonghao/wecom-bot-mcp-server/commit/18ca4d6eac348b10bec8cedf7b753f061ceb8c03))
* **deps:** update dependency mcp to v1.13.0 ([ec70a07](https://github.com/loonghao/wecom-bot-mcp-server/commit/ec70a07800fd9c07ec0c3942cbbc16d76adba764))
* **deps:** update dependency mcp to v1.13.1 ([3fee88c](https://github.com/loonghao/wecom-bot-mcp-server/commit/3fee88c5a905bba88200319e05cb584335560a79))
* **deps:** update dependency mcp to v1.7.1 ([3535ea2](https://github.com/loonghao/wecom-bot-mcp-server/commit/3535ea289da50ba8165fdbac062b2f668d590671))
* **deps:** update dependency mcp to v1.8.0 ([1e7c92b](https://github.com/loonghao/wecom-bot-mcp-server/commit/1e7c92bdecae0974f25c91065996bc3b70475547))
* **deps:** update dependency mcp to v1.9.0 ([80fd77f](https://github.com/loonghao/wecom-bot-mcp-server/commit/80fd77f72bf63ed38f437c1510b8519188699008))
* **deps:** update dependency mcp to v1.9.1 ([c9282bf](https://github.com/loonghao/wecom-bot-mcp-server/commit/c9282bf8cc36caca2f52d51b56d9db6d01c69243))
* **deps:** update dependency mcp to v1.9.2 ([49ddbf8](https://github.com/loonghao/wecom-bot-mcp-server/commit/49ddbf884bfe5438fb5f0259ede6926859957ef7))
* **deps:** update dependency mcp to v1.9.3 ([006ef61](https://github.com/loonghao/wecom-bot-mcp-server/commit/006ef6110197e45d0b86c7fce4996f14bf0f8550))
* **deps:** update dependency mcp to v1.9.4 ([c575cfd](https://github.com/loonghao/wecom-bot-mcp-server/commit/c575cfd3b779a5b75e6bc922272b7372cf10090b))
* **deps:** update dependency pillow to v11.2.1 ([ede7060](https://github.com/loonghao/wecom-bot-mcp-server/commit/ede70606ff7912fcf3e9d482ba0976d3ba8b6b88))
* **deps:** update dependency platformdirs to v4.3.7 ([3f944d5](https://github.com/loonghao/wecom-bot-mcp-server/commit/3f944d503d05018e170885a10da8fdc814fd8f95))
* **deps:** update dependency platformdirs to v4.3.8 ([6d2cd11](https://github.com/loonghao/wecom-bot-mcp-server/commit/6d2cd11199684b7e6b781d39a1f6aa5799260562))
* **deps:** update dependency platformdirs to v4.4.0 ([158b24f](https://github.com/loonghao/wecom-bot-mcp-server/commit/158b24f4fea536665ee68cb3a447ccfcb4ae0107))
* **deps:** update dependency pydantic to v2.11.1 ([3974626](https://github.com/loonghao/wecom-bot-mcp-server/commit/3974626052c6546f83ed397360f7400385a51e73))
* **deps:** update dependency pydantic to v2.11.2 ([a65fb47](https://github.com/loonghao/wecom-bot-mcp-server/commit/a65fb4720b3b0dc81b5587cc1df7fd4c7932e832))
* **deps:** update dependency pydantic to v2.11.3 ([3de7fa6](https://github.com/loonghao/wecom-bot-mcp-server/commit/3de7fa6c007660d988c05d8b7d9ae695fab162a0))
* **deps:** update dependency pydantic to v2.11.4 ([d48b395](https://github.com/loonghao/wecom-bot-mcp-server/commit/d48b39546ac96380fa0cc9d39d1672593662025b))
* **deps:** update dependency pydantic to v2.11.5 ([a406ed0](https://github.com/loonghao/wecom-bot-mcp-server/commit/a406ed043866adc4d51cad3c3f4a8dacd48eecc9))
* **deps:** update dependency pydantic to v2.11.7 ([6d09174](https://github.com/loonghao/wecom-bot-mcp-server/commit/6d09174be9d12c5710097609a4b612c19894b5a1))
* **deps:** update dependency tenacity to v9.1.2 ([4688b65](https://github.com/loonghao/wecom-bot-mcp-server/commit/4688b655f16f52756c2acd89187dc09f91ded46a))
* improve testing coverage and remove unnecessary svglib dependency ([fa045cf](https://github.com/loonghao/wecom-bot-mcp-server/commit/fa045cf18a3fc1d2dd3b137efcf85c1d7c227573))
* **mcp:** provide JSON-schema-friendly tool params and export string __version__\n\n- Change send_wecom_file/file_path and send_wecom_image/image_path to str to satisfy gemini-cli PR [#5694](https://github.com/loonghao/wecom-bot-mcp-server/issues/5694) stricter schema typing\n- Export __version__ from package to ensure server logs a string version\n\nSigned-off-by: Hal &lt;hal.long@outlook.com&gt; ([b469e83](https://github.com/loonghao/wecom-bot-mcp-server/commit/b469e83b82fd8632bef0f13eb7ea7e10b59b7900))
* pin mcp&gt;=1.3.0,&lt;2.0.0 and sanitize shell function env vars ([d8c3bdf](https://github.com/loonghao/wecom-bot-mcp-server/commit/d8c3bdff6f3c47bb5b46a4bb89f83c6b2ededa23))
* remove conflicting default and default_factory in Field ([54ad789](https://github.com/loonghao/wecom-bot-mcp-server/commit/54ad78949e3fff85a9f6c0ce47655d99b6aae5f7))
* require notify-bridge&gt;=0.6.1 for proper content parameter handling ([3db6230](https://github.com/loonghao/wecom-bot-mcp-server/commit/3db6230dcefcab4e54c9b861b65fb5d4bb0f67b2))
* resolve Gemini CLI parameter schema validation issues ([352e94f](https://github.com/loonghao/wecom-bot-mcp-server/commit/352e94fb4f8b22f3111aa3261d7e4221118a6d92))
* resolve lint errors (ruff, isort, mypy) ([9e986ce](https://github.com/loonghao/wecom-bot-mcp-server/commit/9e986ce6c2111caea0c6c1c2669641208cbebe7e))
* sync version numbers to resolve auto-bump tag conflicts ([0fd56b1](https://github.com/loonghao/wecom-bot-mcp-server/commit/0fd56b138dc2f7510ce35c98c29bab8ca8b4888a))
* **tests:** directly replace _bot_registry for proper test isolation ([64e6b6e](https://github.com/loonghao/wecom-bot-mcp-server/commit/64e6b6e3173fe8116396791ba76f2a85e23118d6))
* **tests:** improve test isolation for bot_config tests ([f9a7e21](https://github.com/loonghao/wecom-bot-mcp-server/commit/f9a7e21f5f25783cd8488d283ceb2931fcf18716))
* **tests:** use MagicMock for complete isolation from environment ([0d8ff8f](https://github.com/loonghao/wecom-bot-mcp-server/commit/0d8ff8fc8253b444291cb536211be6cef9d3eb98))
* **tests:** use patch on _bot_registry variable for proper isolation ([9da334f](https://github.com/loonghao/wecom-bot-mcp-server/commit/9da334f91c858ad0ee7708053ca5030a571fe34a))
* **tests:** use patch to mock get_bot_registry for reliable test isolation ([4f1ddbe](https://github.com/loonghao/wecom-bot-mcp-server/commit/4f1ddbe74e5662e7a2266be8d65bef93f12abccd))
* update FastMCP initialization for compatibility with mcp 1.12.3 ([b293e7f](https://github.com/loonghao/wecom-bot-mcp-server/commit/b293e7f752d9c07461027517e96197e68bd701a0))
* update notify-bridge to &gt;=0.6.1 in all dependency files ([55c127e](https://github.com/loonghao/wecom-bot-mcp-server/commit/55c127e7c257032e97864465d3bcf1b41e469f6d))
* update tests to mock get_bot_registry instead of get_webhook_url ([36ba1eb](https://github.com/loonghao/wecom-bot-mcp-server/commit/36ba1ebaddc104d27629b938c3889996e7854797))
* use correct 'content' parameter for notify-bridge wecom API ([ef85323](https://github.com/loonghao/wecom-bot-mcp-server/commit/ef853236cafc3bb0541c6aafb838ba3a684bee89))


### Performance Improvements

* add lru_cache to get_allowed_root and symlink escape test ([02d39c4](https://github.com/loonghao/wecom-bot-mcp-server/commit/02d39c4921dbce20056aced34baf83370068b337))


### Code Refactoring

* remove image hosting feature ([91fe092](https://github.com/loonghao/wecom-bot-mcp-server/commit/91fe0925dc65542ad0b6ceecb8b09558ca606e56))
* **types:** avoid parameter type mutation; use local Path vars for mypy --strict\n\n- file.py: file_path_p: Path\n- image.py: image_path_p: Path\n\nSigned-off-by: Hal &lt;hal.long@outlook.com&gt; ([e81e79d](https://github.com/loonghao/wecom-bot-mcp-server/commit/e81e79dca6c9e6cf1ec011b14e8ad7cca2d71b30))


### Documentation

* add JSON escape tool links for multi-bot config ([da760b6](https://github.com/loonghao/wecom-bot-mcp-server/commit/da760b6e3ef22e856346e0ff5889c08da1d7567a))
* add multi-bot configuration section to homepage ([fb56b74](https://github.com/loonghao/wecom-bot-mcp-server/commit/fb56b74334c591d16a335101120ca3b693b15f82))
* add VitePress documentation with GitHub Actions deployment ([8b449bd](https://github.com/loonghao/wecom-bot-mcp-server/commit/8b449bd5ef1e50e32d43d705da6ae79d3761fed1))
* correct MCP usage description ([f3feb4f](https://github.com/loonghao/wecom-bot-mcp-server/commit/f3feb4f780d2a4b7fb38a7c54c52589d5f855e44))
* update documentation for new features and tools ([84ee217](https://github.com/loonghao/wecom-bot-mcp-server/commit/84ee217c629c99850d41eb504607bcc230b3d85e))
* Update README with detailed information and usage instructions ([5e62969](https://github.com/loonghao/wecom-bot-mcp-server/commit/5e629692907e34cfc301da5ef86d025474a76c83))

## v0.11.1 (2026-06-18)

### Fix

- add path confinement to prevent arbitrary file exfiltration via send_wecom_file (CWE-22)

### Perf

- add lru_cache to get_allowed_root and symlink escape test

## v0.11.0 (2026-01-30)

### Feat

- **prompts**: enhance MCP prompts for intelligent @mention user detection

## v0.10.2 (2025-12-24)

### Fix

- add configure-pages step for GitHub Pages deployment

## v0.10.1 (2025-12-24)

### Fix

- **tests**: use patch on _bot_registry variable for proper isolation
- **tests**: directly replace _bot_registry for proper test isolation
- **tests**: use MagicMock for complete isolation from environment
- **tests**: use patch to mock get_bot_registry for reliable test isolation
- **tests**: improve test isolation for bot_config tests
- update tests to mock get_bot_registry instead of get_webhook_url
- resolve lint errors (ruff, isort, mypy)

## v0.10.0 (2025-12-24)

### Feat

- add environment variables to control logging behavior

## v0.9.0 (2025-12-24)

### Feat

- add markdown type selection and E2E testing framework

## v0.8.3 (2025-11-28)

### Fix

- update notify-bridge to >=0.6.1 in all dependency files

## v0.8.2 (2025-11-28)

### Fix

- require notify-bridge>=0.6.1 for proper content parameter handling

## v0.8.1 (2025-11-28)

### Fix

- use correct 'content' parameter for notify-bridge wecom API

## v0.8.0 (2025-11-19)

### Feat

- add template card tools and remove upload_wecom_media

### Refactor

- remove image hosting feature

## v0.7.0 (2025-11-17)

### Feat

- enforce markdown_v2 only for WeCom messages

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
