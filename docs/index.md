# gdpy

A modern, type-safe Python library for interacting with the Geometry Dash private API.

## Why gdpy?

Instead of manually crafting HTTP requests and parsing custom response formats, gdpy gives you:

- **Clean Pythonic API** — `client.get_user(account_id=71)` vs constructing URLs and parsing `key:value` strings
- **Full type safety** — IDE autocomplete and catch errors before runtime with Pydantic models
- **Built-in crypto** — GJP2 encoding, XOR ciphers, and checksums handled automatically

Raw requests require understanding GD's custom formats and encryption. gdpy abstracts that away.

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
| Accounts | 3 | 5 | 60% |
| Users | 4 | 4 | 100% |
| Levels | 10 | 11 | 91% |
| Comments | 7 | 7 | 100% |
| Songs | 3 | 6 | 50% |
| Social | 12 | 12 | 100% |
| Messages | 4 | 4 | 100% |
| Rewards | 2 | 3 | 67% |
| Lists | 1 | 3 | 33% |
| Misc | 2 | 2 | 100% |
| **Total** | **48** | **57** | **84%** |

See [API Coverage](api-coverage.md) for detailed endpoint status.

## Installation

```bash
pip install gdpy
```

## Quick Start

=== "Synchronous"

    ```python
    from gdpy import Client
    from gdpy.models import User, Level

    # Use without context manager (remember to close!)
    client = Client()
    user: User = client.get_user(account_id=71)  # RobTop
    print(f"Username: {user.username}")
    print(f"Stars: {user.stars}")
    client.close()

    # Or use as context manager (auto-closes)
    with Client() as client:
        levels: list[Level] = client.search_levels(query="ReTraY", limit=5)
        for level in levels:
            print(f"{level.name} - {level.downloads} downloads")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient
    from gdpy.models import User, Level

    async def main():
        # Use without context manager (remember to close!)
        client = AsyncClient()
        user: User = await client.get_user(account_id=71)
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")
        await client.close()

        # Or use as context manager (auto-closes)
        async with AsyncClient() as client:
            levels: list[Level] = await client.search_levels(query="ReTraY", limit=5)
            for level in levels:
                print(f"{level.name}")

    asyncio.run(main())
    ```

## Troubleshooting

??? "Why am I getting 429 errors?"

    The Geometry Dash API has aggressive rate limiting. If you make requests too quickly, you'll get `-1` responses (handled as `InvalidRequestError`). Add delays between requests:

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            for level_id in level_ids:
                level = await client.get_level(level_id=level_id)
                await asyncio.sleep(2)  # Wait between requests
    ```

??? "How do I handle rate limits?"

    Catch `InvalidRequestError` and retry with exponential backoff:

    ```python
    from gdpy import Client
    from gdpy.exceptions import InvalidRequestError
    import time

    with Client() as client:
        for _ in range(3):  # Retry up to 3 times
            try:
                user = client.get_user(account_id=71)
                break
            except InvalidRequestError:
                time.sleep(2)
    ```

??? "Why does level data look incomplete?"

    Some fields like `level_string` (the actual level data) are only included when fetching a single level via `get_level()`, not in search results. If you need full data:

    ```python
    # Search gives basic info
    levels = client.search_levels(query="ReTraY", limit=5)

    # Fetch full data for a specific level
    full_level = client.get_level(level_id=levels[0].level_id)
    print(full_level.level_string)  # Only available here
    ```

## Requirements

- Python 3.10+
- `httpx` - HTTP client (supports both sync and async)
- `pydantic` - Data validation

## License

MIT

---

**Credits:** This library is based on the [Geometry Dash API documentation](https://boomlings.dev).
