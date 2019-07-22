import pytest

from rerwatcher.display import (LCD, Console, DisplayBuilder,
                                UnknownDisplayTypeError)


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


class TestDisplayFactory:
    def test_display_builder_console(self, config):
        display = DisplayBuilder.build(config['display'])

        assert isinstance(display, Console)

    def test_display_builder_lcd(self, mocker, config):
        mocker.patch('rerwatcher.display.CharLCD')
        config['display']['type'] = 'lcd'

        display = DisplayBuilder.build(config['display'])

        assert isinstance(display, LCD)

    def test_display_builder_fail(self, config):
        config['display']['type'] = 'foo'

        with pytest.raises(UnknownDisplayTypeError):
            DisplayBuilder.build(config['display'])
