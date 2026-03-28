# Examples

This page contains various usage examples for gdpy.

## User Operations

### Get User Profile

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        user = client.get_user(account_id=71) # RobTop
        print(f"Username: {user.username}")
        print(f"Stars: {user.stars}")
        print(f"Diamonds: {user.diamonds}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            user = await client.get_user(account_id=71)
            print(f"Username: {user.username}")
            print(f"Stars: {user.stars}")
            print(f"Diamonds: {user.diamonds}")

    asyncio.run(main())
    ```

### Search Users

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        users = client.search_users(query="Viprin")
        for user in users:
            print(f"{user.username} (Account ID: {user.account_id})")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            users = await client.search_users(query="Viprin")
            for user in users:
                print(f"{user.username} (Account ID: {user.account_id})")

    asyncio.run(main())
    ```

### Get User's Created Levels

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        user = client.get_user(account_id=71)  # RobTop
        levels = client.get_user_levels(user_id=user.user_id, limit=10)
        for level in levels:
            print(f"{level.name} - {level.downloads:,} downloads")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            user = await client.get_user(account_id=71)
            levels = await client.get_user_levels(user_id=user.user_id, limit=10)
            for level in levels:
                print(f"{level.name} - {level.downloads:,} downloads")

    asyncio.run(main())
    ```

## Level Operations

### Search Levels

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        levels = client.search_levels(query="Bloodbath", limit=10)
        for level in levels:
            print(f"{level.name}")
            print(f"  Downloads: {level.downloads:,}")
            print(f"  Likes: {level.likes:,}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            levels = await client.search_levels(query="Bloodbath", limit=10)
            for level in levels:
                print(f"{level.name}")
                print(f"  Downloads: {level.downloads:,}")
                print(f"  Likes: {level.likes:,}")

    asyncio.run(main())
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            levels = await client.search_levels(query="Bloodbath", limit=10)
            for level in levels:
                print(f"{level.name}")

    asyncio.run(main())
    ```

### Get Level by ID

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        level = client.get_level(level_id=3009486) # ReTraY
        print(f"Name: {level.name}")
        print(f"Objects: {level.objects:,}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            level = await client.get_level(level_id=3009486)
            print(f"Name: {level.name}")
            print(f"Objects: {level.objects:,}")

    asyncio.run(main())
    ```

### Paginated Search

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        for page in range(3):
            levels = client.search_levels(query="", limit=10, page=page)
            print(f"Page {page}: {len(levels)} levels")
            for level in levels:
                print(f"  - {level.name}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            for page in range(3):
                levels = await client.search_levels(query="", limit=10, page=page)
                print(f"Page {page}: {len(levels)} levels")
                for level in levels:
                    print(f"  - {level.name}")

    asyncio.run(main())
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            level = await client.get_level(level_id=3009486)
            print(f"Name: {level.name}")

    asyncio.run(main())
    ```

### Paginated Search

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        for page in range(3):
            levels = client.search_levels(query="", limit=10, page=page)
            print(f"Page {page}: {len(levels)} levels")
            for level in levels:
                print(f"  - {level.name}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            for page in range(3):
                levels = await client.search_levels(query="", limit=10, page=page)
                print(f"Page {page}: {len(levels)} levels")

    asyncio.run(main())
    ```

## Authentication

### Login

=== "Synchronous"

    ```python
    from gdpy import Client
    from gdpy.exceptions import InvalidCredentialsError

    with Client() as client:
        try:
            if client.login("username", "password"):
                print(f"Logged in as {client.username}")
                print(f"Account ID: {client.account_id}")
        except InvalidCredentialsError:
            print("Invalid credentials")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient
    from gdpy.exceptions import InvalidCredentialsError

    async def main():
        async with AsyncClient() as client:
            try:
                if await client.login("username", "password"):
                    print(f"Logged in as {client.username}")
                    print(f"Account ID: {client.account_id}")
            except InvalidCredentialsError:
                print("Invalid credentials")

    asyncio.run(main())
    ```

### Register Account

=== "Synchronous"

    ```python
    from gdpy import Client
    from gdpy.exceptions import UsernameTakenError, EmailTakenError

    with Client() as client:
        try:
            if client.register("newuser", "password123", "user@email.com"):
                print("Account created!")
        except UsernameTakenError:
            print("Username already taken")
        except EmailTakenError:
            print("Email already registered")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient
    from gdpy.exceptions import UsernameTakenError, EmailTakenError

    async def main():
        async with AsyncClient() as client:
            try:
                if await client.register("newuser", "password123", "user@email.com"):
                    print("Account created!")
            except UsernameTakenError:
                print("Username already taken")
            except EmailTakenError:
                print("Email already registered")

    asyncio.run(main())
    ```

## Error Handling

### Comprehensive Error Handling

=== "Synchronous"

    ```python
    from gdpy import Client
    from gdpy.exceptions import (
        GDError,
        NotFoundError,
        InvalidRequestError,
    )

    with Client() as client:
        try:
            user = client.get_user(account_id=999999999)
        except NotFoundError:
            print("User not found")
        except InvalidRequestError:
            print("Rate limited or invalid request")
        except GDError as e:
            print(f"Error: {e}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient
    from gdpy.exceptions import GDError, NotFoundError, InvalidRequestError

    async def main():
        async with AsyncClient() as client:
            try:
                user = await client.get_user(account_id=999999999)
            except NotFoundError:
                print("User not found")
            except InvalidRequestError:
                print("Rate limited or invalid request")
            except GDError as e:
                print(f"Error: {e}")

    asyncio.run(main())
    ```

### Registration Error Handling

=== "Synchronous"

    ```python
    from gdpy import Client
    from gdpy.exceptions import (
        UsernameTakenError,
        EmailTakenError,
        PasswordTooShortError,
        UsernameTooShortError,
    )

    with Client() as client:
        try:
            client.register("user", "pass", "email@test.com")
        except UsernameTakenError:
            print("Username already exists")
        except EmailTakenError:
            print("Email already registered")
        except PasswordTooShortError:
            print("Password must be at least 6 characters")
        except UsernameTooShortError:
            print("Username must be at least 3 characters")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient
    from gdpy.exceptions import (
        UsernameTakenError,
        EmailTakenError,
        PasswordTooShortError,
        UsernameTooShortError,
    )

    async def main():
        async with AsyncClient() as client:
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

    asyncio.run(main())
    ```

## Working with Models

### User Model

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        user = client.get_user(account_id=71)

        # Basic info
        print(f"Username: {user.username}")
        print(f"Account ID: {user.account_id}")

        # Stats
        print(f"Stars: {user.stars}")
        print(f"Diamonds: {user.diamonds}")
        print(f"Moons: {user.moons}")

        # Coins
        print(f"Secret Coins: {user.secret_coins}/3")
        print(f"User Coins: {user.user_coins}")

        # Social links
        if user.youtube:
            print(f"YouTube: {user.youtube}")
        if user.twitter:
            print(f"Twitter: {user.twitter}")

        # Moderator status
        print(f"Mod Level: {user.mod_level.name}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            user = await client.get_user(account_id=71)

            # Basic info
            print(f"Username: {user.username}")
            print(f"Account ID: {user.account_id}")

            # Stats
            print(f"Stars: {user.stars}")
            print(f"Diamonds: {user.diamonds}")
            print(f"Moons: {user.moons}")

            # Coins
            print(f"Secret Coins: {user.secret_coins}/3")
            print(f"User Coins: {user.user_coins}")

            # Social links
            if user.youtube:
                print(f"YouTube: {user.youtube}")
            if user.twitter:
                print(f"Twitter: {user.twitter}")

            # Moderator status
            print(f"Mod Level: {user.mod_level.name}")

    asyncio.run(main())
    ```

### Level Model

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        level = client.get_level(level_id=3009486)

        # Basic info
        print(f"Name: {level.name}")
        print(f"ID: {level.level_id}")

        # Stats
        print(f"Downloads: {level.downloads:,}")
        print(f"Likes: {level.likes:,}")
        print(f"Objects: {level.objects:,}")

        # Difficulty
        if level.is_demon:
            print(f"Demon Difficulty: {level.demon_difficulty.name}")
        print(f"Length: {level.length.name}")

        # Rating
        print(f"Stars: {level.stars}")
        print(f"Epic Rating: {level.epic_rating.name}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            level = await client.get_level(level_id=3009486)

            # Basic info
            print(f"Name: {level.name}")
            print(f"ID: {level.level_id}")

            # Stats
            print(f"Downloads: {level.downloads:,}")
            print(f"Likes: {level.likes:,}")
            print(f"Objects: {level.objects:,}")

            # Difficulty
            if level.is_demon:
                print(f"Demon Difficulty: {level.demon_difficulty.name}")
            print(f"Length: {level.length.name}")

            # Rating
            print(f"Stars: {level.stars}")
            print(f"Epic Rating: {level.epic_rating.name}")

    asyncio.run(main())
    ```

## Songs

### Get Song Info

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        song = client.get_song(song_id=803223)  # Xtrullor - Arcana
        print(f"Song: {song.name}")
        print(f"Artist: {song.author}")
        print(f"Size: {song.size} MB")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            song = await client.get_song(song_id=803223)
            print(f"Song: {song.name}")
            print(f"Artist: {song.author}")

    asyncio.run(main())
    ```

## Comments

### Get Level Comments

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        comments = client.get_level_comments(level_id=3009486, limit=10)
        for comment in comments:
            print(f"{comment.author}: {comment.content}")
            print(f"  Likes: {comment.likes}")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            comments = await client.get_level_comments(level_id=3009486, limit=10)
            for comment in comments:
                print(f"{comment.author}: {comment.content}")

    asyncio.run(main())
    ```

## Leaderboards

### Global Leaderboard

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        leaderboard = client.get_leaderboard(limit=10)
        for i, entry in enumerate(leaderboard, 1):
            print(f"#{i}: {entry.username} - {entry.stars} stars")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            leaderboard = await client.get_leaderboard(limit=10)
            for i, entry in enumerate(leaderboard, 1):
                print(f"#{i}: {entry.username} - {entry.stars} stars")

    asyncio.run(main())
    ```

### Creator Leaderboard

=== "Synchronous"

    ```python
    from gdpy import Client

    with Client() as client:
        creators = client.get_leaderboard(limit=10, type="creators")
        for i, entry in enumerate(creators, 1):
            print(f"#{i}: {entry.username} - {entry.creator_points} CP")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        async with AsyncClient() as client:
            creators = await client.get_leaderboard(limit=10, type="creators")
            for i, entry in enumerate(creators, 1):
                print(f"#{i}: {entry.username} - {entry.creator_points} CP")

    asyncio.run(main())
    ```

## Async Concurrent Requests

```python
import asyncio
from gdpy import AsyncClient

async def fetch_multiple_users():
    async with AsyncClient() as client:
        # Fetch multiple users concurrently
        users = await asyncio.gather(
            client.get_user(account_id=71),
            client.get_user(account_id=16),
            client.get_user(account_id=1),
        )

        for user in users:
            print(f"{user.username}: {user.stars} stars")

asyncio.run(fetch_multiple_users())
```
