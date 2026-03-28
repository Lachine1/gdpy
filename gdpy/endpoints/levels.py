from gdpy.client import Client
from gdpy.models import Level


class LevelsEndpoint:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def get(self, level_id: int) -> Level:
        return await self._client.get_level(level_id)

    async def search(self, query: str = "", limit: int = 10, page: int = 0) -> list[Level]:
        return await self._client.search_levels(query, limit, page)
