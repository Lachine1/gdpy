import os
import json
import pytest
import pytest_asyncio
import asyncio
from gdpy import AsyncClient
from gdpy.exceptions import InvalidRequestError, InvalidCredentialsError

TEST_ACCOUNT_FILE = "tests/.test_account.json"


@pytest_asyncio.fixture
async def client():
    async with AsyncClient() as client:
        yield client


@pytest_asyncio.fixture(autouse=True)
async def rate_limit_delay():
    await asyncio.sleep(1.0)


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

    @pytest.mark.asyncio
    async def test_get_level_by_id(self, client: AsyncClient):
        try:
            await asyncio.sleep(2)
            level = await client.get_level(level_id=128)  # 1st level
            assert level.level_id == 128
            assert level.name != ""
            assert level.objects > 0
        except InvalidRequestError:
            pytest.skip("Rate limited by server")


class TestSongEndpoints:
    @pytest.mark.asyncio
    async def test_get_song(self, client: AsyncClient):
        song = await client.get_song(song_id=803223)  # Xtrullor - Arcana
        assert song.song_id == 803223
        assert song.name != ""
        assert song.author != ""

    @pytest.mark.asyncio
    async def test_song_has_download_url(self, client: AsyncClient):
        song = await client.get_song(song_id=803223)
        assert song.download_url != ""


class TestCommentEndpoints:
    @pytest.mark.asyncio
    async def test_get_level_comments(self, client: AsyncClient):
        await asyncio.sleep(1)
        comments = await client.get_level_comments(level_id=128, limit=5)
        assert isinstance(comments, list)

    @pytest.mark.asyncio
    async def test_comment_has_content(self, client: AsyncClient):
        await asyncio.sleep(1)
        comments = await client.get_level_comments(level_id=128, limit=5)
        if comments:
            assert comments[0].content != ""
            assert comments[0].author != ""


class TestLeaderboardEndpoints:
    @pytest.mark.asyncio
    async def test_get_leaderboard(self, client: AsyncClient):
        leaderboard = await client.get_leaderboard(limit=10)
        assert isinstance(leaderboard, list)
        assert len(leaderboard) > 0

    @pytest.mark.asyncio
    async def test_leaderboard_entry_has_username(self, client: AsyncClient):
        leaderboard = await client.get_leaderboard(limit=5)
        if leaderboard:
            assert leaderboard[0].username != ""
            assert leaderboard[0].stars > 0

    @pytest.mark.asyncio
    async def test_get_creator_leaderboard(self, client: AsyncClient):
        creators = await client.get_leaderboard(limit=10, type="creators")
        assert isinstance(creators, list)
        if creators:
            assert creators[0].username != ""


class TestUserLevelEndpoints:
    @pytest.mark.asyncio
    async def test_get_user_levels(self, client: AsyncClient):
        user = await client.get_user(account_id=71)  # RobTop
        levels = await client.get_user_levels(user_id=user.user_id, limit=5)
        assert isinstance(levels, list)

    @pytest.mark.asyncio
    async def test_user_level_has_name(self, client: AsyncClient):
        user = await client.get_user(account_id=71)
        levels = await client.get_user_levels(user_id=user.user_id, limit=5)
        if levels:
            assert levels[0].name != ""


class TestSearchAndFetch:
    @pytest.mark.asyncio
    async def test_search_and_get_level(self, client: AsyncClient):
        await asyncio.sleep(1)
        levels = await client.search_levels(query="ReTraY", limit=5)
        assert len(levels) > 0
        
        first_level = levels[0]
        await asyncio.sleep(2)
        fetched_level = await client.get_level(level_id=first_level.level_id)
        
        assert fetched_level.level_id == first_level.level_id
        assert fetched_level.name != ""
        assert fetched_level.objects > 0

    @pytest.mark.asyncio
    async def test_fetch_leaderboard_top_user(self, client: AsyncClient):
        await asyncio.sleep(1)
        leaderboard = await client.get_leaderboard(limit=10)
        assert len(leaderboard) > 0

        top_user = leaderboard[0]
        await asyncio.sleep(2)
        user = await client.get_user(account_id=top_user.account_id)

        assert user.username == top_user.username
        assert user.stars > 0


class TestLevelData:
    @pytest.mark.asyncio
    async def test_level_has_level_string(self, client: AsyncClient):
        await asyncio.sleep(1)
        level = await client.get_level(level_id=128)
        assert level.level_string is not None
        assert level.level_string != ""

    @pytest.mark.asyncio
    async def test_level_has_all_fields(self, client: AsyncClient):
        await asyncio.sleep(1)
        level = await client.get_level(level_id=128)
        assert level.level_id > 0
        assert level.name != ""
        assert level.downloads >= 0
        assert level.likes >= 0
        assert level.objects >= 0

    @pytest.mark.asyncio
    async def test_level_comments_have_all_fields(self, client: AsyncClient):
        await asyncio.sleep(1)
        comments = await client.get_level_comments(level_id=128, limit=10)
        if comments:
            comment = comments[0]
            assert comment.content != ""
            assert comment.author != ""
            assert comment.message_id > 0
            assert comment.likes >= 0


class TestUserData:
    @pytest.mark.asyncio
    async def test_user_has_creator_points(self, client: AsyncClient):
        user = await client.get_user(account_id=71)
        assert user.creator_points >= 0

    @pytest.mark.asyncio
    async def test_user_has_all_stats(self, client: AsyncClient):
        user = await client.get_user(account_id=71)
        assert user.stars >= 0
        assert user.diamonds >= 0
        assert user.moons >= 0
        assert user.secret_coins >= 0
        assert user.user_coins >= 0
        assert user.demons >= 0

    @pytest.mark.asyncio
    async def test_user_has_social_links(self, client: AsyncClient):
        user = await client.get_user(account_id=71)
        assert user.youtube is not None or user.twitter is not None or user.twitch is not None

    @pytest.mark.asyncio
    async def test_leaderboard_entry_has_creator_points(self, client: AsyncClient):
        await asyncio.sleep(1)
        leaderboard = await client.get_leaderboard(limit=5)
        if leaderboard:
            entry = leaderboard[0]
            assert entry.creator_points >= 0
            assert entry.stars >= 0
            assert entry.diamonds >= 0
