# Examples

This page contains various usage examples for gdpy.

## User Operations

### Get User Profile

Retrieve detailed information about a user by their account ID:

```python
import asyncio
from gdpy import Client

async def get_user_profile():
    async with Client() as client:
        # Get RobTop's profile (account ID 71)
        user = await client.get_user(account_id=71)
        
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")
        print(f"Diamonds: {user.diamonds}")
        print(f"Secret Coins: {user.secret_coins}")
        print(f"User Coins: {user.user_coins}")
        print(f"Demons: {user.demons}")
        print(f"Creator Points: {user.creator_points}")
        
        # Check moderator status
        if user.mod_level.value > 0:
            print(f"Moderator: {user.mod_level.name}")

asyncio.run(get_user_profile())
```

### Search for Users

Search for users by name:

```python
import asyncio
from gdpy import Client

async def search_users():
    async with Client() as client:
        users = await client.search_users(query="Viprin")
        
        for user in users:
            print(f"{user.username} (Account ID: {user.account_id})")
            print(f"  Stars: {user.stars}, Diamonds: {user.diamonds}")
            print(f"  Global Rank: {user.global_rank or 'Not ranked'}")

asyncio.run(search_users())
```

## Level Operations

### Search for Levels

Search levels by name with pagination:

```python
import asyncio
from gdpy import Client

async def search_levels():
    async with Client() as client:
        # Search for levels containing "Bloodbath"
        levels = await client.search_levels(query="Bloodbath", limit=10)
        
        for level in levels:
            print(f"{level.name}")
            print(f"  ID: {level.level_id}")
            print(f"  Downloads: {level.downloads:,}")
            print(f"  Likes: {level.likes:,}")
            print(f"  Stars: {level.stars}")

asyncio.run(search_levels())
```

### Get Level Details

Get detailed information about a specific level:

```python
import asyncio
from gdpy import Client

async def get_level():
    async with Client() as client:
        # Get ReTraY by TeamN2
        level = await client.get_level(level_id=3009486)
        
        print(f"Name: {level.name}")
        print(f"Version: {level.version}")
        print(f"Downloads: {level.downloads:,}")
        print(f"Objects: {level.objects:,}")
        
        # Check difficulty
        if level.is_demon:
            print(f"Demon Difficulty: {level.demon_difficulty.name}")
        else:
            print(f"Difficulty: {level.stars} stars")
        
        # Check rating
        if level.epic_rating.value > 0:
            print(f"Rating: {level.epic_rating.name}")

asyncio.run(get_level())
```

### Paginated Level Search

Iterate through multiple pages of results:

```python
import asyncio
from gdpy import Client

async def paginated_search():
    async with Client() as client:
        # Search through 5 pages
        for page in range(5):
            levels = await client.search_levels(
                query="",
                limit=10,
                page=page
            )
            
            print(f"\nPage {page}: {len(levels)} levels")
            for level in levels:
                print(f"  - {level.name} (ID: {level.level_id})")

asyncio.run(paginated_search())
```

## Authentication

### Login to Account

Authenticate with username and password:

```python
import asyncio
from gdpy import Client
from gdpy.exceptions import InvalidCredentialsError, InvalidRequestError

async def login_example():
    async with Client() as client:
        try:
            success = await client.login("your_username", "your_password")
            
            if success:
                print(f"Logged in as: {client.username}")
                print(f"Account ID: {client.account_id}")
                print(f"Player ID: {client._player_id}")
            else:
                print("Login failed")
                
        except InvalidCredentialsError:
            print("Invalid username or password")
        except InvalidRequestError as e:
            print(f"Request error: {e}")

asyncio.run(login_example())
```

### Register New Account

Create a new Geometry Dash account:

```python
import asyncio
from gdpy import Client
from gdpy.exceptions import UsernameTakenError, EmailTakenError

async def register_example():
    async with Client() as client:
        try:
            success = await client.register(
                username="new_username",
                password="secure_password123",
                email="your@email.com"
            )
            
            if success:
                print("Account created successfully!")
                print("You can now login with your credentials")
                
        except UsernameTakenError:
            print("Username is already taken")
        except EmailTakenError:
            print("Email is already registered")

asyncio.run(register_example())
```

### Check Authentication Status

Verify if the client is authenticated:

```python
import asyncio
from gdpy import Client

async def check_auth():
    async with Client() as client:
        print(f"Is authenticated: {client.is_authenticated}")
        
        # After login
        if await client.login("username", "password"):
            print(f"Is authenticated: {client.is_authenticated}")
            print(f"Username: {client.username}")
            print(f"Account ID: {client.account_id}")

asyncio.run(check_auth())
```

## Error Handling

### Basic Error Handling

Catch specific errors:

```python
import asyncio
from gdpy import Client
from gdpy.exceptions import NotFoundError, InvalidRequestError

async def safe_get_user(account_id: int):
    async with Client() as client:
        try:
            user = await client.get_user(account_id=account_id)
            return user
        except NotFoundError:
            print(f"User {account_id} not found")
        except InvalidRequestError:
            print("Rate limited or invalid request")
        return None

asyncio.run(safe_get_user(71))
```

### Comprehensive Error Handling

Handle all possible errors:

```python
import asyncio
from gdpy import Client
from gdpy.exceptions import (
    GDError,
    NotFoundError,
    InvalidRequestError,
    InvalidCredentialsError,
    AccountDisabledError,
)

async def comprehensive_error_handling():
    async with Client() as client:
        try:
            # Try to login
            await client.login("username", "password")
            
            # Try to get a user
            user = await client.get_user(account_id=12345)
            print(f"Found user: {user.username}")
            
        except InvalidCredentialsError:
            print("Wrong username or password")
        except AccountDisabledError:
            print("Account has been disabled")
        except NotFoundError:
            print("User not found")
        except InvalidRequestError:
            print("Rate limited or invalid request")
        except GDError as e:
            print(f"Unexpected gdpy error: {e}")

asyncio.run(comprehensive_error_handling())
```

### Registration Error Handling

Handle registration-specific errors:

```python
import asyncio
from gdpy import Client
from gdpy.exceptions import (
    UsernameTakenError,
    EmailTakenError,
    PasswordTooShortError,
    UsernameTooShortError,
)

async def handle_registration_errors():
    async with Client() as client:
        try:
            await client.register("user", "pass", "email@test.com")
        except UsernameTakenError:
            print("Username already exists")
        except EmailTakenError:
            print("Email already registered")
        except PasswordTooShortError:
            print("Password must be at least 6 characters")
        except UsernameTooShortError:
            print("Username must be at least 3 characters")

asyncio.run(handle_registration_errors())
```

## Working with Models

### User Model Fields

Access all user profile fields:

```python
import asyncio
from gdpy import Client

async def user_model_fields():
    async with Client() as client:
        user = await client.get_user(account_id=71)
        
        # Basic info
        print(f"Username: {user.username}")
        print(f"User ID: {user.user_id}")
        print(f"Account ID: {user.account_id}")
        
        # Progress stats
        print(f"Stars: {user.stars}")
        print(f"Diamonds: {user.diamonds}")
        print(f"Moons: {user.moons}")
        
        # Coins
        print(f"Secret Coins: {user.secret_coins}/3")
        print(f"User Coins: {user.user_coins}")
        
        # Completion stats
        print(f"Demons Beaten: {user.demons}")
        print(f"Creator Points: {user.creator_points}")
        
        # Icon customization
        print(f"Icon ID: {user.icon_id}")
        print(f"Primary Color: {user.color1}")
        print(f"Secondary Color: {user.color2}")
        if user.color3:
            print(f"Glow Color: {user.color3}")
        print(f"Has Glow: {user.has_glow}")
        
        # Social links
        if user.youtube:
            print(f"YouTube: {user.youtube}")
        if user.twitter:
            print(f"Twitter: {user.twitter}")
        if user.twitch:
            print(f"Twitch: {user.twitch}")
        if user.discord:
            print(f"Discord: {user.discord}")
        
        # Moderation
        print(f"Mod Level: {user.mod_level.name}")
        
        # Privacy settings
        print(f"Message State: {user.message_state.name}")

asyncio.run(user_model_fields())
```

### Level Model Fields

Access all level information:

```python
import asyncio
from gdpy import Client

async def level_model_fields():
    async with Client() as client:
        level = await client.get_level(level_id=3009486)
        
        # Basic info
        print(f"Name: {level.name}")
        print(f"ID: {level.level_id}")
        print(f"Description: {level.description}")
        print(f"Version: {level.version}")
        
        # Stats
        print(f"Downloads: {level.downloads:,}")
        print(f"Likes: {level.likes:,}")
        print(f"Objects: {level.objects:,}")
        
        # Rating
        print(f"Stars: {level.stars}")
        print(f"Featured: {level.featured}")
        print(f"Epic Rating: {level.epic_rating.name}")
        
        # Difficulty
        if level.is_demon:
            print(f"Demon Difficulty: {level.demon_difficulty.name}")
        elif level.is_auto:
            print("Auto Level")
        else:
            print(f"Difficulty: {level.stars} stars")
        
        # Length
        print(f"Length: {level.length.name}")
        
        # Audio
        if level.song_id:
            print(f"Custom Song ID: {level.song_id}")
        elif level.official_song_id:
            print(f"Official Song ID: {level.official_song_id}")
        
        # Coins
        print(f"User Coins: {level.coins}")
        print(f"Verified Coins: {level.verified_coins}")
        
        # Other
        print(f"Two Player: {level.two_player}")

asyncio.run(level_model_fields())
```
