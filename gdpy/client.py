"""Main client module for interacting with the Geometry Dash API.

This library is based on the Geometry Dash API documentation from:
https://github.com/Rifct/gd-docs
"""

import httpx

from gdpy.constants import Secrets, URLs
from gdpy.crypto import generate_gjp2
from gdpy.exceptions import (
    AccountDisabledError,
    EmailTakenError,
    InvalidCredentialsError,
    InvalidEmailError,
    InvalidRequestError,
    NotFoundError,
    PasswordTooShortError,
    UsernameTakenError,
    UsernameTooShortError,
)
from gdpy.models import (
    Comment,
    DailyLevel,
    FriendRequest,
    Gauntlet,
    LeaderboardScore,
    Level,
    MapPack,
    Message,
    Song,
    TopArtist,
    User,
)
from gdpy.utils.parsing import parse_list_response, parse_response


class Client:
    """Synchronous client for interacting with the Geometry Dash API.

    This client provides methods to interact with Geometry Dash's private API,
    including user lookups, level searches, and authentication.

    Based on the Geometry Dash API documentation: https://github.com/Rifct/gd-docs

    Args:
        base_url: Optional custom base URL for the API. Defaults to boomlings.com.

    Example:
    ```python
    client = Client()
    user = client.get_user(account_id=71)
    print(user.username)
    client.close()

    # Or use as context manager:
    with Client() as client:
        user = client.get_user(account_id=71)
        print(user.username)
    ```
    """

    def __init__(self, base_url: str | None = None) -> None:
        """Initialize the client.

        Args:
            base_url: Optional custom base URL for the API.
        """
        self.base_url = base_url or URLs.DEFAULT
        self._client: httpx.Client | None = None
        self._account_id: int | None = None
        self._player_id: int | None = None
        self._username: str | None = None
        self._password: str | None = None

    def _ensure_client(self) -> httpx.Client:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.Client(
                headers={
                    "User-Agent": "",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                timeout=30.0,
            )
        return self._client

    def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            self._client.close()
            self._client = None

    def __enter__(self) -> "Client":
        """Enter context manager and initialize HTTP client."""
        self._ensure_client()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit context manager and close HTTP client."""
        self.close()

    @property
    def is_authenticated(self) -> bool:
        """Check if the client is authenticated."""
        return self._account_id is not None

    @property
    def account_id(self) -> int | None:
        """Get the authenticated account ID."""
        return self._account_id

    @property
    def username(self) -> str | None:
        """Get the authenticated username."""
        return self._username

    def _request(self, endpoint: str, data: dict[str, str], secret: str = Secrets.COMMON) -> str:
        """Make a request to the Geometry Dash API."""
        client = self._ensure_client()
        data["secret"] = secret
        url = f"{self.base_url}/{endpoint}"
        response = client.post(url, data=data)
        response.raise_for_status()
        return response.text

    def _handle_error(self, response: str) -> None:
        """Handle error responses from the API."""
        if response.startswith("-"):
            code = int(response)
            if code == -1:
                raise InvalidRequestError("Rate limited or invalid request")
            elif code == -11:
                raise InvalidCredentialsError("Invalid username or password")
            elif code == -12:
                raise AccountDisabledError("Account has been disabled")
            elif code == -2:
                raise UsernameTakenError("Username is already taken")
            elif code == -3:
                raise EmailTakenError("Email is already registered")
            elif code == -6:
                raise InvalidEmailError("Invalid or blacklisted email address")
            elif code == -8:
                raise PasswordTooShortError("Password must be at least 6 characters")
            elif code == -9:
                raise UsernameTooShortError("Username must be at least 3 characters")
            else:
                raise NotFoundError(f"Request failed with code {code}")

    def login(self, username: str, password: str) -> bool:
        """Login to a Geometry Dash account.

        Args:
            username: Account username.
            password: Account password.

        Returns:
            True if login successful, False otherwise.

        Raises:
            InvalidCredentialsError: If credentials are incorrect.
            AccountDisabledError: If account is disabled.
            InvalidRequestError: If rate limited.
        """
        import random

        udid = "S" + str(random.randint(100000, 100000000)) + str(random.randint(100000, 100000000))
        gjp2 = generate_gjp2(password)
        data = {
            "udid": udid,
            "userName": username,
            "gjp2": gjp2,
            "secret": Secrets.ACCOUNT,
        }
        response = self._request("accounts/loginGJAccount.php", data)
        if response.startswith("-"):
            self._handle_error(response)
            return False
        parts = response.split(",")
        if len(parts) >= 2:
            self._account_id = int(parts[0])
            self._player_id = int(parts[1])
            self._username = username
            self._password = password
            return True
        return False

    def register(self, username: str, password: str, email: str) -> bool:
        """Register a new Geometry Dash account.

        Uses the pre-2.2 API endpoint. GD 2.2 added captcha protection via
        register.php web page, but registerGJAccount.php API still works.

        Note: GD rejects temporary email addresses.

        Args:
            username: Desired username (min 3 characters).
            password: Desired password (min 6 characters).
            email: Email address (must be real, not temp email).

        Returns:
            True if registration successful, False otherwise.

        Raises:
            UsernameTakenError: If username is already taken.
            EmailTakenError: If email is already registered.
            PasswordTooShortError: If password is too short.
            UsernameTooShortError: If username is too short.
            InvalidEmailError: If email is invalid or blacklisted.
        """
        data = {
            "userName": username,
            "password": password,
            "email": email,
        }
        response = self._request("accounts/registerGJAccount.php", data, Secrets.ACCOUNT)
        if response.startswith("-"):
            self._handle_error(response)
            return False
        return response == "1"

    def get_user(self, account_id: int) -> User:
        """Get a user by their account ID.

        Args:
            account_id: The account ID of the user.

        Returns:
            User object with profile information.

        Raises:
            NotFoundError: If user is not found.
            InvalidRequestError: If rate limited.
        """
        data = {"targetAccountID": str(account_id)}
        response = self._request("getGJUserInfo20.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return User.model_validate(parsed)

    def search_users(self, query: str, limit: int = 10) -> list[User]:
        """Search for users by name.

        Args:
            query: Search query (username or partial match).
            limit: Maximum number of results to return.

        Returns:
            List of User objects matching the query.
        """
        data = {"str": query, "total": str(limit), "page": "0"}
        response = self._request("getGJUsers20.php", data)
        if response.startswith("-"):
            return []
        user_data = parse_response(response.split("#")[0])
        return [User.model_validate(user_data)]

    def get_level(self, level_id: int) -> Level:
        """Get a level by its ID.

        Args:
            level_id: The ID of the level.

        Returns:
            Level object with level information.

        Raises:
            NotFoundError: If level is not found.
            InvalidRequestError: If rate limited.
        """
        data = {"levelID": str(level_id)}
        response = self._request("downloadGJLevel22.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response.split("#")[0])
        return Level.model_validate(parsed)

    def search_levels(self, query: str = "", limit: int = 10, page: int = 0) -> list[Level]:
        """Search for levels by name.

        Args:
            query: Search query (level name or partial match).
            limit: Maximum number of results per page.
            page: Page number for pagination.

        Returns:
            List of Level objects matching the query.
        """
        data = {"str": query, "total": str(limit), "page": str(page), "type": "0"}
        response = self._request("getGJLevels21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        levels_data = parse_list_response(parts[0])
        return [Level.model_validate(level) for level in levels_data]

    def get_song(self, song_id: int) -> Song:
        """Get a custom song by its ID.

        Args:
            song_id: The ID of the song.

        Returns:
            Song object with song information.

        Raises:
            NotFoundError: If song is not found.
            InvalidRequestError: If rate limited.
        """
        data = {"songID": str(song_id)}
        response = self._request("getGJSongInfo.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return Song.model_validate(parsed)

    def get_level_comments(self, level_id: int, limit: int = 10, page: int = 0) -> list[Comment]:
        """Get comments for a level.

        Args:
            level_id: The ID of the level.
            limit: Maximum number of comments to return.
            page: Page number for pagination.

        Returns:
            List of Comment objects.
        """
        data = {
            "levelID": str(level_id),
            "total": str(limit),
            "page": str(page),
            "mode": "0",
        }
        response = self._request("getGJComments21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        comments = []
        for comment_str in parts[0].split("|"):
            if not comment_str:
                continue
            comment_parts = comment_str.split(":")
            comment_data = parse_response(comment_parts[0])
            if len(comment_parts) > 1:
                user_data = parse_response(comment_parts[1])
                comment_data["username"] = user_data.get("1", "")
            comments.append(Comment.model_validate(comment_data))
        return comments

    def get_leaderboard(self, limit: int = 100, type: str = "top") -> list[LeaderboardScore]:
        """Get the leaderboard.

        Args:
            limit: Maximum number of results (max 100).
            type: Leaderboard type - "top" or "creators".

        Returns:
            List of LeaderboardScore objects.
        """
        type_value = "creators" if type == "creators" else "top"
        data = {"type": type_value, "count": str(min(limit, 100))}
        response = self._request("getGJScores20.php", data)
        if response.startswith("-"):
            return []
        entries_data = parse_list_response(response)
        return [LeaderboardScore.model_validate(e) for e in entries_data]

    def get_user_levels(self, user_id: int, limit: int = 10, page: int = 0) -> list[Level]:
        """Get levels created by a user.

        Args:
            user_id: The user's ID (not account ID).
            limit: Maximum number of levels to return.
            page: Page number for pagination.

        Returns:
            List of Level objects created by the user.
        """
        data = {
            "str": str(user_id),
            "total": str(limit),
            "page": str(page),
            "type": "5",
        }
        response = self._request("getGJLevels21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        levels_data = parse_list_response(parts[0])
        return [Level.model_validate(level) for level in levels_data]

    def get_daily_level(self, type: str = "daily") -> DailyLevel:
        """Get the current daily/weekly level info.

        Args:
            type: "daily", "weekly", or "event".

        Returns:
            DailyLevel object with index and time_left.
        """
        type_map = {"daily": "0", "weekly": "1", "event": "2"}
        data = {"type": type_map.get(type, "0")}
        response = self._request("getGJDailyLevel.php", data)
        if response.startswith("-"):
            return DailyLevel()
        parts = response.split("|")
        if len(parts) >= 2:
            return DailyLevel(index=int(parts[0]), time_left=int(parts[1]))
        return DailyLevel()

    def get_gauntlets(self) -> list[Gauntlet]:
        """Get all gauntlets.

        Returns:
            List of Gauntlet objects.
        """
        data = {"special": "1"}
        response = self._request("getGJGauntlets21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        gauntlets_data = parse_list_response(parts[0])
        return [Gauntlet.model_validate(g) for g in gauntlets_data]

    def get_map_packs(self, page: int = 0) -> list[MapPack]:
        """Get map packs.

        Args:
            page: Page number for pagination.

        Returns:
            List of MapPack objects.
        """
        data = {"page": str(page)}
        response = self._request("getGJMapPacks21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        packs_data = parse_list_response(parts[0])
        return [MapPack.model_validate(p) for p in packs_data]

    def get_top_artists(self, page: int = 0) -> list[TopArtist]:
        """Get RobTop's handpicked top artists.

        Args:
            page: Page number for pagination.

        Returns:
            List of TopArtist objects.
        """
        data = {"page": str(page)}
        response = self._request("getGJTopArtists.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        artists_data = parse_list_response(parts[0])
        return [TopArtist.model_validate(a) for a in artists_data]

    def get_account_comments(
        self, account_id: int, limit: int = 10, page: int = 0
    ) -> list[Comment]:
        """Get comments on a user's profile.

        Args:
            account_id: The account ID of the user.
            limit: Maximum number of comments to return.
            page: Page number for pagination.

        Returns:
            List of Comment objects.
        """
        data = {
            "accountID": str(account_id),
            "total": str(limit),
            "page": str(page),
        }
        response = self._request("getGJAccountComments20.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        comments_data = parse_list_response(parts[0])
        return [Comment.model_validate(c) for c in comments_data]

    def get_comment_history(
        self, user_id: int, limit: int = 10, page: int = 0, mode: str = "recent"
    ) -> list[Comment]:
        """Get a user's comment history (comments they've posted on levels).

        Args:
            user_id: The user's ID (not account ID).
            limit: Maximum number of comments to return.
            page: Page number for pagination.
            mode: "recent" or "liked".

        Returns:
            List of Comment objects.
        """
        mode_value = "1" if mode == "liked" else "0"
        data = {
            "userID": str(user_id),
            "total": str(limit),
            "page": str(page),
            "mode": mode_value,
        }
        response = self._request("getGJCommentHistory.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        comments = []
        for comment_str in parts[0].split("|"):
            if not comment_str:
                continue
            comment_parts = comment_str.split(":")
            comment_data = parse_response(comment_parts[0])
            if len(comment_parts) > 1:
                user_data = parse_response(comment_parts[1])
                comment_data["username"] = user_data.get("1", "")
            comments.append(Comment.model_validate(comment_data))
        return comments

    def get_messages(self, limit: int = 10, page: int = 0, sent: bool = False) -> list[Message]:
        """Get inbox or sent messages. Requires authentication.

        Args:
            limit: Maximum number of messages to return.
            page: Page number for pagination.
            sent: If True, get sent messages instead of inbox.

        Returns:
            List of Message objects.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get messages")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "page": str(page),
            "total": str(limit),
            "getSent": "1" if sent else "0",
        }
        response = self._request("getGJMessages20.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        messages_data = parse_list_response(parts[0])
        return [Message.model_validate(m) for m in messages_data]

    def get_message(self, message_id: int) -> Message:
        """Download full message content. Requires authentication.

        Args:
            message_id: The message ID to download.

        Returns:
            Message object with full content.

        Raises:
            RuntimeError: If not authenticated.
            NotFoundError: If message not found.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get message")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "messageID": str(message_id),
        }
        response = self._request("downloadGJMessage20.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return Message.model_validate(parsed)

    def send_message(self, recipient_id: int, subject: str, body: str) -> bool:
        """Send a private message. Requires authentication.

        Args:
            recipient_id: The recipient's account ID.
            subject: Message subject.
            body: Message body.

        Returns:
            True if message sent successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to send message")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "toAccountID": str(recipient_id),
            "subject": base64.b64encode(subject.encode()).decode(),
            "body": base64.b64encode(body.encode()).decode(),
        }
        response = self._request("uploadGJMessage20.php", data)
        return response != "-1"

    def delete_message(self, message_id: int) -> bool:
        """Delete a message. Requires authentication.

        Args:
            message_id: The message ID to delete.

        Returns:
            True if deleted successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete message")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "messageID": str(message_id),
        }
        response = self._request("deleteGJMessages20.php", data)
        return response == "1"

    def get_friend_requests(
        self, limit: int = 10, page: int = 0, sent: bool = False
    ) -> list[FriendRequest]:
        """Get friend requests. Requires authentication.

        Args:
            limit: Maximum number of requests to return.
            page: Page number for pagination.
            sent: If True, get sent requests instead of received.

        Returns:
            List of FriendRequest objects.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get friend requests")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "page": str(page),
            "total": str(limit),
            "getSent": "1" if sent else "0",
        }
        response = self._request("getGJFriendRequests20.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        requests_data = parse_list_response(parts[0])
        return [FriendRequest.model_validate(r) for r in requests_data]

    def send_friend_request(self, recipient_id: int, message: str = "") -> bool:
        """Send a friend request. Requires authentication.

        Args:
            recipient_id: The recipient's account ID.
            message: Optional message with the request.

        Returns:
            True if request sent successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to send friend request")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "toAccountID": str(recipient_id),
            "comment": base64.b64encode(message.encode()).decode() if message else "",
        }
        response = self._request("uploadFriendRequest20.php", data)
        return response != "-1"

    def accept_friend_request(self, request_id: int) -> bool:
        """Accept a friend request. Requires authentication.

        Args:
            request_id: The friend request ID.

        Returns:
            True if accepted successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to accept friend request")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "requestID": str(request_id),
        }
        response = self._request("acceptGJFriendRequest20.php", data)
        return response == "1"

    def delete_friend_request(self, request_id: int) -> bool:
        """Delete a friend request. Requires authentication.

        Args:
            request_id: The friend request ID.

        Returns:
            True if deleted successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete friend request")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "requestID": str(request_id),
        }
        response = self._request("deleteGJFriendRequests20.php", data)
        return response == "1"

    def get_friends(self) -> list[User]:
        """Get friends list. Requires authentication.

        Returns:
            List of User objects.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get friends")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "type": "0",
        }
        response = self._request("getGJUserList20.php", data)
        if response.startswith("-"):
            return []
        users_data = parse_list_response(response)
        return [User.model_validate(u) for u in users_data]

    def remove_friend(self, friend_id: int) -> bool:
        """Remove a friend. Requires authentication.

        Args:
            friend_id: The friend's account ID.

        Returns:
            True if removed successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to remove friend")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "targetAccountID": str(friend_id),
        }
        response = self._request("removeGJFriend20.php", data)
        return response == "1"

    def block_user(self, user_id: int) -> bool:
        """Block a user. Requires authentication.

        Args:
            user_id: The user's account ID to block.

        Returns:
            True if blocked successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to block user")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "targetAccountID": str(user_id),
        }
        response = self._request("blockGJUser20.php", data)
        return response == "1"

    def unblock_user(self, user_id: int) -> bool:
        """Unblock a user. Requires authentication.

        Args:
            user_id: The user's account ID to unblock.

        Returns:
            True if unblocked successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to unblock user")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "targetAccountID": str(user_id),
        }
        response = self._request("unblockGJUser20.php", data)
        return response == "1"

    def get_blocked_users(self) -> list[User]:
        """Get blocked users list. Requires authentication.

        Returns:
            List of User objects.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get blocked users")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "type": "1",
        }
        response = self._request("getGJUserList20.php", data)
        if response.startswith("-"):
            return []
        users_data = parse_list_response(response)
        return [User.model_validate(u) for u in users_data]

    def like_level(self, level_id: int, like: bool = True) -> bool:
        """Like or dislike a level.

        Args:
            level_id: The level ID.
            like: True to like, False to dislike.

        Returns:
            True if successful.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to like levels")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "itemID": str(level_id),
            "type": "1",
            "like": "1" if like else "0",
        }
        response = self._request("likeGJItem211.php", data)
        return response == "1"

    def like_comment(self, comment_id: int, like: bool = True) -> bool:
        """Like or dislike a level comment.

        Args:
            comment_id: The comment ID.
            like: True to like, False to dislike.

        Returns:
            True if successful.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to like comments")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "itemID": str(comment_id),
            "type": "2",
            "like": "1" if like else "0",
        }
        response = self._request("likeGJItem211.php", data)
        return response == "1"

    def post_level_comment(self, level_id: int, content: str, percent: int = 0) -> int | None:
        """Post a comment on a level. Requires authentication.

        Args:
            level_id: The level ID to comment on.
            content: The comment content.
            percent: Optional percentage to display.

        Returns:
            Comment ID if successful, None otherwise.

        Raises:
            RuntimeError: If not authenticated.
        """
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to post comment")
        encoded_content = base64.b64encode(content.encode()).decode()
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "userName": self._username,
            "comment": encoded_content,
            "levelID": str(level_id),
            "percent": str(percent),
        }
        response = self._request("uploadGJComment21.php", data)
        if response.startswith("-"):
            return None
        return int(response) if response.isdigit() else None

    def delete_level_comment(self, comment_id: int, level_id: int) -> bool:
        """Delete a level comment. Requires authentication.

        Args:
            comment_id: The comment ID to delete.
            level_id: The level ID the comment is on.

        Returns:
            True if deleted successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete comment")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "commentID": str(comment_id),
            "levelID": str(level_id),
        }
        response = self._request("deleteGJComment20.php", data)
        return response == "1"

    def post_profile_comment(self, content: str) -> int | None:
        """Post a comment on your profile. Requires authentication.

        Args:
            content: The comment content.

        Returns:
            Comment ID if successful, None otherwise.

        Raises:
            RuntimeError: If not authenticated.
        """
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to post profile comment")
        encoded_content = base64.b64encode(content.encode()).decode()
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "userName": self._username,
            "comment": encoded_content,
        }
        response = self._request("uploadGJAccComment20.php", data)
        if response.startswith("-"):
            return None
        return int(response) if response.isdigit() else None

    def delete_profile_comment(self, comment_id: int) -> bool:
        """Delete a profile comment. Requires authentication.

        Args:
            comment_id: The comment ID to delete.

        Returns:
            True if deleted successfully.

        Raises:
            RuntimeError: If not authenticated.
        """
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete profile comment")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "commentID": str(comment_id),
        }
        response = self._request("deleteGJAccComment20.php", data)
        return response == "1"


class AsyncClient:
    """Asynchronous client for interacting with the Geometry Dash API.

    This client provides async methods to interact with Geometry Dash's private API,
    including user lookups, level searches, and authentication.

    Based on the Geometry Dash API documentation: https://github.com/Rifct/gd-docs

    Args:
        base_url: Optional custom base URL for the API. Defaults to boomlings.com.

    Example:
    ```python
    client = AsyncClient()
    user = await client.get_user(account_id=71)
    print(user.username)
    await client.close()

    # Or use as context manager:
    async with AsyncClient() as client:
        user = await client.get_user(account_id=71)
        print(user.username)
    ```
    """

    def __init__(self, base_url: str | None = None) -> None:
        """Initialize the async client.

        Args:
            base_url: Optional custom base URL for the API.
        """
        self.base_url = base_url or URLs.DEFAULT
        self._client: httpx.AsyncClient | None = None
        self._account_id: int | None = None
        self._player_id: int | None = None
        self._username: str | None = None
        self._password: str | None = None

    def _ensure_client(self) -> httpx.AsyncClient:
        """Ensure HTTP client is initialized."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    "User-Agent": "",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                timeout=30.0,
            )
        return self._client

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self) -> "AsyncClient":
        """Enter async context manager and initialize HTTP client."""
        self._ensure_client()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: object,
    ) -> None:
        """Exit async context manager and close HTTP client."""
        await self.close()

    @property
    def is_authenticated(self) -> bool:
        """Check if the client is authenticated."""
        return self._account_id is not None

    @property
    def account_id(self) -> int | None:
        """Get the authenticated account ID."""
        return self._account_id

    @property
    def username(self) -> str | None:
        """Get the authenticated username."""
        return self._username

    async def _request(
        self, endpoint: str, data: dict[str, str], secret: str = Secrets.COMMON
    ) -> str:
        """Make a request to the Geometry Dash API."""
        client = self._ensure_client()
        data["secret"] = secret
        url = f"{self.base_url}/{endpoint}"
        response = await client.post(url, data=data)
        response.raise_for_status()
        return response.text

    def _handle_error(self, response: str) -> None:
        """Handle error responses from the API."""
        if response.startswith("-"):
            code = int(response)
            if code == -1:
                raise InvalidRequestError("Rate limited or invalid request")
            elif code == -11:
                raise InvalidCredentialsError("Invalid username or password")
            elif code == -12:
                raise AccountDisabledError("Account has been disabled")
            elif code == -2:
                raise UsernameTakenError("Username is already taken")
            elif code == -3:
                raise EmailTakenError("Email is already registered")
            elif code == -6:
                raise InvalidEmailError("Invalid or blacklisted email address")
            elif code == -8:
                raise PasswordTooShortError("Password must be at least 6 characters")
            elif code == -9:
                raise UsernameTooShortError("Username must be at least 3 characters")
            else:
                raise NotFoundError(f"Request failed with code {code}")

    async def login(self, username: str, password: str) -> bool:
        """Login to a Geometry Dash account.

        Args:
            username: Account username.
            password: Account password.

        Returns:
            True if login successful, False otherwise.

        Raises:
            InvalidCredentialsError: If credentials are incorrect.
            AccountDisabledError: If account is disabled.
            InvalidRequestError: If rate limited.
        """
        import random

        udid = "S" + str(random.randint(100000, 100000000)) + str(random.randint(100000, 100000000))
        gjp2 = generate_gjp2(password)
        data = {
            "udid": udid,
            "userName": username,
            "gjp2": gjp2,
            "secret": Secrets.ACCOUNT,
        }
        response = await self._request("accounts/loginGJAccount.php", data)
        if response.startswith("-"):
            self._handle_error(response)
            return False
        parts = response.split(",")
        if len(parts) >= 2:
            self._account_id = int(parts[0])
            self._player_id = int(parts[1])
            self._username = username
            self._password = password
            return True
        return False

    async def register(self, username: str, password: str, email: str) -> bool:
        """Register a new Geometry Dash account.

        Uses the pre-2.2 API endpoint. GD 2.2 added captcha protection via
        register.php web page, but registerGJAccount.php API still works.

        Note: GD rejects temporary email addresses.

        Args:
            username: Desired username (min 3 characters).
            password: Desired password (min 6 characters).
            email: Email address (must be real, not temp email).

        Returns:
            True if registration successful, False otherwise.

        Raises:
            UsernameTakenError: If username is already taken.
            EmailTakenError: If email is already registered.
            PasswordTooShortError: If password is too short.
            UsernameTooShortError: If username is too short.
            InvalidEmailError: If email is invalid or blacklisted.
        """
        data = {
            "userName": username,
            "password": password,
            "email": email,
        }
        response = await self._request("accounts/registerGJAccount.php", data, Secrets.ACCOUNT)
        if response.startswith("-"):
            self._handle_error(response)
            return False
        return response == "1"

    async def get_user(self, account_id: int) -> User:
        """Get a user by their account ID.

        Args:
            account_id: The account ID of the user.

        Returns:
            User object with profile information.

        Raises:
            NotFoundError: If user is not found.
            InvalidRequestError: If rate limited.
        """
        data = {"targetAccountID": str(account_id)}
        response = await self._request("getGJUserInfo20.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return User.model_validate(parsed)

    async def search_users(self, query: str, limit: int = 10) -> list[User]:
        """Search for users by name.

        Args:
            query: Search query (username or partial match).
            limit: Maximum number of results to return.

        Returns:
            List of User objects matching the query.
        """
        data = {"str": query, "total": str(limit), "page": "0"}
        response = await self._request("getGJUsers20.php", data)
        if response.startswith("-"):
            return []
        user_data = parse_response(response.split("#")[0])
        return [User.model_validate(user_data)]

    async def get_level(self, level_id: int) -> Level:
        """Get a level by its ID.

        Args:
            level_id: The ID of the level.

        Returns:
            Level object with level information.

        Raises:
            NotFoundError: If level is not found.
            InvalidRequestError: If rate limited.
        """
        data = {"levelID": str(level_id)}
        response = await self._request("downloadGJLevel22.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response.split("#")[0])
        return Level.model_validate(parsed)

    async def search_levels(self, query: str = "", limit: int = 10, page: int = 0) -> list[Level]:
        """Search for levels by name.

        Args:
            query: Search query (level name or partial match).
            limit: Maximum number of results per page.
            page: Page number for pagination.

        Returns:
            List of Level objects matching the query.
        """
        data = {"str": query, "total": str(limit), "page": str(page), "type": "0"}
        response = await self._request("getGJLevels21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        levels_data = parse_list_response(parts[0])
        return [Level.model_validate(level) for level in levels_data]

    async def get_song(self, song_id: int) -> Song:
        """Get a custom song by its ID.

        Args:
            song_id: The ID of the song.

        Returns:
            Song object with song information.

        Raises:
            NotFoundError: If song is not found.
            InvalidRequestError: If rate limited.
        """
        data = {"songID": str(song_id)}
        response = await self._request("getGJSongInfo.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return Song.model_validate(parsed)

    async def get_level_comments(
        self, level_id: int, limit: int = 10, page: int = 0
    ) -> list[Comment]:
        """Get comments for a level.

        Args:
            level_id: The ID of the level.
            limit: Maximum number of comments to return.
            page: Page number for pagination.

        Returns:
            List of Comment objects.
        """
        data = {
            "levelID": str(level_id),
            "total": str(limit),
            "page": str(page),
            "mode": "0",
        }
        response = await self._request("getGJComments21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        comments = []
        for comment_str in parts[0].split("|"):
            if not comment_str:
                continue
            comment_parts = comment_str.split(":")
            comment_data = parse_response(comment_parts[0])
            if len(comment_parts) > 1:
                user_data = parse_response(comment_parts[1])
                comment_data["username"] = user_data.get("1", "")
            comments.append(Comment.model_validate(comment_data))
        return comments

    async def get_leaderboard(self, limit: int = 100, type: str = "top") -> list[LeaderboardScore]:
        """Get the leaderboard.

        Args:
            limit: Maximum number of results (max 100).
            type: Leaderboard type - "top" or "creators".

        Returns:
            List of LeaderboardScore objects.
        """
        type_value = "creators" if type == "creators" else "top"
        data = {"type": type_value, "count": str(min(limit, 100))}
        response = await self._request("getGJScores20.php", data)
        if response.startswith("-"):
            return []
        entries_data = parse_list_response(response)
        return [LeaderboardScore.model_validate(e) for e in entries_data]

    async def get_user_levels(self, user_id: int, limit: int = 10, page: int = 0) -> list[Level]:
        """Get levels created by a user.

        Args:
            user_id: The user's ID (not account ID).
            limit: Maximum number of levels to return.
            page: Page number for pagination.

        Returns:
            List of Level objects created by the user.
        """
        data = {
            "str": str(user_id),
            "total": str(limit),
            "page": str(page),
            "type": "5",
        }
        response = await self._request("getGJLevels21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        levels_data = parse_list_response(parts[0])
        return [Level.model_validate(level) for level in levels_data]

    async def get_daily_level(self, type: str = "daily") -> DailyLevel:
        """Get the current daily/weekly level info.

        Args:
            type: "daily", "weekly", or "event".

        Returns:
            DailyLevel object with index and time_left.
        """
        type_map = {"daily": "0", "weekly": "1", "event": "2"}
        data = {"type": type_map.get(type, "0")}
        response = await self._request("getGJDailyLevel.php", data)
        if response.startswith("-"):
            return DailyLevel()
        parts = response.split("|")
        if len(parts) >= 2:
            return DailyLevel(index=int(parts[0]), time_left=int(parts[1]))
        return DailyLevel()

    async def get_gauntlets(self) -> list[Gauntlet]:
        """Get all gauntlets.

        Returns:
            List of Gauntlet objects.
        """
        data = {"special": "1"}
        response = await self._request("getGJGauntlets21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        gauntlets_data = parse_list_response(parts[0])
        return [Gauntlet.model_validate(g) for g in gauntlets_data]

    async def get_map_packs(self, page: int = 0) -> list[MapPack]:
        """Get map packs.

        Args:
            page: Page number for pagination.

        Returns:
            List of MapPack objects.
        """
        data = {"page": str(page)}
        response = await self._request("getGJMapPacks21.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        packs_data = parse_list_response(parts[0])
        return [MapPack.model_validate(p) for p in packs_data]

    async def get_top_artists(self, page: int = 0) -> list[TopArtist]:
        """Get RobTop's handpicked top artists.

        Args:
            page: Page number for pagination.

        Returns:
            List of TopArtist objects.
        """
        data = {"page": str(page)}
        response = await self._request("getGJTopArtists.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        artists_data = parse_list_response(parts[0])
        return [TopArtist.model_validate(a) for a in artists_data]

    async def get_account_comments(
        self, account_id: int, limit: int = 10, page: int = 0
    ) -> list[Comment]:
        """Get comments on a user's profile.

        Args:
            account_id: The account ID of the user.
            limit: Maximum number of comments to return.
            page: Page number for pagination.

        Returns:
            List of Comment objects.
        """
        data = {
            "accountID": str(account_id),
            "total": str(limit),
            "page": str(page),
        }
        response = await self._request("getGJAccountComments20.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        comments_data = parse_list_response(parts[0])
        return [Comment.model_validate(c) for c in comments_data]

    async def get_comment_history(
        self, user_id: int, limit: int = 10, page: int = 0, mode: str = "recent"
    ) -> list[Comment]:
        """Get a user's comment history (comments they've posted on levels).

        Args:
            user_id: The user's ID (not account ID).
            limit: Maximum number of comments to return.
            page: Page number for pagination.
            mode: "recent" or "liked".

        Returns:
            List of Comment objects.
        """
        mode_value = "1" if mode == "liked" else "0"
        data = {
            "userID": str(user_id),
            "total": str(limit),
            "page": str(page),
            "mode": mode_value,
        }
        response = await self._request("getGJCommentHistory.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        comments = []
        for comment_str in parts[0].split("|"):
            if not comment_str:
                continue
            comment_parts = comment_str.split(":")
            comment_data = parse_response(comment_parts[0])
            if len(comment_parts) > 1:
                user_data = parse_response(comment_parts[1])
                comment_data["username"] = user_data.get("1", "")
                comments.append(Comment.model_validate(comment_data))
        return comments

    async def get_messages(
        self, limit: int = 10, page: int = 0, sent: bool = False
    ) -> list[Message]:
        """Get inbox or sent messages. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get messages")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "page": str(page),
            "total": str(limit),
            "getSent": "1" if sent else "0",
        }
        response = await self._request("getGJMessages20.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        messages_data = parse_list_response(parts[0])
        return [Message.model_validate(m) for m in messages_data]

    async def get_message(self, message_id: int) -> Message:
        """Download full message content. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get message")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "messageID": str(message_id),
        }
        response = await self._request("downloadGJMessage20.php", data)
        if response.startswith("-"):
            self._handle_error(response)
        parsed = parse_response(response)
        return Message.model_validate(parsed)

    async def send_message(self, recipient_id: int, subject: str, body: str) -> bool:
        """Send a private message. Requires authentication."""
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to send message")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "toAccountID": str(recipient_id),
            "subject": base64.b64encode(subject.encode()).decode(),
            "body": base64.b64encode(body.encode()).decode(),
        }
        response = await self._request("uploadGJMessage20.php", data)
        return response != "-1"

    async def delete_message(self, message_id: int) -> bool:
        """Delete a message. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete message")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "messageID": str(message_id),
        }
        response = await self._request("deleteGJMessages20.php", data)
        return response == "1"

    async def get_friend_requests(
        self, limit: int = 10, page: int = 0, sent: bool = False
    ) -> list[FriendRequest]:
        """Get friend requests. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get friend requests")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "page": str(page),
            "total": str(limit),
            "getSent": "1" if sent else "0",
        }
        response = await self._request("getGJFriendRequests20.php", data)
        if response.startswith("-"):
            return []
        parts = response.split("#")
        if not parts:
            return []
        requests_data = parse_list_response(parts[0])
        return [FriendRequest.model_validate(r) for r in requests_data]

    async def send_friend_request(self, recipient_id: int, message: str = "") -> bool:
        """Send a friend request. Requires authentication."""
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to send friend request")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "toAccountID": str(recipient_id),
            "comment": base64.b64encode(message.encode()).decode() if message else "",
        }
        response = await self._request("uploadFriendRequest20.php", data)
        return response != "-1"

    async def accept_friend_request(self, request_id: int) -> bool:
        """Accept a friend request. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to accept friend request")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "requestID": str(request_id),
        }
        response = await self._request("acceptGJFriendRequest20.php", data)
        return response == "1"

    async def delete_friend_request(self, request_id: int) -> bool:
        """Delete a friend request. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete friend request")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "requestID": str(request_id),
        }
        response = await self._request("deleteGJFriendRequests20.php", data)
        return response == "1"

    async def get_friends(self) -> list[User]:
        """Get friends list. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get friends")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "type": "0",
        }
        response = await self._request("getGJUserList20.php", data)
        if response.startswith("-"):
            return []
        users_data = parse_list_response(response)
        return [User.model_validate(u) for u in users_data]

    async def remove_friend(self, friend_id: int) -> bool:
        """Remove a friend. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to remove friend")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "targetAccountID": str(friend_id),
        }
        response = await self._request("removeGJFriend20.php", data)
        return response == "1"

    async def block_user(self, user_id: int) -> bool:
        """Block a user. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to block user")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "targetAccountID": str(user_id),
        }
        response = await self._request("blockGJUser20.php", data)
        return response == "1"

    async def unblock_user(self, user_id: int) -> bool:
        """Unblock a user. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to unblock user")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "targetAccountID": str(user_id),
        }
        response = await self._request("unblockGJUser20.php", data)
        return response == "1"

    async def get_blocked_users(self) -> list[User]:
        """Get blocked users list. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to get blocked users")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "type": "1",
        }
        response = await self._request("getGJUserList20.php", data)
        if response.startswith("-"):
            return []
        users_data = parse_list_response(response)
        return [User.model_validate(u) for u in users_data]

    async def like_level(self, level_id: int, like: bool = True) -> bool:
        """Like or dislike a level."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to like levels")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "itemID": str(level_id),
            "type": "1",
            "like": "1" if like else "0",
        }
        response = await self._request("likeGJItem211.php", data)
        return response == "1"

    async def like_comment(self, comment_id: int, like: bool = True) -> bool:
        """Like or dislike a level comment."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to like comments")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "itemID": str(comment_id),
            "type": "2",
            "like": "1" if like else "0",
        }
        response = await self._request("likeGJItem211.php", data)
        return response == "1"

    async def post_level_comment(self, level_id: int, content: str, percent: int = 0) -> int | None:
        """Post a comment on a level. Requires authentication."""
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to post comment")
        encoded_content = base64.b64encode(content.encode()).decode()
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "userName": self._username,
            "comment": encoded_content,
            "levelID": str(level_id),
            "percent": str(percent),
        }
        response = await self._request("uploadGJComment21.php", data)
        if response.startswith("-"):
            return None
        return int(response) if response.isdigit() else None

    async def delete_level_comment(self, comment_id: int, level_id: int) -> bool:
        """Delete a level comment. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete comment")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "commentID": str(comment_id),
            "levelID": str(level_id),
        }
        response = await self._request("deleteGJComment20.php", data)
        return response == "1"

    async def post_profile_comment(self, content: str) -> int | None:
        """Post a comment on your profile. Requires authentication."""
        import base64

        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to post profile comment")
        encoded_content = base64.b64encode(content.encode()).decode()
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "userName": self._username,
            "comment": encoded_content,
        }
        response = await self._request("uploadGJAccComment20.php", data)
        if response.startswith("-"):
            return None
        return int(response) if response.isdigit() else None

    async def delete_profile_comment(self, comment_id: int) -> bool:
        """Delete a profile comment. Requires authentication."""
        if not self.is_authenticated:
            raise RuntimeError("Must be authenticated to delete profile comment")
        data = {
            "accountID": str(self._account_id),
            "gjp2": generate_gjp2(self._password),
            "commentID": str(comment_id),
        }
        response = await self._request("deleteGJAccComment20.php", data)
        return response == "1"
