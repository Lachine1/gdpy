# Examples

This page contains advanced usage examples for gdpy.

## Advanced Level Operations

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

Note: GD rejects temporary email addresses. Use a real email.

=== "Synchronous"

    ```python
    from gdpy import Client
    from gdpy.exceptions import (
        UsernameTakenError,
        EmailTakenError,
        InvalidEmailError,
    )

    with Client() as client:
        try:
            if client.register("newuser", "password123", "user@real-email.com"):
                print("Account created!")
        except UsernameTakenError:
            print("Username already taken")
        except EmailTakenError:
            print("Email already registered")
        except InvalidEmailError:
            print("Invalid or blacklisted email")
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient
    from gdpy.exceptions import (
        UsernameTakenError,
        EmailTakenError,
        InvalidEmailError,
    )

    async def main():
        async with AsyncClient() as client:
            try:
                if await client.register("newuser", "password123", "user@real-email.com"):
                    print("Account created!")
            except UsernameTakenError:
                print("Username already taken")
            except EmailTakenError:
                print("Email already registered")
            except InvalidEmailError:
                print("Invalid or blacklisted email")

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
        InvalidEmailError,
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
        except InvalidEmailError:
            print("Invalid or blacklisted email")
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
        InvalidEmailError,
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
            except InvalidEmailError:
                print("Invalid or blacklisted email")

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

## Async Concurrent Requests

Fetch multiple resources concurrently using `asyncio.gather`:

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

## Custom Base URL

Connect to private Geometry Dash servers:

=== "Synchronous"

    ```python
    from gdpy import Client

    # Use a custom server
    with Client(base_url="https://custom-gd-server.com/database") as client:
        user = client.get_user(account_id=1)
        print(user.username)
    ```

=== "Asynchronous"

    ```python
    import asyncio
    from gdpy import AsyncClient

    async def main():
        # Use a custom server
        async with AsyncClient(base_url="https://custom-gd-server.com/database") as client:
            user = await client.get_user(account_id=1)
            print(user.username)

    asyncio.run(main())
    ```
