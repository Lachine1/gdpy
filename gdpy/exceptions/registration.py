from gdpy.exceptions.base import GDError


class RegistrationError(GDError):
    pass


class UsernameTakenError(RegistrationError):
    error_code = -2


class EmailTakenError(RegistrationError):
    error_code = -3


class PasswordTooShortError(RegistrationError):
    error_code = -8


class UsernameTooShortError(RegistrationError):
    error_code = -9
