from typing import Any

from gdpy.client import Client
from gdpy.utils.parsing import parse_list_response


class SocialsEndpoint:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def get_friend_requests(self, limit: int = 10) -> list[dict[str, Any]]:
        data = {
            "total": str(limit),
            "page": "0",
        }
        response = await self._client._request("getGJFriendRequests20.php", data)
        if response.startswith("-"):
            return []
        return parse_list_response(response)

    async def get_messages(self, limit: int = 10) -> list[dict[str, Any]]:
        data = {
            "total": str(limit),
            "page": "0",
        }
        response = await self._client._request("getGJMessages20.php", data)
        if response.startswith("-"):
            return []
        return parse_list_response(response)
