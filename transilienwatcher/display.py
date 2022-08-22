from abc import ABC, abstractmethod


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
        from RPLCD.gpio import CharLCD
        from RPi import GPIO

        self._lcd = CharLCD(
            pin_rs=15,
            pin_rw=18,
            pin_e=16,
            pins_data=[21, 22, 23, 24],
            numbering_mode=GPIO.BOARD,
        )

    def print(self, messages: list):
        self._lcd.clear()
        self._lcd.write_string("\n".join(messages))


class LCDI2C(LCD):
    def __init__(self, columns: int, rows: int, address: int):
        from RPLCD.i2c import CharLCD

        self._lcd = CharLCD(
            i2c_expander="PCF8574",
            cols=columns,
            rows=4,
            address=address,
            backlight_enabled=True,
        )


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
