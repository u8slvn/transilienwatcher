#!/usr/bin/env python3
# coding: utf-8

import pytest
from unittest.mock import patch, Mock
from rerwatcher import display


class TestConsoleDisplay:
    @patch('builtins.print')
    def test_print_on_console(self, print_mock):
        # GIVEN
        message = Mock()
        message.text.return_value = 'FOO'
        messages = [message]
        console_display = display.ConsoleDisplay()

        # WHEN
        console_display.display(messages)

        # THEN
        print_mock.assert_called_with('FOO')


class TestDisplayDeviceFactory:
    @patch('rerwatcher.display.ConsoleDisplay')
    def test_device_builder_console_display(self, console_display_mock):
        # GIVEN
        config_console = Mock()
        config_console.get.return_value = 'console'
        console_display_mock.return_value = 'FOO-CONSOLE'

        # WHEN
        device = display.DisplayDeviceFactory.build(config_console)

        # THEN
        assert device == 'FOO-CONSOLE'

    @patch('rerwatcher.display.MatrixDisplay')
    def test_device_builder_matrix_display(self, matrix_display_mock):
        # GIVEN
        config_matrix = Mock()
        config_matrix.get.return_value = 'matrix'
        matrix_display_mock.return_value = 'FOO-MATRIX'

        # WHEN
        device = display.DisplayDeviceFactory.build(config_matrix)

        # THEN
        assert device == 'FOO-MATRIX'

    def test_device_builder_fail(self):
        # GIVEN
        config_matrix = Mock()
        config_matrix.get.return_value = 'foobar'

        # WHEN
        with pytest.raises(NotImplementedError) as error:
            display.DisplayDeviceFactory.build(config_matrix)

        assert error.typename == 'NotImplementedError'
