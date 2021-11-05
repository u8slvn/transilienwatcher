import pytest

from transilienwatcher.display import (
    Console,
    DisplayBuilder,
    LCD,
    UnknownDisplayTypeError,
    LCDI2C,
)


class TestLCDDisplay:
    def test_print_on_lcd(self, mocker):
        digital_in_out = mocker.patch("transilienwatcher.display.DigitalInOut")
        char_lcd = mocker.patch("transilienwatcher.display.Character_LCD_Mono")
        messages = ["foo", "bar"]
        lcd = LCD(columns=16, rows=2)

        lcd.print(messages)

        assert 7 == digital_in_out.call_count
        char_lcd.assert_called_once()
        assert char_lcd().backlight is True
        char_lcd().clear.assert_called_once()
        assert char_lcd().message == "foo\nbar"


class TestLCDI2CDisplay:
    def test_print_on_lcd_i2c(self, mocker):
        char_lcd = mocker.patch("transilienwatcher.display.Character_LCD_I2C")
        messages = ["foo", "bar"]
        lcd = LCDI2C(columns=16, rows=2)

        lcd.print(messages)

        char_lcd.assert_called_once()
        assert char_lcd().backlight is True
        char_lcd().clear.assert_called_once()
        assert char_lcd().message == "foo\nbar"


class TestConsoleDisplay:
    def test_print_on_console(self, capsys):
        messages = ["TEST: 12min"]
        console = Console()

        console.print(messages)

        captured = capsys.readouterr()
        assert "TEST: 12min\n" == captured.out


class TestDisplayFactory:
    def test_display_builder_console(self, config):
        display = DisplayBuilder.build(config["display"])

        assert isinstance(display, Console)

    def test_display_builder_lcd(self, mocker, config):
        mocker.patch("transilienwatcher.display.DigitalInOut")
        mocker.patch("transilienwatcher.display.Character_LCD_Mono")
        config["display"]["type"] = "lcd"

        display = DisplayBuilder.build(config["display"])

        assert isinstance(display, LCD)

    def test_display_builder_lcd_i2c(self, mocker, config):
        mocker.patch("transilienwatcher.display.Character_LCD_I2C")
        config["display"]["type"] = "lcd_i2c"

        display = DisplayBuilder.build(config["display"])

        assert isinstance(display, LCDI2C)

    def test_display_builder_fail(self, config):
        config["display"]["type"] = "foo"

        with pytest.raises(UnknownDisplayTypeError):
            DisplayBuilder.build(config["display"])
