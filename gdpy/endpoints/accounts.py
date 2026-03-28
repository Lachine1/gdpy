from gdpy.client import Client


class AccountsEndpoint:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def login(self, username: str, password: str) -> bool:
        result = await self._client.login(username, password)
        return bool(result)

    async def register(self, username: str, password: str, email: str) -> bool:
        result = await self._client.register(username, password, email)
        return bool(result)
