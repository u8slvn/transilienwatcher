import functools

from loguru import logger
from requests import RequestException, ReadTimeout


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
        except (RequestException, ReadTimeout):
            logger.error("Request failed.")
            raise RequestError("HTTP: unknown error")

    return wrapper


def format_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error("Format failed.")
            raise FormatError("FORMAT: unknown error")

    return wrapper


def fetch_data_error_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (RequestError, FormatError) as error:
            return [str(error)]
        except Exception:
            raise

    return wrapper
