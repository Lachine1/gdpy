"""Base exception classes for gdpy.

All exceptions in gdpy inherit from GDError, making it easy to catch
any gdpy-related exception with a single except clause.
"""


class GDError(Exception):
    """Base exception for all gdpy errors.

    All exceptions in gdpy inherit from this class, allowing you to
    catch any gdpy-related error with a single except clause.

    Example:
        ```python
        try:
            user = await client.get_user(account_id=999999)
        except GDError as e:
            print(f"gdpy error: {e}")
        ```
    """

    pass


class RequestError(GDError):
    """Base exception for request-related errors.

    This is the parent class for errors that occur during API requests,
    including authentication errors, rate limiting, and not found errors.
    """

    pass
