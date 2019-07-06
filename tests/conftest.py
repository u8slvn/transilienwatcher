#!/usr/bin/env python3
# coding: utf-8

import pytest

from rerwatcher.app import RerWatcher

FAKE_CONFIG = {
    "api": {
        "url": 'https://test.url/${departure_station}/depart/${arrival_station}',
        "departure_station": 123,
        "arrival_station": 321,
        "user": 'user',
        "password": 'password',
        "date_format": '%d/%m/%Y %H:%M',
        "encoding": 'utf-8',
    },
    "refresh_time": {
        "default": 10,
        "step": 10,
        "max": 30,
    },
    "device": {
        "type": 'console',
    },
}


@pytest.fixture(scope="function")
def mock_config(monkeypatch):
    load_config = lambda: FAKE_CONFIG
    monkeypatch.setattr(RerWatcher, "load_config", load_config)
