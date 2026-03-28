# Getting Started

This guide will help you get started with gdpy.

## Installation

### Basic Installation

Install gdpy using pip:

```bash
pip install gdpy
```

### Development Installation

To install with development dependencies (for running tests):

```bash
pip install "gdpy[dev]"
```

## Sync vs Async

gdpy provides two client classes:

- **`Client`** - Synchronous client for simple scripts and traditional applications
- **`AsyncClient`** - Asynchronous client for modern async applications and high-performance scenarios

Both clients have the same API, but `AsyncClient` methods are async (use `await`).

## Basic Usage

### Synchronous Client

```python
from gdpy import Client

with Client() as client:
    user = client.get_user(account_id=71)
    print(f"Username: {user.username}")
```

### Asynchronous Client

```python
import asyncio
from gdpy import AsyncClient

async def main():
    async with AsyncClient() as client:
        user = await client.get_user(account_id=71)
        print(f"Username: {user.username}")

asyncio.run(main())
```

## User Operations

### Get User by ID

```python
# Sync
with Client() as client:
    user = client.get_user(account_id=71)
    print(f"Username: {user.username}")
    print(f"Stars: {user.stars}")

# Async
async with AsyncClient() as client:
    user = await client.get_user(account_id=71)
    print(f"Username: {user.username}")
```

### Search Users

```python
# Sync
with Client() as client:
    users = client.search_users(query="RobTop")
    for user in users:
        print(f"{user.username} (ID: {user.account_id})")

# Async
async with AsyncClient() as client:
    users = await client.search_users(query="RobTop")
    for user in users:
        print(user.username)
```

## Level Operations

### Search Levels

```python
# Sync
with Client() as client:
    levels = client.search_levels(query="Bloodbath", limit=10)
    for level in levels:
        print(f"{level.name} - {level.downloads} downloads")

# Async
async with AsyncClient() as client:
    levels = await client.search_levels(query="Bloodbath", limit=10)
    for level in levels:
        print(level.name)
```

### Get Level by ID

```python
# Sync
with Client() as client:
    level = client.get_level(level_id=3009486)  # ReTraY
    print(f"Name: {level.name}")
    print(f"Objects: {level.objects}")

# Async
async with AsyncClient() as client:
    level = await client.get_level(level_id=3009486)
    print(f"Name: {level.name}")
```

### Paginated Search

```python
# Sync
with Client() as client:
    for page in range(3):
        levels = client.search_levels(query="", limit=10, page=page)
        print(f"Page {page}: {len(levels)} levels")

# Async
async with AsyncClient() as client:
    for page in range(3):
        levels = await client.search_levels(query="", limit=10, page=page)
        print(f"Page {page}: {len(levels)} levels")
```

## Authentication

### Login

```python
# Sync
from gdpy import Client
from gdpy.exceptions import InvalidCredentialsError

with Client() as client:
    try:
        if client.login("username", "password"):
            print(f"Logged in as {client.username}")
    except InvalidCredentialsError:
        print("Invalid credentials")

# Async
async with AsyncClient() as client:
    try:
        if await client.login("username", "password"):
            print(f"Logged in as {client.username}")
    except InvalidCredentialsError:
        print("Invalid credentials")
```

### Register

```python
# Sync
from gdpy import Client
from gdpy.exceptions import UsernameTakenError

with Client() as client:
    try:
        if client.register("newuser", "password123", "user@email.com"):
            print("Account created!")
    except UsernameTakenError:
        print("Username taken")

# Async
async with AsyncClient() as client:
    try:
        if await client.register("newuser", "password123", "user@email.com"):
            print("Account created!")
    except UsernameTakenError:
        print("Username taken")
```

## Error Handling

```python
from gdpy import Client
from gdpy.exceptions import GDError, NotFoundError, InvalidRequestError

with Client() as client:
    try:
        user = client.get_user(account_id=999999999)
    except NotFoundError:
        print("User not found!")
    except InvalidRequestError:
        print("Rate limited or invalid request")
    except GDError as e:
        print(f"Error: {e}")
```

## Which Client Should I Use?

### Use `Client` (sync) when:
- Writing simple scripts
- Building traditional synchronous applications
- You don't need concurrent requests
- Working in environments without async support

### Use `AsyncClient` (async) when:
- Building web applications (FastAPI, etc.)
- You need concurrent API calls
- Working with other async libraries
- Building high-performance applications

## Next Steps

- Check out the [API Reference](api/client.md) for detailed documentation
- See [Examples](examples.md) for more usage patterns

---

**Credits:** This library is based on the [Geometry Dash API documentation](https://github.com/Rifct/gd-docs).
