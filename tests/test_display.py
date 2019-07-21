import pytest

from rerwatcher.display import (LCD, Console, DisplayDeviceFactory,
                                DisplayTypeNotSupportedError)


class TestLCDDisplay:
    def test_print_on_lcd(self, mocker):
        charlcd = mocker.patch('rerwatcher.display.CharLCD')
        messages = ['foo']
        lcd = LCD()

        lcd.print(messages)

        assert (1, 0) == charlcd().cursor_pos
        charlcd().write_string.assert_called_once_with('foo')


class TestConsoleDisplay:
    def test_print_on_console(self, capsys):
        messages = ['TEST: 12min']
        console = Console()

        console.print(messages)

        captured = capsys.readouterr()
        assert 'TEST: 12min\n' == captured.out


class TestDisplayDeviceFactory:
    def test_device_builder_console_display(self, config):
        device = DisplayDeviceFactory.build(config['device'])

        assert isinstance(device, Console)

    def test_device_builder_matrix_display(self, mocker, config):
        mocker.patch('rerwatcher.display.CharLCD')
        config['device']['type'] = 'lcd'

        device = DisplayDeviceFactory.build(config['device'])

        assert isinstance(device, LCD)

    def test_device_builder_fail(self, config):
        config['device']['type'] = 'foo'

        with pytest.raises(DisplayTypeNotSupportedError):
            DisplayDeviceFactory.build(config['device'])
