from gdpy.exceptions.base import RequestError


class AuthError(RequestError):
    pass


class InvalidCredentialsError(AuthError):
    error_code = -11


class AccountDisabledError(AuthError):
    error_code = -12
