from gdpy.client import Client
from gdpy.models import User


class UsersEndpoint:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def get(self, account_id: int) -> User:
        return await self._client.get_user(account_id)

    async def search(self, query: str, limit: int = 10) -> list[User]:
        return await self._client.search_users(query, limit)
