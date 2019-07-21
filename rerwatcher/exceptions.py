import functools

from loguru import logger
from requests import RequestException, ReadTimeout, HTTPError


class TransilienError(Exception):
    pass


class RequestError(TransilienError):
    pass


class FormatError(TransilienError):
    pass


def request_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except HTTPError as err:
            logger.error("Request failed.")
            status = err.response.status_code if err.response else "unknown"
            raise RequestError(f"HTTP: {status} error")
        except (RequestException, ReadTimeout):
            logger.error("Request failed.")
            raise RequestError(f"HTTP: unknown Error")

    return wrapper


def format_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error("Format failed.")
            raise FormatError(f"FORMAT: error")

    return wrapper
