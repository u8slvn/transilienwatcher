#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time

from requests.auth import HTTPBasicAuth
from lxml import etree
from datetime import datetime
# from luma.led_matrix.device import max7219
# from luma.core.interface.serial import spi, noop
# from luma.core.render import canvas
# from luma.core.legacy import text
# from luma.core.legacy.font import proportional, LCD_FONT

# Basic fetch time config
DEFAULT_WAITING_TIME = 10
STEP_WAITING_TIME = 10
MAX_WAITING_TIME = 30

# Api credentials
URL_API = 'http://api.transilien.com/gare/87543207/depart/87547315'
USER = 'user'
PASSWORD = 'password'

def message_formatter(miss, date):
    date_train = datetime.strptime(date, '%d/%m/%Y %H:%M')
    date = int( round( (date_train - datetime.now()).seconds / 60 ) )
    date = "%smin" % str(date) if date < 60 else "%sh" % str(date//60)

    return ("%s : %s" % (miss, date))

def manage_waiting_time(is_error, waiting_time):
    if is_error:
        if waiting_time < MAX_WAITING_TIME:
            waiting_time += STEP_WAITING_TIME
        return waiting_time

    return DEFAULT_WAITING_TIME

def rer_watcher():
    # create matrix device
    # serial = spi(port=0, device=0, gpio=noop())
    # device = max7219(serial, width=64, height=16, block_orientation=-90, rotate=0)
    # device.contrast(32)
    # print("Matrix device created")

    waiting_time = DEFAULT_WAITING_TIME
    messages = []

    while True:
        try:
            r = requests.get(URL_API, auth=HTTPBasicAuth(USER, PASSWORD))

            tree = etree.fromstring(r.text.encode('utf-8'))

            for train in tree.xpath('/passages/train')[:2]:
                msg = message_formatter(
                    train.find('miss').text,
                    train.find('date').text
                )
                messages.append(msg)
            messages.reverse()

            waiting_time = manage_waiting_time(False, waiting_time)
        except requests.exceptions.RequestException as e:
            waiting_time = manage_waiting_time(True, waiting_time)
            messages.append('Connexion error')
        except Exception as e:
            waiting_time = manage_waiting_time(True, waiting_time)
            messages.append('Data error')
        finally:
            for i in range(len(messages)):
                print(messages.pop(i - 1))

            # with canvas(device) as draw:
            #     for msg in messages:
            #         text(draw, (0, 9), "World", fill="white", font=proportional(LCD_FONT))

            time.sleep(waiting_time);

if __name__ == "__main__":
    try:
        rer_watcher()
    except KeyboardInterrupt:
        pass
