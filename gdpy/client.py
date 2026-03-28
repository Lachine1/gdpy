"""Main client module for interacting with the Geometry Dash API."""

import httpx

from gdpy.constants import Secrets, URLs
from gdpy.crypto import generate_gjp2
from gdpy.exceptions import (
    AccountDisabledError,
    EmailTakenError,
    InvalidCredentialsError,
    InvalidRequestError,
    NotFoundError,
    PasswordTooShortError,
    UsernameTakenError,
    UsernameTooShortError,
)
from gdpy.models import Level, User
from gdpy.utils.parsing import parse_list_response, parse_response


class Client:
    """Async client for interacting with the Geometry Dash API.
    
    This client provides methods to interact with Geometry Dash's private API,
    including user lookups, level searches, and authentication.
    
    Args:
        base_url: Optional custom base URL for the API. Defaults to boomlings.com.
    
    Example:
        ```python
        async with Client() as client:
            user = await client.get_user(account_id=71)
            print(user.username)
        ```
    """

    def __init__(self, base_url: str | None = None) -> None:
        """Initialize the client.
        
        Args:
            base_url: Optional custom base URL for the API.
        """
        self.base_url = base_url or URLs.DEFAULT
        self._client: httpx.AsyncClient | None = None
        self._account_id: int | None = None
        self._player_id: int | None = None
        self._username: str | None = None
        self._password: str | None = None

    async def __aenter__(self) -> "Client":
        """Enter async context manager and initialize HTTP client."""
        self._client = httpx.AsyncClient(
            headers={
                "User-Agent": "",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            timeout=30.0,
        )
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit async context manager and close HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def is_authenticated(self) -> bool:
        """Check if the client is authenticated.
        
        Returns:
            True if logged in, False otherwise.
        """
        return self._account_id is not None

    @property
    def account_id(self) -> int | None:
        """Get the authenticated account ID.
        
        Returns:
            Account ID if authenticated, None otherwise.
        """
        return self._account_id

    @property
    def username(self) -> str | None:
        """Get the authenticated username.
        
        Returns:
            Username if authenticated, None otherwise.
        """
        return self._username

    async def _request(
        self, endpoint: str, data: dict[str, str], secret: str = Secrets.COMMON
    ) -> str:
        """Make a request to the Geometry Dash API.
        
        Args:
            endpoint: API endpoint path.
            data: Request data dictionary.
            secret: API secret to use.
        
        Returns:
            Response text from the API.
        
        Raises:
            RuntimeError: If client is not initialized.
            httpx.HTTPStatusError: If request fails.
        """
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with Client() as client:'")
        data["secret"] = secret
        url = f"{self.base_url}/{endpoint}"
        response = await self._client.post(url, data=data)
        response.raise_for_status()
        return response.text

    def _handle_error(self, response: str) -> None:
        """Handle error responses from the API.
        
        Args:
            response: Error response string.
        
        Raises:
            Appropriate exception based on error code.
        """
        if response.startswith("-"):
            code = int(response)
            if code == -1:
                raise InvalidRequestError("Rate limited or invalid request")
            elif code == -11:
                raise InvalidCredentialsError("Invalid username or password")
            elif code == -12:
                raise AccountDisabledError("Account has been disabled")
            elif code == -2:
                raise UsernameTakenError("Username is already taken")
            elif code == -3:
                raise EmailTakenError("Email is already registered")
            elif code == -8:
                raise PasswordTooShortError("Password must be at least 6 characters")
            elif code == -9:
                raise UsernameTooShortError("Username must be at least 3 characters")
            else:
                raise NotFoundError(f"Request failed with code {code}")

    async def login(self, username: str, password: str) -> bool:
        """Login to a Geometry Dash account.
        
        Args:
            username: Account username.
            password: Account password.
        
        Returns:
            True if login successful, False otherwise.
        
        Raises:
            InvalidCredentialsError: If credentials are incorrect.
            AccountDisabledError: If account is disabled.
            InvalidRequestError: If rate limited.
        
        Example:
            ```python
            async with Client() as client:
                if await client.login("username", "password"):
                    print(f"Logged in as {client.username}")
            ```
        """
        import random

        udid = "S" + str(random.randint(100000, 100000000)) + str(random.randint(100000, 100000000))
        gjp2 = generate_gjp2(password)
        data = {
            "udid": udid,
            "userName": username,
            "gjp2": gjp2,
            "secret": Secrets.ACCOUNT,
        }
        response = await self._request("accounts/loginGJAccount.php", data)
        if response.startswith("-"):
            self._handle_error(response)
            return False
        parts = response.split(",")
        if len(parts) >= 2:
            self._account_id = int(parts[0])
            self._player_id = int(parts[1])
            self._username = username
            self._password = password
            return True
        return False

    async def register(self, username: str, password: str, email: str) -> bool:
        """Register a new Geometry Dash account.
        
        Args:
            username: Desired username (min 3 characters).
            password: Desired password (min 6 characters).
            email: Email address.
        
        Returns:
            True if registration successful, False otherwise.
        
        Raises:
            UsernameTakenError: If username is already taken.
            EmailTakenError: If email is already registered.
            PasswordTooShortError: If password is too short.
            UsernameTooShortError: If username is too short.
        
        Example:
            ```python
            async with Client() as client:
                if await client.register("newuser", "password123", "user@email.com"):
                    print("Account created!")
            ```
        """
        data = {
            "userName": username,
            "password": password,
            "email": email,
        }
        response = await self._request("accounts/registerGJAccount.php", data, Secrets.ACCOUNT)
        if response.startswith("-"):
            self._handle_error(response)
            return False
        return response == "1"

    async def get_user(self, account_id: int) -> User:
        """Get a user by their account ID.
        
        Args:
            account_id: The account ID of the user.
        
        Returns:
            User object with profile information.
        
        Raises:
            NotFoundError: If user is not found.
            InvalidRequestError: If rate limited.
        
        Example:
            ```python
            async with Client() as client:
                user = await client.get_user(account_id=71)
                print(f"Username: {user.username}")
                print(f"Stars: {user.stars}")
            ```
        """
        data = {
            "targetAccountID": str(account_id),
        }
        response = await self._request("getGJUserInfo20.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return User.model_validate(parsed)

    async def search_users(self, query: str, limit: int = 10) -> list[User]:
        """Search for users by name.
        
        Args:
            query: Search query (username or partial match).
            limit: Maximum number of results to return.
        
        Returns:
            List of User objects matching the query.
        
        Example:
            ```python
            async with Client() as client:
                users = await client.search_users(query="RobTop")
                for user in users:
                    print(user.username)
            ```
        """
        data = {
            "str": query,
            "total": str(limit),
            "page": "0",
        }
        response = await self._request("getGJUsers20.php", data)
        if response.startswith("-"):
            return []
        user_data = parse_response(response.split("#")[0])
        return [User.model_validate(user_data)]

    async def get_level(self, level_id: int) -> Level:
        """Get a level by its ID.
        
        Args:
            level_id: The ID of the level.
        
        Returns:
            Level object with level information.
        
        Raises:
            NotFoundError: If level is not found.
            InvalidRequestError: If rate limited.
        
        Example:
            ```python
            async with Client() as client:
                level = await client.get_level(level_id=3009486)  # ReTraY
                print(f"Name: {level.name}")
                print(f"Downloads: {level.downloads}")
            ```
        """
        data = {
            "levelID": str(level_id),
        }
        response = await self._request("downloadGJLevel22.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response.split("#")[0])
        return Level.model_validate(parsed)

    async def search_levels(self, query: str = "", limit: int = 10, page: int = 0) -> list[Level]:
        """Search for levels by name.
        
        Args:
            query: Search query (level name or partial match).
            limit: Maximum number of results per page.
            page: Page number for pagination.
        
        Returns:
            List of Level objects matching the query.
        
        Example:
            ```python
            async with Client() as client:
                levels = await client.search_levels(query="ReTraY", limit=10)
                for level in levels:
                    print(f"{level.name} - {level.downloads} downloads")
            ```
        """
        data = {
            "str": query,
            "total": str(limit),
            "page": str(page),
            "type": "0",
        }
        response = await self._request("getGJLevels21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        levels_data = parse_list_response(parts[0])
        return [Level.model_validate(level) for level in levels_data]
