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

## Basic Usage

### Creating a Client

The `Client` class is the main entry point for interacting with the Geometry Dash API. It must be used as an async context manager to ensure proper resource cleanup:

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
print(f"Demons: {user.demons}")
print(f"Creator Points: {user.creator_points}")
```

Search for users by name:

```python
users = await client.search_users(query="RobTop")
for user in users:
    print(f"{user.username} (Account ID: {user.account_id})")
```

### Searching Levels

Search for levels by name:

```python
levels = await client.search_levels(query="Bloodbath", limit=10)
for level in levels:
    print(f"{level.name}")
    print(f"  Downloads: {level.downloads}")
    print(f"  Likes: {level.likes}")
    print(f"  Stars: {level.stars}")
```

Get a specific level by ID:

```python
level = await client.get_level(level_id=3009486)  # ReTraY
print(f"Name: {level.name}")
print(f"Objects: {level.objects}")
print(f"Coins: {level.coins}")
```

### Paginated Search

Level search supports pagination:

```python
for page in range(3):
    levels = await client.search_levels(query="", limit=10, page=page)
    print(f"Page {page}: {len(levels)} levels")
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

Register a new account:

```python
async with Client() as client:
    success = await client.register(
        username="newuser",
        password="securepassword123",
        email="user@example.com"
    )
    if success:
        print("Account created successfully!")
```

## Error Handling

gdpy provides specific exceptions for different error cases:

```python
from gdpy import Client
from gdpy.exceptions import (
    GDError,
    NotFoundError,
    InvalidRequestError,
    InvalidCredentialsError,
)

async with Client() as client:
    try:
        user = await client.get_user(account_id=999999999)
    except NotFoundError:
        print("User not found!")
    except InvalidRequestError:
        print("Rate limited or invalid request")
    except GDError as e:
        print(f"Unexpected error: {e}")
```

### Exception Hierarchy

- `GDError` - Base exception for all gdpy errors
  - `RequestError` - Base for request-related errors
    - `AuthError` - Base for authentication errors
      - `InvalidCredentialsError` - Wrong username/password
      - `AccountDisabledError` - Account is banned/disabled
    - `InvalidRequestError` - Rate limited or generic error
    - `NotFoundError` - Resource not found
  - `ValidationError` - Invalid input data
  - `RegistrationError` - Registration failed
    - `UsernameTakenError` - Username already exists
    - `EmailTakenError` - Email already registered
    - `PasswordTooShortError` - Password too short
    - `UsernameTooShortError` - Username too short

## Working with Models

### User Model

The `User` model contains all user profile information:

```python
user = await client.get_user(account_id=71)

# Basic info
print(f"Username: {user.username}")
print(f"User ID: {user.user_id}")
print(f"Account ID: {user.account_id}")

# Stats
print(f"Stars: {user.stars}")
print(f"Diamonds: {user.diamonds}")
print(f"Moons: {user.moons}")
print(f"Secret Coins: {user.secret_coins}")
print(f"User Coins: {user.user_coins}")
print(f"Demons: {user.demons}")
print(f"Creator Points: {user.creator_points}")

# Icons
print(f"Icon ID: {user.icon_id}")
print(f"Color 1: {user.color1}")
print(f"Color 2: {user.color2}")
print(f"Has Glow: {user.has_glow}")

# Social links (if set)
if user.youtube:
    print(f"YouTube: {user.youtube}")
if user.twitter:
    print(f"Twitter: {user.twitter}")

# Moderation status
print(f"Mod Level: {user.mod_level}")  # NONE, MODERATOR, or ELDER_MOD
```

### Level Model

The `Level` model contains level information:

```python
level = await client.get_level(level_id=3009486)

# Basic info
print(f"Name: {level.name}")
print(f"ID: {level.level_id}")
print(f"Description: {level.description}")

# Stats
print(f"Downloads: {level.downloads}")
print(f"Likes: {level.likes}")
print(f"Objects: {level.objects}")

# Rating
print(f"Stars: {level.stars}")
print(f"Featured: {level.featured}")
print(f"Epic Rating: {level.epic_rating}")  # NONE, EPIC, LEGENDARY, MYTHIC

# Difficulty
print(f"Is Demon: {level.is_demon}")
print(f"Demon Difficulty: {level.demon_difficulty}")  # EASY, MEDIUM, HARD, INSANE, EXTREME
print(f"Length: {level.length}")  # TINY, SHORT, MEDIUM, LONG, XL

# Audio
if level.song_id:
    print(f"Custom Song ID: {level.song_id}")
if level.official_song_id:
    print(f"Official Song ID: {level.official_song_id}")

# Coins
print(f"Coins: {level.coins}")
print(f"Verified Coins: {level.verified_coins}")
```

## Next Steps

- Check out the [API Reference](api/client.md) for detailed documentation
- See [Examples](examples.md) for more usage patterns
