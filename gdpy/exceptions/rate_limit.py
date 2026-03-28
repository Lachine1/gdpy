from gdpy.exceptions.base import RequestError


class RateLimitError(RequestError):
    error_code = -1
