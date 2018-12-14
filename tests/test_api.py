#!/usr/bin/env python3
# coding: utf-8

from datetime import timedelta

from unittest.mock import patch, Mock
import pytest
from freezegun import freeze_time
from rerwatcher import api


class TestTransilienApiDriver:
    def setup(self):
        self.api_driver = api.TransilienApi(Mock())
        self.api_driver._date_format = '%d/%m/%Y %H:%M'
        self.api_driver._encoding = 'utf-8'

    @pytest.mark.parametrize("given,expected", [
        (timedelta(seconds=40), '1min',),
        (timedelta(seconds=120), '2min',),
        (timedelta(seconds=7400), '2h',),
    ])
    def test_timedelta_formatter(self, given, expected):
        assert self.api_driver._timedelta_formatter(given) == expected

    @freeze_time("27-10-2018 13:30")
    def test_convert_date_to_time(self):
        # GIVEN
        api_driver = self.api_driver
        api_driver._timedelta_formatter = Mock(return_value='2min')
        date_str = '27/10/2018 13:32'

        # WHEN
        time = api_driver._convert_date_to_time(date_str=date_str)

        # THEN
        assert time == '2min'
        api_driver._timedelta_formatter.assert_called_once_with(
            timedelta(seconds=120))

    @patch('rerwatcher.api.TimeTable')
    @patch('rerwatcher.api.etree')
    def test_extract_timetables_should_return_two_elements(
            self,
            etree_mock,
            timetable_mock
    ):
        # GIVEN
        api_driver = self.api_driver
        api_driver._convert_date_to_time = Mock()
        tree_mock = Mock()
        tree_mock.xpath.return_value = [Mock(), Mock()]
        etree_mock.fromstring.return_value = tree_mock
        timetable_mock.side_effect = ['FOO', 'BAR']

        # WHEN
        result_list = api_driver._get_timetables(Mock())

        # THEN
        assert result_list == ['FOO', 'BAR']
        assert len(api_driver._convert_date_to_time.call_args_list) is 2


class TestTimeTable:
    def test_text(self):
        # GIVEN
        timetable = api.TimeTable('FOO', 'BAR')

        # WHEN
        message = timetable.text()

        # THEN
        assert message == 'FOO: BAR'
