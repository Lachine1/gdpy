# gdpy

A modern Python client for the Geometry Dash API.

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
        user = await client.get_user(account_id=173831)
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")

        # Search levels
        levels = await client.search_levels(query="ReTraY", limit=10)
        for level in levels:
            print(f"{level.name} by {level.author_id}")

asyncio.run(main())
```

## Features

- Async-first design using httpx
- Type-safe with full type hints
- Pydantic models for validation
- Comprehensive error handling
- Support for users, levels, comments, and more

## License

MIT
