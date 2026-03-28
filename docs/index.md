# gdpy

A modern, type-safe Python library for interacting with the Geometry Dash private API.

## Features

- 🚀 **Async-first** - Built with `asyncio` and `httpx` for modern async Python
- 🎯 **Type-safe** - Full type hints with runtime validation via Pydantic
- 📦 **Well-structured** - Clean, pythonic API design with proper separation of concerns
- 🔐 **Built-in crypto** - XOR cipher, GJP2 encoding, base64 utilities, and checksums
- ⚠️ **Comprehensive errors** - Full exception hierarchy for different error scenarios
- 📖 **Well-documented** - Docstrings and examples for all public APIs

## Installation

```bash
pip install gdpy
```

## Quick Start

```python
import asyncio
from gdpy import Client

async def main():
    async with Client() as client:
        # Get user info
        user = await client.get_user(account_id=71)  # RobTop
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")
        print(f"Diamonds: {user.diamonds}")

        # Search levels
        levels = await client.search_levels(query="ReTraY", limit=5)
        for level in levels:
            print(f"{level.name} - {level.downloads} downloads")

asyncio.run(main())
```

## Requirements

- Python 3.10+
- `httpx` - HTTP client
- `pydantic` - Data validation

## License

MIT
