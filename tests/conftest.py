import sys
from unittest.mock import Mock

from loguru import logger
import pytest
import requests

# Monkeypatch for non Raspberry pi environment.
sys.modules['board'] = Mock()

logger.disable('transilienwatcher')

CONFIG = {
    'transilien': {
        'url': 'https://test.url/00000000/d/00000000',
        'username': 'username',
        'password': 'password',
    },
    'refresh_time': 10,
    'display': {
        'type': 'console',
        'lcd-config': {
            'columns': 16,
            'rows': 2,
        },
    },
}


@pytest.fixture(scope='module')
def config():
    return CONFIG


@pytest.fixture(scope='function')
def requests_fixture():
    with open('tests/fixture.xml') as file:
        return file.read()


@pytest.fixture(scope='function')
def requests_fixture_status():
    with open('tests/fixture_with_status.xml') as file:
        return file.read()


@pytest.fixture(scope='function')
def mock_requests(monkeypatch, requests_fixture):
    def get():
        return requests_fixture

    monkeypatch.setattr(requests, 'get', get)
