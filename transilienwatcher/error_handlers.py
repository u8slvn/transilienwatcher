import functools

from loguru import logger
from requests import RequestException, ReadTimeout

from transilienwatcher.exceptions import FormatError, RequestError, \
    TransilienError


def request_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (RequestException, ReadTimeout):
            logger.error("Request failed.")
            raise RequestError("HTTP: unknown error")

    return wrapper


def format_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            logger.error("Format failed.")
            raise FormatError("FORMAT: unknown error")

    return wrapper


def fetch_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TransilienError as error:
            return [str(error)]
        except Exception:
            raise

    return wrapper
