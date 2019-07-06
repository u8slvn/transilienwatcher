from datetime import timedelta

import pytest
from freezegun import freeze_time

from rerwatcher.formatter import (TimeTable, format_timedelta,
                                  calculate_time_delta_with_now,
                                  TransilienApiFormatter)
from tests.conftest import FAKE_CONFIG, FAKE_RESPONSE


def test_timetable_text():
    timetable = TimeTable('FOO', 'BAR')

    message = timetable.text()

    assert message == 'FOO: BAR'


@pytest.mark.parametrize("given,expected", [
    (timedelta(seconds=40), '1min',),
    (timedelta(seconds=120), '2min',),
    (timedelta(seconds=7400), '2h',),
])
def test_format_timedelta(given, expected):
    assert format_timedelta(given) == expected


@freeze_time("27-10-2018 13:30")
def test_calculate_time_delta_with_now():
    date_str = '27/10/2018 13:32'

    time_delta = calculate_time_delta_with_now(
        date=date_str,
        date_format=TransilienApiFormatter.date_format
    )

    assert time_delta == timedelta(seconds=120)

@freeze_time("27-10-2018 13:30")
def test_transilien_api_formatter():
    formatter = TransilienApiFormatter()

    result = formatter.format_response(FAKE_RESPONSE)

    assert result[0].miss == 'DACA'
    assert result[0].time == '8h'
    assert result[1].miss == 'FACA'
    assert result[1].time == '9h'
