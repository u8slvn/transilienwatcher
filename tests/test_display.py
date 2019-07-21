#!/usr/bin/env python3
# coding: utf-8

import pytest

from rerwatcher import display
from rerwatcher.formatter import TimeTable
from tests.conftest import CONFIG


class TestLCDDisplay:
    def test_print_on_lcd(self, mocker):
        lcd = mocker.patch('rerwatcher.display.CharLCD')
        messages = [mocker.Mock(**{'text.return_value': 'foo'})]
        matrix = display.LCD()

        matrix.print(messages)

        assert (1, 0) == lcd().cursor_pos
        lcd().write_string.assert_called_once_with('foo')


class TestConsoleDisplay:
    def test_print_on_console(self, capsys):
        messages = [TimeTable(miss='TEST', time='12min')]
        console = display.Console()

        console.print(messages)

        captured = capsys.readouterr()
        assert 'TEST: 12min\n' == captured.out


class TestDisplayDeviceFactory:
    def test_device_builder_console_display(self):
        CONFIG['device']['type'] = 'console'

        device = display.DisplayDeviceFactory.build(CONFIG['device'])

        assert isinstance(device, display.Console)

    def test_device_builder_matrix_display(self, mocker):
        mocker.patch('rerwatcher.display.CharLCD')
        CONFIG['device']['type'] = 'lcd'

        device = display.DisplayDeviceFactory.build(CONFIG['device'])

        assert isinstance(device, display.LCD)

    def test_device_builder_fail(self):
        CONFIG['device']['type'] = 'foo'

        with pytest.raises(display.DisplayTypeNotSupportedError):
            display.DisplayDeviceFactory.build(CONFIG['device'])
