import pytest
from gdpy import Client, AsyncClient, User, Level
from gdpy.exceptions import NotFoundError, InvalidRequestError


class TestSyncClient:
    def test_get_user_by_id(self):
        with Client() as client:
            user = client.get_user(account_id=71)
            assert isinstance(user, User)
            assert user.account_id == 71
            assert user.username == "RobTop"

    def test_search_users(self):
        with Client() as client:
            users = client.search_users(query="RobTop")
            assert isinstance(users, list)
            assert len(users) > 0

    def test_search_levels(self):
        with Client() as client:
            levels = client.search_levels(query="ReTraY", limit=5)
            assert isinstance(levels, list)
            assert len(levels) > 0

    def test_context_manager(self):
        with Client() as client:
            assert client._client is not None
        assert client._client is None

    def test_is_authenticated_initially_false(self):
        with Client() as client:
            assert client.is_authenticated is False


class TestAsyncClient:
    @pytest.mark.asyncio
    async def test_get_user_by_id(self):
        async with AsyncClient() as client:
            user = await client.get_user(account_id=71)
            assert isinstance(user, User)
            assert user.account_id == 71
            assert user.username == "RobTop"

    @pytest.mark.asyncio
    async def test_search_users(self):
        async with AsyncClient() as client:
            users = await client.search_users(query="RobTop")
            assert isinstance(users, list)
            assert len(users) > 0

    @pytest.mark.asyncio
    async def test_search_levels(self):
        async with AsyncClient() as client:
            levels = await client.search_levels(query="ReTraY", limit=5)
            assert isinstance(levels, list)
            assert len(levels) > 0

    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with AsyncClient() as client:
            assert client._client is not None
        assert client._client is None

    @pytest.mark.asyncio
    async def test_is_authenticated_initially_false(self):
        async with AsyncClient() as client:
            assert client.is_authenticated is False
