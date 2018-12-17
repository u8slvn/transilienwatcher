#!/usr/bin/env python3
# coding: utf-8

import pytest
from unittest.mock import patch, Mock
from .context import display
from . import FAKE_CONFIG


class TestConsoleDisplay:
    @patch('builtins.print')
    def test_print_on_console(self, print_mock):
        # GIVEN
        message = Mock()
        message.text.return_value = 'FOO'
        messages = [message]
        console_display = display.ConsoleDisplay()

        # WHEN
        console_display.print(messages)

        # THEN
        print_mock.assert_called_with('FOO')


class TestDisplayDeviceFactory:
    @patch('rerwatcher.display.ConsoleDisplay')
    def test_device_builder_console_display(self, console_display_mock):
        # GIVEN
        FAKE_CONFIG['device']['type'] = 'console'
        console_display_mock.return_value = 'FOO-CONSOLE'

        # WHEN
        device = display.DisplayDeviceFactory.build(FAKE_CONFIG)

        # THEN
        assert device == 'FOO-CONSOLE'

    @patch('rerwatcher.display.MatrixDisplay')
    def test_device_builder_matrix_display(self, matrix_display_mock):
        # GIVEN
        FAKE_CONFIG['device']['type'] = 'matrix'
        matrix_display_mock.return_value = 'FOO-MATRIX'

        # WHEN
        device = display.DisplayDeviceFactory.build(FAKE_CONFIG)

        # THEN
        assert device == 'FOO-MATRIX'

    def test_device_builder_fail(self):
        # GIVEN
        FAKE_CONFIG['device']['type'] = 'foo'

        # WHEN
        with pytest.raises(display.DiplayTypeNotStupported) as error:
            display.DisplayDeviceFactory.build(FAKE_CONFIG)

        assert error.typename == 'DiplayTypeNotStupported'
