# gdpy

A modern, type-safe Python library for interacting with the Geometry Dash private API.

## Features

- 🔄 **Sync & Async** - Both synchronous (`Client`) and asynchronous (`AsyncClient`) interfaces
- 🚀 **Modern HTTP** - Built with `httpx` for both sync and async operations
- 🎯 **Type-safe** - Full type hints with runtime validation via Pydantic
- 📦 **Well-structured** - Clean, pythonic API design
- 🔐 **Built-in crypto** - XOR cipher, GJP2 encoding, base64 utilities, and checksums
- ⚠️ **Comprehensive errors** - Full exception hierarchy for different error scenarios
- 📖 **Well-documented** - Docstrings and examples for all public APIs

## Installation

```bash
pip install gdpy
```

## Quick Start

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        # Get user info
        user = client.get_user(account_id=71) # RobTop
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")

        # Search levels
        levels = client.search_levels(query="ReTraY", limit=5)
        for level in levels:
            print(f"{level.name} - {level.downloads} downloads")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            # Get user info
            user = await client.get_user(account_id=71)
            print(f"Username: {user.username}")

            # Search levels
            levels = await client.search_levels(query="ReTraY", limit=5)
            for level in levels:
                print(f"{level.name}")

    asyncio.run(main())
    ```

### Asynchronous Usage

```python
import asyncio
from gdpy import AsyncClient

async def main():
    async with AsyncClient() as client:
        # Get user info
        user = await client.get_user(account_id=71)
        print(f"Username: {user.username}")

        # Search levels
        levels = await client.search_levels(query="ReTraY", limit=5)
        for level in levels:
            print(f"{level.name}")

asyncio.run(main())
```

## Requirements

- Python 3.10+
- `httpx` - HTTP client (supports both sync and async)
- `pydantic` - Data validation

## License

MIT

---

**Credits:** This library is based on the [Geometry Dash API documentation](https://github.com/Rifct/gd-docs).
