#!/usr/bin/env python3
# coding: utf-8

import pytest


@pytest.fixture(scope="module")
def fake_config():
    return {
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
