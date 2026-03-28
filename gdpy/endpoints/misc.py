from typing import Any

from gdpy.client import Client
from gdpy.utils.parsing import parse_list_response, parse_response


class MiscEndpoint:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def get_daily_level(self) -> dict[str, Any]:
        data = {"daily": "1"}
        response = await self._client._request("getGJDailyLevel.php", data)
        if response.startswith("-"):
            return {}
        return parse_response(response)

    async def get_weekly_level(self) -> dict[str, Any]:
        data = {"weekly": "1"}
        response = await self._client._request("getGJDailyLevel.php", data)
        if response.startswith("-"):
            return {}
        return parse_response(response)

    async def get_gauntlets(self) -> list[dict[str, Any]]:
        response = await self._client._request("getGJGauntlets21.php", {})
        if response.startswith("-"):
            return []
        return parse_list_response(response)

    async def get_map_packs(self, limit: int = 10) -> list[dict[str, Any]]:
        data = {
            "total": str(limit),
            "page": "0",
        }
        response = await self._client._request("getGJMapPacks21.php", data)
        if response.startswith("-"):
            return []
        return parse_list_response(response)
