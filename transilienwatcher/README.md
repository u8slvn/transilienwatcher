# TransilienWatcher

[![CI](https://github.com/u8slvn/transilienwatcher/actions/workflows/ci.yml/badge.svg)](https://github.com/u8slvn/transilienwatcher/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/u8slvn/transilienwatcher/badge.svg)](https://coveralls.io/github/u8slvn/transilienwatcher)
![Python version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10-blue)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Zero%20W%20%7C%203%20B%2B-c51A4A?logo=raspberry-pi)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Setup Raspberry PI

```shell
$ sudo apt update
$ sudo apt upgrade
$ sudo apt install git
$ sudo apt install python-smbus
$ sudo apt-get install pigpio python-pigpio python3-pigpio
$ sudo apt install python3-pip
$ pip3 install --upgrade pip
$ rpi-update
$ sudo reboot
```

After reboot:

```shell
$ sudo raspi-config
```

Select `3 Interface Options` > `P5 I2C` > `Yes` > `Ok` > `Finish` 

## Install TransilienWatcher

```shell
$ pip install git+https://github.com/u8slvn/transilienwatcher.git#egg=transilienwatcher
export PATH=/home/pi/.local/bin:$PATH
```

## Configuration

```shell
$ transiliwatcher-init
$ vim ~/transilienwatcher/config.py
```

```xml
transilien:
  stations:
    departure: '00000000'
    arrival: '00000000'
  credentials:
    username: 'username'
    password: 'password'
refresh_time: 60
display:
  type: 'lcd_i2c'
  lcd:
    columns: 16
    rows: 2
```

## Start TransilienWatcher

```shell
$ transilienwatcher start
$ transilienwatcher status
```

Log file is available in `~/transilienwatcher/transilienwatcher.log`.

Stop the app:

```shell
$ translienwatcher stop
```