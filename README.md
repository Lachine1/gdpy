# gdpy

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Lachine1/gdpy/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docs](https://img.shields.io/badge/docs-github_pages-blue.svg)](https://lachine1.github.io/gdpy/)

A modern, type-safe Python library for interacting with the Geometry Dash private API.

**[Documentation](https://lachine1.github.io/gdpy/)** | **[API Coverage](https://lachine1.github.io/gdpy/api-coverage/)**

## Features

- **Sync & Async** - Both synchronous (`Client`) and asynchronous (`AsyncClient`) interfaces
- **Modern HTTP** - Built with `httpx` for both sync and async operations
- **Type-safe** - Full type hints with runtime validation via Pydantic
- **Custom servers** - Connect to private GD servers via `base_url` parameter
- **Built-in crypto** - XOR cipher, GJP2 encoding, base64 utilities, and checksums
- **Comprehensive errors** - Full exception hierarchy for different error scenarios

## Installation

```bash
pip install gdpy
```

Or using [uv](https://docs.astral.sh/uv/):

```bash
uv pip install gdpy
```

## Quick Start

### Synchronous

```python
from gdpy import Client

with Client() as client:
    # Get user info
    user = client.get_user(account_id=71)  # RobTop
    print(f"Username: {user.username}")
    print(f"Stars: {user.stars}")

    # Search levels
    levels = client.search_levels(query="ReTraY", limit=5)
    for level in levels:
        print(f"{level.name} - {level.downloads} downloads")
```

### Asynchronous

```python
import asyncio
from gdpy import AsyncClient

async def main():
    async with AsyncClient() as client:
        # Get user info
        user = await client.get_user(account_id=71)  # RobTop
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")

        # Search levels
        levels = await client.search_levels(query="ReTraY", limit=5)
        for level in levels:
            print(f"{level.name} - {level.downloads} downloads")

asyncio.run(main())
```

### Custom Server

```python
from gdpy import Client

# Connect to a private GD server
with Client(base_url="https://your-server.com/database") as client:
    user = client.get_user(account_id=1)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT
