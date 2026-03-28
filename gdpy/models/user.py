"""Pydantic models for Geometry Dash API responses.

This module contains all the data models used to represent responses
from the Geometry Dash API, including users, levels, comments, and more.
"""

from enum import IntEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ModLevel(IntEnum):
    """Moderator level for a user.

    Attributes:
        NONE: Not a moderator.
        MODERATOR: Regular moderator (yellow badge).
        ELDER_MOD: Elder moderator (orange badge).
    """

    NONE = 0
    MODERATOR = 1
    ELDER_MOD = 2


class MessageState(IntEnum):
    """Message privacy settings.

    Attributes:
        ALL: Anyone can send messages.
        FRIENDS_ONLY: Only friends can send messages.
        NONE: No one can send messages.
    """

    ALL = 0
    FRIENDS_ONLY = 1
    NONE = 2


class User(BaseModel):
    """Represents a Geometry Dash user profile.

    Contains all information about a user including stats, icons,
    social links, and moderation status.

    Attributes:
        username: The user's display name.
        user_id: The user's ID (different from account ID).
        account_id: The user's account ID.
        stars: Total stars collected.
        diamonds: Total diamonds collected.
        moons: Total moons collected.
        secret_coins: Secret coins collected (max 3).
        user_coins: User coins collected.
        demons: Demons completed.
        creator_points: Creator points earned.
        icon_id: Current icon ID.
        color1: Primary icon color.
        color2: Secondary icon color.
        color3: Glow color (if has_glow is True).
        icon_type: Current icon type (cube, ship, ball, etc.).
        has_glow: Whether glow is enabled.
        youtube: YouTube channel (if set).
        twitter: Twitter handle (if set).
        twitch: Twitch channel (if set).
        discord: Discord handle (if set).
        instagram: Instagram username (if set).
        tiktok: TikTok handle (if set).
        mod_level: Moderator status.
        message_state: Message privacy setting.
        friend_state: Friend request setting.
        comment_history_state: Comment history visibility.
        global_rank: Global leaderboard rank (if on leaderboard).

    Example:
        ```python
        user = await client.get_user(account_id=71)
        print(f"{user.username} has {user.stars} stars")
        ```
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    username: str = Field(alias="1")
    user_id: int = Field(alias="2")
    account_id: int = Field(alias="16")
    stars: int = Field(default=0, alias="3")
    diamonds: int = Field(default=0, alias="46")
    moons: int = Field(default=0, alias="52")
    secret_coins: int = Field(default=0, alias="13")
    user_coins: int = Field(default=0, alias="17")
    demons: int = Field(default=0, alias="4")
    creator_points: int = Field(default=0, alias="8")
    icon_id: int = Field(default=0, alias="9")
    color1: int = Field(default=0, alias="10")
    color2: int = Field(default=0, alias="11")
    color3: int | None = Field(default=None, alias="51")
    icon_type: int = Field(default=0, alias="14")
    has_glow: bool = Field(default=False, alias="28")
    youtube: str | None = Field(default=None, alias="20")
    twitter: str | None = Field(default=None, alias="44")
    twitch: str | None = Field(default=None, alias="45")
    discord: str | None = Field(default=None, alias="58")
    instagram: str | None = Field(default=None, alias="59")
    tiktok: str | None = Field(default=None, alias="60")
    mod_level: ModLevel = Field(default=ModLevel.NONE, alias="49")
    message_state: MessageState = Field(default=MessageState.ALL, alias="18")
    friend_state: int = Field(default=0, alias="19")
    comment_history_state: int = Field(default=0, alias="50")
    global_rank: int | None = Field(default=None, alias="30")

    @field_validator("has_glow", mode="before")
    @classmethod
    def parse_bool(cls, v: Any) -> bool:
        """Parse boolean values from string responses."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            if v == "" or v == "0":
                return False
            return v != "0"
        return bool(v)


class LevelDifficulty(IntEnum):
    """Level difficulty rating.

    Attributes:
        UNSPECIFIED: No difficulty specified.
        AUTO: Auto level (no skill required).
        EASY: Easy difficulty.
        NORMAL: Normal difficulty.
        HARD: Hard difficulty.
        HARDER: Harder difficulty.
        INSANE: Insane difficulty.
        DEMON: Demon difficulty.
    """

    UNSPECIFIED = 0
    AUTO = 1
    EASY = 2
    NORMAL = 3
    HARD = 4
    HARDER = 5
    INSANE = 6
    DEMON = 7


class DemonDifficulty(IntEnum):
    """Demon level difficulty rating.

    Attributes:
        EASY: Easy demon.
        MEDIUM: Medium demon.
        HARD: Hard demon.
        INSANE: Insane demon.
        EXTREME: Extreme demon.
    """

    EASY = 3
    MEDIUM = 4
    HARD = 0
    INSANE = 5
    EXTREME = 6


class LevelLength(IntEnum):
    """Level length classification.

    Attributes:
        TINY: Very short level.
        SHORT: Short level.
        MEDIUM: Medium length level.
        LONG: Long level.
        XL: Extra long level.
    """

    TINY = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    XL = 4


class EpicRating(IntEnum):
    """Level epic/featured rating.

    Attributes:
        NONE: Not epic rated.
        EPIC: Epic rating.
        LEGENDARY: Legendary rating.
        MYTHIC: Mythic rating.
    """

    NONE = 0
    EPIC = 1
    LEGENDARY = 2
    MYTHIC = 3


class Level(BaseModel):
    """Represents a Geometry Dash level.

    Contains all information about a level including stats, difficulty,
    and audio information.

    Attributes:
        level_id: Unique level identifier.
        name: Level name.
        description: Level description.
        version: Level version number.
        author_id: Creator's player ID.
        downloads: Total downloads.
        likes: Total likes.
        stars: Star rating (0 if not rated).
        is_demon: Whether level is a demon.
        is_auto: Whether level is auto.
        featured: Whether level is featured.
        objects: Object count in level.
        length: Level length classification.
        song_id: Custom song ID (if using custom song).
        official_song_id: Official song ID (if using official song).
        coins: Number of user coins in level.
        verified_coins: Whether coins are verified.
        two_player: Whether level supports two players.
        level_string: Level data (only in downloads).
        demon_difficulty: Demon difficulty (if demon).
        epic_rating: Epic/legendary/mythic rating.
        password: Level password (if copyable).

    Example:
        ```python
        level = await client.get_level(level_id=3009486)
        print(f"{level.name} has {level.objects} objects")
        ```
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    level_id: int = Field(alias="1")
    name: str = Field(alias="2")
    description: str = Field(default="", alias="3")
    version: int = Field(default=1, alias="5")
    author_id: int = Field(alias="6")
    downloads: int = Field(default=0, alias="10")
    likes: int = Field(default=0, alias="14")
    stars: int = Field(default=0, alias="18")
    is_demon: bool = Field(default=False, alias="17")
    is_auto: bool = Field(default=False, alias="25")
    featured: bool = Field(default=False, alias="19")
    objects: int = Field(default=0, alias="45")
    length: LevelLength = Field(default=LevelLength.MEDIUM, alias="15")
    song_id: int | None = Field(default=None, alias="35")
    official_song_id: int | None = Field(default=None, alias="12")
    coins: int = Field(default=0, alias="37")
    verified_coins: bool = Field(default=False, alias="38")
    two_player: bool = Field(default=False, alias="31")
    level_string: str | None = Field(default=None, alias="4")
    demon_difficulty: DemonDifficulty | None = Field(default=None, alias="43")
    epic_rating: EpicRating = Field(default=EpicRating.NONE, alias="42")
    password: str | None = Field(default=None, alias="27")

    @field_validator(
        "is_demon",
        "is_auto",
        "featured",
        "verified_coins",
        "two_player",
        mode="before",
    )
    @classmethod
    def parse_bool(cls, v: Any) -> bool:
        """Parse boolean values from string responses."""
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            if v == "" or v == "0":
                return False
            return v != "0"
        return bool(v)


class Comment(BaseModel):
    """Represents a level or profile comment.

    Attributes:
        content: Comment text content (base64 decoded).
        author: Comment author's username.
        author_id: Comment author's user ID.
        likes: Number of likes on the comment.
        message_id: Unique comment/message ID.
        percent: Progress percentage shown in comment.
        age: How long ago the comment was posted.
        is_spam: Whether comment is marked as spam.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    content: str = Field(alias="2")
    author: str = Field(default="", alias="username")
    author_id: int = Field(default=0, alias="3")
    likes: int = Field(default=0, alias="4")
    message_id: int = Field(default=0, alias="6")
    percent: int = Field(default=0, alias="10")
    age: str = Field(default="", alias="9")
    is_spam: bool = Field(default=False, alias="7")

    @field_validator("content", mode="before")
    @classmethod
    def decode_base64(cls, v: Any) -> str:
        """Decode base64 encoded comment content."""
        if isinstance(v, str):
            try:
                import base64
                return base64.b64decode(v).decode("utf-8")
            except Exception:
                return v
        return str(v)


class Song(BaseModel):
    """Represents a custom song from Newgrounds.

    Attributes:
        song_id: Unique song identifier.
        name: Song name.
        author: Song artist name.
        size: File size in MB.
        download_url: URL to download the song.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    song_id: int = Field(alias="1")
    name: str = Field(alias="2")
    author: str = Field(alias="4")
    size: float = Field(default=0.0, alias="5")
    download_url: str = Field(alias="10")


class Message(BaseModel):
    """Represents a private message.

    Attributes:
        message_id: Unique message identifier.
        subject: Message subject line.
        content: Message body content.
        author: Sender's username.
        author_id: Sender's account ID.
        is_read: Whether message has been read.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    message_id: int = Field(alias="1")
    subject: str = Field(alias="4")
    content: str = Field(alias="5")
    author: str = Field(alias="6")
    author_id: int = Field(alias="7")
    is_read: bool = Field(default=False, alias="8")


class FriendRequest(BaseModel):
    """Represents a friend request.

    Attributes:
        request_id: Unique request identifier.
        from_user: Sender's username.
        from_user_id: Sender's user ID.
        to_user: Recipient's username.
        to_user_id: Recipient's user ID.
        message: Optional message with the request.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    request_id: int = Field(alias="1")
    from_user: str = Field(alias="2")
    from_user_id: int = Field(alias="3")
    to_user: str = Field(alias="4")
    to_user_id: int = Field(alias="5")
    message: str = Field(default="", alias="6")


class LeaderboardScore(BaseModel):
    """Represents a leaderboard entry.

    Attributes:
        username: Player's username.
        user_id: Player's user ID.
        stars: Total stars.
        demons: Demons completed.
        ranking: Global rank position.
        creator_points: Creator points earned.
        icon_id: Current icon ID.
        color1: Primary icon color.
        color2: Secondary icon color.
        secret_coins: Secret coins collected (max 3).
        icon_type: Current icon type.
        account_id: Player's account ID.
        user_coins: User coins collected.
        diamonds: Total diamonds.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    username: str = Field(alias="1")
    user_id: int = Field(alias="2")
    stars: int = Field(default=0, alias="3")
    demons: int = Field(default=0, alias="4")
    ranking: int = Field(default=0, alias="6")
    creator_points: int = Field(default=0, alias="8")
    icon_id: int = Field(default=0, alias="9")
    color1: int = Field(default=0, alias="10")
    color2: int = Field(default=0, alias="11")
    secret_coins: int = Field(default=0, alias="13")
    icon_type: int = Field(default=0, alias="14")
    account_id: int = Field(default=0, alias="16")
    user_coins: int = Field(default=0, alias="17")
    diamonds: int = Field(default=0, alias="46")


class Gauntlet(BaseModel):
    """Represents a Geometry Dash gauntlet.

    Attributes:
        gauntlet_id: Unique gauntlet identifier.
        levels: List of level IDs in the gauntlet.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    gauntlet_id: int = Field(alias="1")
    levels: str = Field(alias="3")

    @property
    def level_ids(self) -> list[int]:
        """Get list of level IDs as integers."""
        return [int(lvl) for lvl in self.levels.split(",") if lvl]


class MapPack(BaseModel):
    """Represents a Geometry Dash map pack.

    Attributes:
        pack_id: Unique pack identifier.
        name: Pack name.
        levels: Comma-separated level IDs.
        stars: Stars rewarded for completion.
        coins: Coins rewarded for completion.
        difficulty: Pack difficulty (0-10).
        text_color: RGB color for title text.
        bar_color: RGB color for completion bar.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    pack_id: int = Field(alias="1")
    name: str = Field(alias="2")
    levels: str = Field(alias="3")
    stars: int = Field(default=0, alias="4")
    coins: int = Field(default=0, alias="5")
    difficulty: int = Field(default=0, alias="6")
    text_color: str = Field(default="255,255,255", alias="7")
    bar_color: str = Field(default="255,255,255", alias="8")

    @property
    def level_ids(self) -> list[int]:
        """Get list of level IDs as integers."""
        return [int(lvl) for lvl in self.levels.split(",") if lvl]


class DailyLevel(BaseModel):
    """Represents daily/weekly level info.

    Attributes:
        index: Current daily/weekly level index.
        time_left: Seconds until next level.
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    index: int = Field(default=0)
    time_left: int = Field(default=0)


class TopArtist(BaseModel):
    """Represents a top artist.

    Attributes:
        name: Artist name.
        youtube: YouTube channel (optional).
    """

    model_config = ConfigDict(populate_by_name=True, extra="allow")

    name: str = Field(alias="4")
    youtube: str | None = Field(default=None, alias="7")
