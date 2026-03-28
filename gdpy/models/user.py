from enum import IntEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ModLevel(IntEnum):
    NONE = 0
    MODERATOR = 1
    ELDER_MOD = 2


class MessageState(IntEnum):
    ALL = 0
    FRIENDS_ONLY = 1
    NONE = 2


class User(BaseModel):
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
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            if v == "" or v == "0":
                return False
            return v != "0"
        return bool(v)


class LevelDifficulty(IntEnum):
    UNSPECIFIED = 0
    AUTO = 1
    EASY = 2
    NORMAL = 3
    HARD = 4
    HARDER = 5
    INSANE = 6
    DEMON = 7


class DemonDifficulty(IntEnum):
    EASY = 3
    MEDIUM = 4
    HARD = 0
    INSANE = 5
    EXTREME = 6


class LevelLength(IntEnum):
    TINY = 0
    SHORT = 1
    MEDIUM = 2
    LONG = 3
    XL = 4


class EpicRating(IntEnum):
    NONE = 0
    EPIC = 1
    LEGENDARY = 2
    MYTHIC = 3


class Level(BaseModel):
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
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            if v == "" or v == "0":
                return False
            return v != "0"
        return bool(v)


class Comment(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    comment_id: int = Field(alias="2")
    level_id: int = Field(default=0, alias="1")
    content: str = Field(alias="9")
    author: str = Field(alias="3")
    author_id: int = Field(alias="6")
    likes: int = Field(default=0, alias="12")
    is_spam: bool = Field(default=False, alias="7")


class Song(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    song_id: int = Field(alias="1")
    name: str = Field(alias="2")
    author: str = Field(alias="4")
    size: float = Field(default=0.0, alias="5")
    download_url: str = Field(alias="10")


class Message(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    message_id: int = Field(alias="1")
    subject: str = Field(alias="4")
    content: str = Field(alias="5")
    author: str = Field(alias="6")
    author_id: int = Field(alias="7")
    is_read: bool = Field(default=False, alias="8")


class FriendRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    request_id: int = Field(alias="1")
    from_user: str = Field(alias="2")
    from_user_id: int = Field(alias="3")
    to_user: str = Field(alias="4")
    to_user_id: int = Field(alias="5")
    message: str = Field(default="", alias="6")


class LeaderboardScore(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="allow")

    rank: int = Field(alias="1")
    username: str = Field(alias="2")
    user_id: int = Field(alias="3")
    account_id: int = Field(alias="4")
    stars: int = Field(default=0, alias="5")
    diamonds: int = Field(default=0, alias="6")
