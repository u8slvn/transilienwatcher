import pytest
import requests
from loguru import logger

from rerwatcher.app import RerWatcher

logger.disable('rerwatcher')

CONFIG = {
    'transilien': {
        'url': 'https://test.url/00000000/d/00000000',
        'username': 'username',
        'password': 'password',
    },
    'refresh_time': 10,
    'display': {
        'type': 'console',
    },
}


@pytest.fixture(scope='module')
def config():
    return CONFIG


@pytest.fixture(scope='function')
def mock_config(monkeypatch):
    def load_config():
        return CONFIG

    monkeypatch.setattr(RerWatcher, 'load_config', load_config)


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
