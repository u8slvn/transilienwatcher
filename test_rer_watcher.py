#!/usr/bin/env python
# -*- coding: utf-8 -*-

from freezegun import freeze_time
import pytest
import rer_watcher

@freeze_time("27-10-2017 13:31")
@pytest.mark.parametrize("miss,date,expected", [
        ('ROMI', '27/10/2017 13:41', 'ROMI : 10min'),
        ('MONA', '27/10/2017 21:41', 'MONA : 8h'),
    ])
def test_message_formatter(miss, date, expected):
    assert rer_watcher.message_formatter(miss, date) == expected

@pytest.mark.parametrize("is_error,waiting_time,expected", [
        (False, 10, 10),
        (True, 10, 20),
        (True, 20, 30),
        (True, 30, 30),
    ])
def test_manage_waiting_time(is_error, waiting_time, expected):
    rer_watcher.DEFAULT_WAITING_TIME = 10
    rer_watcher.STEP_WAITING_TIME = 10
    rer_watcher.MAX_WAITING_TIME = 30
    assert rer_watcher.manage_waiting_time(is_error, waiting_time) == expected
