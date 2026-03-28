import os
import json
import pytest
import pytest_asyncio
from gdpy import AsyncClient
from gdpy.exceptions import InvalidRequestError, InvalidCredentialsError

TEST_ACCOUNT_FILE = "tests/.test_account.json"


@pytest_asyncio.fixture
async def client():
    async with AsyncClient() as client:
        yield client


class TestAuthentication:
    @pytest.mark.asyncio
    async def test_login_invalid_credentials(self, client: AsyncClient):
        try:
            result = await client.login("nonexistentuser12345", "wrongpassword123")
            assert result is False
        except InvalidRequestError:
            pytest.skip("Rate limited by server")

    @pytest.mark.asyncio
    async def test_is_authenticated_initially_false(self, client: AsyncClient):
        assert client.is_authenticated is False

    @pytest.mark.asyncio
    async def test_account_id_initially_none(self, client: AsyncClient):
        assert client.account_id is None

    @pytest.mark.asyncio
    async def test_username_initially_none(self, client: AsyncClient):
        assert client.username is None


class TestUserEndpoints:
    @pytest.mark.asyncio
    async def test_get_user_robtop(self, client: AsyncClient):
        user = await client.get_user(account_id=71)
        assert user.account_id == 71
        assert user.username == "RobTop"
        assert user.stars > 0

    @pytest.mark.asyncio
    async def test_get_user_by_search(self, client: AsyncClient):
        users = await client.search_users(query="RobTop")
        assert len(users) > 0
        robtop = next((u for u in users if u.username == "RobTop"), None)
        assert robtop is not None
        assert robtop.account_id == 71


class TestLevelEndpoints:
    @pytest.mark.asyncio
    async def test_search_levels(self, client: AsyncClient):
        levels = await client.search_levels(query="ReTraY", limit=5)
        assert isinstance(levels, list)
        assert len(levels) > 0

    @pytest.mark.asyncio
    async def test_level_has_name(self, client: AsyncClient):
        levels = await client.search_levels(query="ReTraY", limit=1)
        if levels:
            assert levels[0].name != ""
