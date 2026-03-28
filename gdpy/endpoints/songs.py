from gdpy.client import Client
from gdpy.exceptions import NotFoundError
from gdpy.models import Song
from gdpy.utils.parsing import parse_response


class SongsEndpoint:
    def __init__(self, client: Client) -> None:
        self._client = client

    async def get(self, song_id: int) -> Song:
        data = {
            "songID": str(song_id),
        }
        response = await self._client._request("getGJSongInfo.php", data)
        if response.startswith("-"):
            raise NotFoundError(f"Song {song_id} not found")
        parsed = parse_response(response)
        return Song.model_validate(parsed)
