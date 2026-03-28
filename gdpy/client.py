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
    def __init__(self, base_url: str | None = None):
        self.base_url = base_url or URLs.DEFAULT
        self._client: httpx.AsyncClient | None = None
        self._account_id: int | None = None
        self._player_id: int | None = None
        self._username: str | None = None
        self._password: str | None = None

    async def __aenter__(self) -> "Client":
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
        if self._client:
            await self._client.aclose()
            self._client = None

    @property
    def is_authenticated(self) -> bool:
        return self._account_id is not None

    @property
    def account_id(self) -> int | None:
        return self._account_id

    @property
    def username(self) -> str | None:
        return self._username

    async def _request(
        self, endpoint: str, data: dict[str, str], secret: str = Secrets.COMMON
    ) -> str:
        if not self._client:
            raise RuntimeError("Client not initialized. Use 'async with Client() as client:'")
        data["secret"] = secret
        url = f"{self.base_url}/{endpoint}"
        response = await self._client.post(url, data=data)
        response.raise_for_status()
        return response.text

    def _handle_error(self, response: str) -> None:
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
        data = {
            "targetAccountID": str(account_id),
        }
        response = await self._request("getGJUserInfo20.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return User.model_validate(parsed)

    async def search_users(self, query: str, limit: int = 10) -> list[User]:
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
        data = {
            "levelID": str(level_id),
        }
        response = await self._request("downloadGJLevel22.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response.split("#")[0])
        return Level.model_validate(parsed)

    async def search_levels(self, query: str = "", limit: int = 10, page: int = 0) -> list[Level]:
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
