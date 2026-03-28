# Getting Started

## Installation

Install gdpy using pip:

```bash
pip install gdpy
```

Or with development dependencies:

```bash
pip install "gdpy[dev]"
```

## Basic Usage

### Creating a Client

The `Client` class is the main entry point for interacting with the Geometry Dash API. Always use it as an async context manager:

```python
from gdpy import Client

async with Client() as client:
    # Your code here
    pass
```

### Fetching Users

Get user information by account ID:

```python
user = await client.get_user(account_id=71)
print(f"Username: {user.username}")
print(f"Stars: {user.stars}")
print(f"Diamonds: {user.diamonds}")
```

Search for users by name:

```python
users = await client.search_users(query="RobTop")
for user in users:
    print(f"{user.username} (ID: {user.account_id})")
```

### Searching Levels

Search for levels by name:

```python
levels = await client.search_levels(query="ReTraY", limit=10)
for level in levels:
    print(f"{level.name} by {level.author_id}")
    print(f"  Downloads: {level.downloads}, Likes: {level.likes}")
```

Get a specific level by ID:

```python
level = await client.get_level(level_id=3009486)
print(f"Name: {level.name}")
print(f"Difficulty: {level.stars} stars")
```

### Authentication

Login to an account for authenticated operations:

```python
async with Client() as client:
    success = await client.login("username", "password")
    if success:
        print(f"Logged in as {client.username}")
        print(f"Account ID: {client.account_id}")
```

## Error Handling

gdpy provides specific exceptions for different error cases:

```python
from gdpy import Client
from gdpy.exceptions import NotFoundError, InvalidRequestError

async with Client() as client:
    try:
        user = await client.get_user(account_id=999999999)
    except NotFoundError:
        print("User not found!")
    except InvalidRequestError as e:
        print(f"Request failed: {e}")
```

## Next Steps

- Check out the [API Reference](api/client.md) for detailed documentation
- See [Examples](examples.md) for more usage patterns
