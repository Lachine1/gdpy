# Examples

## User Operations

### Get User Profile

```python
import asyncio
from gdpy import Client

async def get_user_profile():
    async with Client() as client:
        user = await client.get_user(account_id=71)  # RobTop
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")
        print(f"Diamonds: {user.diamonds}")
        print(f"Secret Coins: {user.secret_coins}")
        print(f"User Coins: {user.user_coins}")
        print(f"Demons: {user.demons}")
        print(f"Creator Points: {user.creator_points}")

asyncio.run(get_user_profile())
```

### Search Users

```python
import asyncio
from gdpy import Client

async def search_users():
    async with Client() as client:
        users = await client.search_users(query="Viprin")
        for user in users:
            print(f"{user.username} (Account ID: {user.account_id})")

asyncio.run(search_users())
```

## Level Operations

### Search Levels

```python
import asyncio
from gdpy import Client

async def search_levels():
    async with Client() as client:
        levels = await client.search_levels(query="Bloodbath", limit=10)
        for level in levels:
            print(f"{level.name}")
            print(f"  ID: {level.level_id}")
            print(f"  Downloads: {level.downloads}")
            print(f"  Likes: {level.likes}")
            print(f"  Stars: {level.stars}")

asyncio.run(search_levels())
```

### Get Level Details

```python
import asyncio
from gdpy import Client

async def get_level():
    async with Client() as client:
        # ReTraY by TeamN2
        level = await client.get_level(level_id=3009486)
        print(f"Name: {level.name}")
        print(f"Version: {level.version}")
        print(f"Downloads: {level.downloads}")
        print(f"Objects: {level.objects}")
        print(f"Coins: {level.coins}")

asyncio.run(get_level())
```

### Paginated Level Search

```python
import asyncio
from gdpy import Client

async def paginated_search():
    async with Client() as client:
        for page in range(3):
            levels = await client.search_levels(query="", limit=10, page=page)
            print(f"Page {page}: {len(levels)} levels")
            for level in levels:
                print(f"  - {level.name}")

asyncio.run(paginated_search())
```

## Authentication

### Login and Check Status

```python
import asyncio
from gdpy import Client
from gdpy.exceptions import InvalidCredentialsError, InvalidRequestError

async def login_example():
    async with Client() as client:
        try:
            success = await client.login("username", "password")
            if success:
                print(f"Logged in as: {client.username}")
                print(f"Account ID: {client.account_id}")
                print(f"Player ID: {client._player_id}")
        except InvalidCredentialsError:
            print("Invalid username or password")
        except InvalidRequestError as e:
            print(f"Request failed: {e}")

asyncio.run(login_example())
```

### Register New Account

```python
import asyncio
from gdpy import Client
from gdpy.exceptions import UsernameTakenError, EmailTakenError

async def register_example():
    async with Client() as client:
        try:
            success = await client.register(
                username="newuser",
                password="securepassword123",
                email="user@example.com"
            )
            if success:
                print("Account created successfully!")
        except UsernameTakenError:
            print("Username is already taken")
        except EmailTakenError:
            print("Email is already registered")

asyncio.run(register_example())
```

## Error Handling

### Comprehensive Error Handling

```python
import asyncio
from gdpy import Client, User
from gdpy.exceptions import (
    GDError,
    NotFoundError,
    InvalidRequestError,
    RateLimitError,
)

async def safe_get_user(account_id: int):
    async with Client() as client:
        try:
            user = await client.get_user(account_id=account_id)
            return user
        except NotFoundError:
            print(f"User {account_id} not found")
        except InvalidRequestError:
            print("Invalid request - check parameters")
        except GDError as e:
            print(f"Unexpected error: {e}")
        return None

asyncio.run(safe_get_user(71))
```

## Working with Models

### Access User Model Fields

```python
import asyncio
from gdpy import Client

async def user_model_example():
    async with Client() as client:
        user = await client.get_user(account_id=71)
        
        # Basic info
        print(f"Username: {user.username}")
        print(f"User ID: {user.user_id}")
        print(f"Account ID: {user.account_id}")
        
        # Stats
        print(f"Stars: {user.stars}")
        print(f"Diamonds: {user.diamonds}")
        print(f"Moons: {user.moons}")
        
        # Icons
        print(f"Icon ID: {user.icon_id}")
        print(f"Color 1: {user.color1}")
        print(f"Color 2: {user.color2}")
        print(f"Has Glow: {user.has_glow}")
        
        # Social links
        if user.youtube:
            print(f"YouTube: {user.youtube}")
        if user.twitter:
            print(f"Twitter: {user.twitter}")

asyncio.run(user_model_example())
```

### Access Level Model Fields

```python
import asyncio
from gdpy import Client

async def level_model_example():
    async with Client() as client:
        level = await client.get_level(level_id=3009486)
        
        # Basic info
        print(f"Name: {level.name}")
        print(f"ID: {level.level_id}")
        print(f"Version: {level.version}")
        
        # Stats
        print(f"Downloads: {level.downloads}")
        print(f"Likes: {level.likes}")
        print(f"Objects: {level.objects}")
        
        # Rating
        print(f"Stars: {level.stars}")
        print(f"Featured: {level.featured}")
        print(f"Epic Rating: {level.epic_rating}")
        
        # Audio
        if level.song_id:
            print(f"Custom Song ID: {level.song_id}")
        if level.official_song_id:
            print(f"Official Song ID: {level.official_song_id}")

asyncio.run(level_model_example())
```
