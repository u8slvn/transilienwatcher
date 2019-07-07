#!/usr/bin/env python3
# coding: utf-8

import pytest
import requests
from loguru import logger

from rerwatcher.app import RerWatcher

logger.disable('rerwatcher')

FAKE_CONFIG = {
    'api': {
        'url': 'https://test.url/${departure_station}/d/${arrival_station}',
        'departure_station': 123,
        'arrival_station': 321,
        'user': 'user',
        'password': 'password',
    },
    'refresh_time': {
        'default': 10,
        'step': 10,
        'max': 30,
    },
    'device': {
        'type': 'console',
    },
}


@pytest.fixture(scope='function')
def mock_config(monkeypatch):
    def load_config():
        return FAKE_CONFIG
    monkeypatch.setattr(RerWatcher, 'load_config', load_config)


def requests_fixture():
    with open('tests/fixture.xml') as file:
        return file.read()


class MockResponse:
    def __init__(self, text):
        self.text = text


FAKE_RESPONSE = MockResponse(requests_fixture())


@pytest.fixture(scope='function')
def mock_requests(monkeypatch):
    def get():
        return FAKE_RESPONSE
    monkeypatch.setattr(requests, 'get', get)
