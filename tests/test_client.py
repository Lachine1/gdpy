import pytest
import pytest_asyncio
from gdpy import Client, User, Level
from gdpy.exceptions import NotFoundError, InvalidRequestError


@pytest_asyncio.fixture
async def client():
    async with Client() as client:
        yield client


class TestUserEndpoints:
    @pytest.mark.asyncio
    async def test_get_user_by_id(self, client: Client):
        user = await client.get_user(account_id=71)
        assert isinstance(user, User)
        assert user.account_id == 71
        assert user.username == "RobTop"

    @pytest.mark.asyncio
    async def test_search_users(self, client: Client):
        users = await client.search_users(query="RobTop")
        assert isinstance(users, list)
        assert len(users) > 0
        assert any(u.username == "RobTop" for u in users)


class TestLevelEndpoints:
    @pytest.mark.asyncio
    async def test_search_levels(self, client: Client):
        levels = await client.search_levels(query="ReTraY", limit=5)
        assert isinstance(levels, list)
        assert len(levels) > 0


class TestClientContext:
    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with Client() as client:
            assert client._client is not None
        assert client._client is None

    @pytest.mark.asyncio
    async def test_is_authenticated_initially_false(self, client: Client):
        assert client.is_authenticated is False
