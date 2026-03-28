# Exceptions

Exception hierarchy for handling errors.

## Base Exceptions

::: gdpy.exceptions.base.GDError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.base.RequestError
    handlers:
      python:
        docstring_style: google

## Authentication Errors

::: gdpy.exceptions.auth.AuthError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.auth.InvalidCredentialsError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.auth.AccountDisabledError
    handlers:
      python:
        docstring_style: google

## Request Errors

::: gdpy.exceptions.invalid_request.InvalidRequestError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.not_found.NotFoundError
    handlers:
      python:
        docstring_style: google

## Registration Errors

::: gdpy.exceptions.registration.RegistrationError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.registration.UsernameTakenError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.registration.EmailTakenError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.registration.PasswordTooShortError
    handlers:
      python:
        docstring_style: google

::: gdpy.exceptions.registration.UsernameTooShortError
    handlers:
      python:
        docstring_style: google

## Validation Errors

::: gdpy.exceptions.validation.ValidationError
    handlers:
      python:
        docstring_style: google
