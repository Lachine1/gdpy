# Getting Started

This guide will help you get started with gdpy.

## Installation

Install gdpy using pip:

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
    user = client.get_user(account_id=71)  # RobTop
    print(f"Username: {user.username}")
    print(f"Stars: {user.stars}")
```

### Asynchronous

```python
import asyncio
from gdpy import AsyncClient

async def main():
    async with AsyncClient() as client:
        user = await client.get_user(account_id=71)
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")

asyncio.run(main())
```

## Basic Operations

### Get User

```python
from gdpy import Client

with Client() as client:
    user = client.get_user(account_id=71)
    print(f"Username: {user.username}")
    print(f"Stars: {user.stars}")
    print(f"Diamonds: {user.diamonds}")
```

### Search Levels

```python
from gdpy import Client

with Client() as client:
    levels = client.search_levels(query="Bloodbath", limit=10)
    for level in levels:
        print(f"{level.name} - {level.downloads} downloads")
```

### Get Level by ID

```python
from gdpy import Client

with Client() as client:
    level = client.get_level(level_id=3009486)  # ReTraY
    print(f"Name: {level.name}")
    print(f"Objects: {level.objects:,}")
```

### Get Leaderboard

```python
from gdpy import Client

with Client() as client:
    leaderboard = client.get_leaderboard(limit=10)
    for i, entry in enumerate(leaderboard, 1):
        print(f"#{i}: {entry.username} - {entry.stars} stars")
```

## Sync vs Async

gdpy provides two client classes:

- **`Client`** - Synchronous client for simple scripts and traditional applications
- **`AsyncClient`** - Asynchronous client for modern async applications and concurrent requests

Both clients have the same API, but `AsyncClient` methods are async (use `await`).

### Use `Client` (sync) when:

- Writing simple scripts
- Building traditional synchronous applications
- Working in environments without async support

### Use `AsyncClient` (async) when:

- Building web applications (FastAPI, etc.)
- You need concurrent API calls
- Working with other async libraries

## Error Handling

```python
from gdpy import Client
from gdpy.exceptions import GDError, NotFoundError

with Client() as client:
    try:
        user = client.get_user(account_id=999999999)
    except NotFoundError:
        print("User not found!")
    except GDError as e:
        print(f"Error: {e}")
```

## Custom Server

Connect to private Geometry Dash servers:

```python
from gdpy import Client

with Client(base_url="https://your-server.com/database") as client:
    user = client.get_user(account_id=1)
```

## Next Steps

- [Examples](examples.md) - Advanced usage patterns
- [API Reference](api/client.md) - Detailed method documentation
- [API Coverage](api-coverage.md) - Implemented endpoints
