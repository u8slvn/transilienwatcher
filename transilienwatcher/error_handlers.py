import functools

from loguru import logger
from requests import ReadTimeout, RequestException

from transilienwatcher.exceptions import FormatError, RequestError, \
    TransilienError


def request_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (RequestException, ReadTimeout) as error:
            logger.error(f"Request failed.\n{error}")
            raise RequestError("ERROR: http")
        except Exception as error:
            logger.error(f"Request failed.\n{error}")
            raise RequestError("ERROR: api")

    return wrapper


def format_data(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            logger.error(f"Format failed.\n{error}")
            raise FormatError("ERROR: format")

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
