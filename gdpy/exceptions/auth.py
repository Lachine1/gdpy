"""Authentication-related exceptions.

These exceptions are raised when authentication operations fail,
such as login or registration errors.
"""

from gdpy.exceptions.base import RequestError


class AuthError(RequestError):
    """Base exception for authentication errors.
    
    Raised when authentication-related operations fail.
    """

    pass


class InvalidCredentialsError(AuthError):
    """Raised when login credentials are incorrect.
    
    This exception is raised when attempting to login with
    an invalid username or password combination.
    
    Attributes:
        error_code: The API error code (-11).
    """

    error_code = -11


class AccountDisabledError(AuthError):
    """Raised when the account has been disabled.
    
    This exception is raised when attempting to login to
    an account that has been banned or disabled by moderators.
    
    Attributes:
        error_code: The API error code (-12).
    """

    error_code = -12
