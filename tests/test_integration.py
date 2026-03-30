import asyncio

import pytest
import pytest_asyncio

from gdpy import AsyncClient
from gdpy.exceptions import InvalidRequestError
from gdpy.models import LevelDifficulty


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
            level = await client.get_level(level_id=128)
            assert level.level_id == 128
            assert level.name != ""
            assert level.objects > 0
        except InvalidRequestError:
            pytest.skip("Rate limited by server")


class TestSongEndpoints:
    @pytest.mark.asyncio
    async def test_get_song(self, client: AsyncClient):
        song = await client.get_song(song_id=803223)
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
        user = await client.get_user(account_id=71)
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


class TestDailyLevel:
    @pytest.mark.asyncio
    async def test_get_daily_level(self, client: AsyncClient):
        daily = await client.get_daily_level()
        assert daily.index >= 0

    @pytest.mark.asyncio
    async def test_get_weekly_level(self, client: AsyncClient):
        weekly = await client.get_daily_level(type="weekly")
        assert weekly.index >= 0


class TestGauntlets:
    @pytest.mark.asyncio
    async def test_get_gauntlets(self, client: AsyncClient):
        gauntlets = await client.get_gauntlets()
        assert isinstance(gauntlets, list)

    @pytest.mark.asyncio
    async def test_gauntlet_has_levels(self, client: AsyncClient):
        gauntlets = await client.get_gauntlets()
        if gauntlets:
            assert gauntlets[0].gauntlet_id > 0
            assert len(gauntlets[0].level_ids) > 0


class TestMapPacks:
    @pytest.mark.asyncio
    async def test_get_map_packs(self, client: AsyncClient):
        packs = await client.get_map_packs()
        assert isinstance(packs, list)

    @pytest.mark.asyncio
    async def test_map_pack_has_name(self, client: AsyncClient):
        packs = await client.get_map_packs()
        if packs:
            assert packs[0].pack_id > 0
            assert packs[0].name != ""


class TestTopArtists:
    @pytest.mark.asyncio
    async def test_get_top_artists(self, client: AsyncClient):
        artists = await client.get_top_artists()
        assert isinstance(artists, list)

    @pytest.mark.asyncio
    async def test_top_artist_has_name(self, client: AsyncClient):
        artists = await client.get_top_artists()
        if artists:
            assert artists[0].name != ""


class TestAccountComments:
    @pytest.mark.asyncio
    async def test_get_account_comments(self, client: AsyncClient):
        comments = await client.get_account_comments(account_id=71)
        assert isinstance(comments, list)

    @pytest.mark.asyncio
    async def test_account_comment_has_content(self, client: AsyncClient):
        comments = await client.get_account_comments(account_id=71, limit=5)
        if comments:
            assert comments[0].content != ""


class TestCommentHistory:
    @pytest.mark.asyncio
    async def test_get_comment_history(self, client: AsyncClient):
        user = await client.get_user(account_id=71)
        comments = await client.get_comment_history(user_id=user.user_id)
        assert isinstance(comments, list)


class TestLevelDifficulty:
    """Test difficulty computation on real levels."""

    @pytest.mark.asyncio
    async def test_easy_level_difficulty(self, client: AsyncClient):
        """ReTraY (ID 6508283) should be EASY."""
        level = await client.get_level(level_id=6508283)
        assert level.name == "ReTraY"
        assert level.difficulty == LevelDifficulty.EASY

    @pytest.mark.asyncio
    async def test_normal_level_difficulty(self, client: AsyncClient):
        """Level Easy (ID 11940) should be NORMAL."""
        level = await client.get_level(level_id=11940)
        assert level.name == "Level Easy"
        assert level.difficulty == LevelDifficulty.NORMAL

    @pytest.mark.asyncio
    async def test_hard_level_difficulty(self, client: AsyncClient):
        """OuterSpace (ID 27732941) should be HARD."""
        level = await client.get_level(level_id=27732941)
        assert level.name == "OuterSpace"
        assert level.difficulty == LevelDifficulty.HARD

    @pytest.mark.asyncio
    async def test_harder_level_difficulty(self, client: AsyncClient):
        """Shock (ID 28225110) should be HARDER."""
        level = await client.get_level(level_id=28225110)
        assert level.name == "Shock"
        assert level.difficulty == LevelDifficulty.HARDER

    @pytest.mark.asyncio
    async def test_insane_level_difficulty(self, client: AsyncClient):
        """Unity (ID 12057578) should be INSANE."""
        level = await client.get_level(level_id=12057578)
        assert level.name == "Unity"
        assert level.difficulty == LevelDifficulty.INSANE

    @pytest.mark.asyncio
    async def test_auto_level_difficulty(self, client: AsyncClient):
        """ninemore (ID 114552503) should be AUTO."""
        level = await client.get_level(level_id=114552503)
        assert level.name == "ninemore"
        assert level.difficulty == LevelDifficulty.AUTO

    @pytest.mark.asyncio
    async def test_easy_demon_difficulty(self, client: AsyncClient):
        """The Nightmare (ID 13519) should be EASY_DEMON."""
        level = await client.get_level(level_id=13519)
        assert level.name == "The Nightmare"
        assert level.difficulty == LevelDifficulty.EASY_DEMON

    @pytest.mark.asyncio
    async def test_medium_demon_difficulty(self, client: AsyncClient):
        """Skeletal Shenanigans (ID 118509879) should be MEDIUM_DEMON."""
        level = await client.get_level(level_id=118509879)
        assert level.name == "Skeletal Shenanigans"
        assert level.difficulty == LevelDifficulty.MEDIUM_DEMON

    @pytest.mark.asyncio
    async def test_hard_demon_difficulty(self, client: AsyncClient):
        """Nine Circles (ID 4284013) should be HARD_DEMON."""
        level = await client.get_level(level_id=4284013)
        assert level.name == "Nine Circles"
        assert level.difficulty == LevelDifficulty.HARD_DEMON

    @pytest.mark.asyncio
    async def test_extreme_demon_difficulty(self, client: AsyncClient):
        """Bloodbath (ID 10565740) should be EXTREME_DEMON."""
        level = await client.get_level(level_id=10565740)
        assert level.name == "Bloodbath"
        assert level.difficulty == LevelDifficulty.EXTREME_DEMON
