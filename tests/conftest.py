import builtins
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
import requests
from loguru import logger

# Monkeypatch for non Raspberry pi environment.
sys.modules["board"] = Mock()

logger.disable("transilienwatcher")

CONFIG = {
    "transilien": {
        "stations": {
            "departure": "00000000",
            "arrival": None,
        },
        "credentials": {
            "username": "username",
            "password": "password",
        },
    },
    "refresh_time": 10,
    "display": {
        "type": "console",
        "lcd": {
            "columns": 16,
            "rows": 2,
        },
        "lcd_i2c": {
            "columns": 16,
            "rows": 2,
            "address": 0x20,
        },
    },
}


@pytest.fixture(scope="module")
def config():
    return CONFIG


@pytest.fixture(scope="function")
def requests_fixture():
    with open("tests/fixture.xml") as file:
        return file.read()


@pytest.fixture(scope="function")
def requests_fixture_status():
    with open("tests/fixture_with_status.xml") as file:
        return file.read()


@pytest.fixture(scope="function")
def mock_requests(monkeypatch, requests_fixture):
    def get():
        return requests_fixture

    monkeypatch.setattr(requests, "get", get)


@pytest.fixture
def cleanup_files(monkeypatch):
    def open_wrapper(open_func, files):
        def open_patched(path, mode="r", *args, **kwargs):
            if mode in ["w", "x"] and not Path(path).is_file():
                files.append(path)
            return open_func(path, mode=mode, *args, **kwargs)

        return open_patched

    files = []
    monkeypatch.setattr(builtins, "open", open_wrapper(builtins.open, files))
    yield
    for file in files:
        Path(file).unlink()
