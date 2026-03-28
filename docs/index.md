# gdpy

A modern, type-safe Python library for interacting with the Geometry Dash private API.

## Features

- :arrows_counterclockwise: **Sync & Async** - Both synchronous (`Client`) and asynchronous (`AsyncClient`) interfaces
- :rocket: **Modern HTTP** - Built with `httpx` for both sync and async operations
- :dart: **Type-safe** - Full type hints with runtime validation via Pydantic
- :package: **Well-structured** - Clean, pythonic API design
- :lock: **Built-in crypto** - XOR cipher, GJP2 encoding, base64 utilities, and checksums
- :warning: **Comprehensive errors** - Full exception hierarchy for different error scenarios
- :book: **Well-documented** - Docstrings and examples for all public APIs

## API Coverage

| Category | Implemented | Total | Coverage |
| :--- | :---: | :---: | :---: |
| Authentication | 2 | 2 | 100% |
| Users | 4 | 4 | 100% |
| Levels | 7 | 13 | 54% |
| Comments | 3 | 7 | 43% |
| Songs | 2 | 3 | 67% |
| Social | 0 | 8 | 0% |
| Messages | 0 | 4 | 0% |
| **Total** | **18** | **43** | **42%** |

See [API Coverage](api-coverage.md) for detailed endpoint status.

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

## Requirements

- Python 3.10+
- `httpx` - HTTP client (supports both sync and async)
- `pydantic` - Data validation

## License

MIT

---

**Credits:** This library is based on the [Geometry Dash API documentation](https://boomlings.dev).
