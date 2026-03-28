from typing import Any

from gdpy.client import Client
from gdpy.utils.parsing import parse_list_response


class CommentsEndpoint:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def get_level_comments(self, level_id: int, limit: int = 10) -> list[dict[str, Any]]:
        data = {
            "levelID": str(level_id),
            "total": str(limit),
            "page": "0",
        }
        response = await self._client._request("getGJComments21.php", data)
        if response.startswith("-"):
            return []
        return parse_list_response(response)

    async def get_account_comments(self, account_id: int, limit: int = 10) -> list[dict[str, Any]]:
        data = {
            "accountID": str(account_id),
            "total": str(limit),
            "page": "0",
        }
        response = await self._client._request("getGJAccountComments20.php", data)
        if response.startswith("-"):
            return []
        return parse_list_response(response)
