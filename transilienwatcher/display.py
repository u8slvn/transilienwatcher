from abc import ABC, abstractmethod

from adafruit_character_lcd.character_lcd import Character_LCD_Mono
from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C
from digitalio import DigitalInOut


class UnknownDisplayTypeError(NotImplementedError):
    pass


class Display(ABC):
    @abstractmethod
    def print(self, messages: list):
        raise NotImplementedError


class Console(Display):
    def print(self, messages: list):
        for message in messages:
            print(message)


class LCD(Display):
    def __init__(self, columns: int, rows: int):
        import board

        rs = DigitalInOut(board.D7)
        en = DigitalInOut(board.D8)
        d4 = DigitalInOut(board.D9)
        d5 = DigitalInOut(board.D10)
        d6 = DigitalInOut(board.D11)
        d7 = DigitalInOut(board.D12)
        backlight = DigitalInOut(board.D13)

        self._lcd = Character_LCD_Mono(
            rs=rs,
            en=en,
            db4=d4,
            db5=d5,
            db6=d6,
            db7=d7,
            columns=columns,
            lines=rows,
            backlight_pin=backlight,
        )
        self._lcd.backlight = True

    def print(self, messages: list):
        self._lcd.clear()
        self._lcd.message = "\n".join(messages)


class LCDI2C(LCD):
    def __init__(self, columns: int, rows: int, address: int = 0x20):
        import board

        i2c = board.I2C()
        self._lcd = Character_LCD_I2C(
            i2c=i2c, columns=columns, lines=rows, address=address
        )
        self._lcd.backlight = True


class DisplayBuilder(ABC):
    @staticmethod
    def build(config: dict):
        display = {
            "lcd_i2c": lambda: LCDI2C(**config["lcd_i2c"]),
            "lcd": lambda: LCD(**config["lcd"]),
            "console": lambda: Console(),
        }.get(config["type"])

        if not display:
            raise UnknownDisplayTypeError

        return display()
