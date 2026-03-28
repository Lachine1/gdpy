import pytest
from gdpy.exceptions import (
    GDError,
    RequestError,
    AuthError,
    InvalidCredentialsError,
    AccountDisabledError,
    RateLimitError,
    NotFoundError,
    RegistrationError,
    UsernameTakenError,
    EmailTakenError,
    PasswordTooShortError,
    UsernameTooShortError,
)


class TestExceptions:
    def test_exception_hierarchy(self):
        assert issubclass(RequestError, GDError)
        assert issubclass(AuthError, RequestError)
        assert issubclass(InvalidCredentialsError, AuthError)
        assert issubclass(AccountDisabledError, AuthError)
        assert issubclass(RateLimitError, RequestError)
        assert issubclass(NotFoundError, RequestError)
        assert issubclass(RegistrationError, GDError)
        assert issubclass(UsernameTakenError, RegistrationError)
        assert issubclass(EmailTakenError, RegistrationError)

    def test_error_codes(self):
        assert InvalidCredentialsError.error_code == -11
        assert AccountDisabledError.error_code == -12
        assert RateLimitError.error_code == -1
        assert UsernameTakenError.error_code == -2
        assert EmailTakenError.error_code == -3
        assert PasswordTooShortError.error_code == -8
        assert UsernameTooShortError.error_code == -9

    def test_raise_exceptions(self):
        with pytest.raises(InvalidCredentialsError):
            raise InvalidCredentialsError("test")

        with pytest.raises(RateLimitError):
            raise RateLimitError("test")
