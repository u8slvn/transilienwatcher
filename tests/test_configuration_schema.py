from cerberus import Validator
import pytest

from transilienwatcher.configuration import (arrival_schema, credential_schema,
                                             departure_schema, display_schema,
                                             lcd_size_schema)

departure_validator = Validator({'departure': departure_schema})
arrival_validator = Validator({'arrival': arrival_schema})
credential_validator = Validator({'credential': credential_schema})
lcd_size_validator = Validator({'lcd_size': lcd_size_schema})
display_validator = Validator({'display': display_schema})


@pytest.mark.parametrize('departure, expected', [
    ({'departure': '12345678'}, True),
    ({'departure': 12345678}, False),
    ({'departure': '1234'}, False),
    ({'departure': '1234567890'}, False),
    ({'departure': 'abc'}, False),
    ({'departure': None}, False),
    ({}, False),
])
def test_departure_schema(departure, expected):
    assert expected == departure_validator.validate(departure)


@pytest.mark.parametrize('arrival, expected', [
    ({'arrival': '12345678'}, True),
    ({'arrival': None}, True),
    ({}, True),
    ({'arrival': 12345678}, False),
    ({'arrival': '1234'}, False),
    ({'arrival': '1234567890'}, False),
    ({'arrival': 'abc'}, False),
])
def test_arrival_schema(arrival, expected):
    assert expected == arrival_validator.validate(arrival)


@pytest.mark.parametrize('credential, expected', [
    ({'credential': 'password'}, True),
    ({'credential': 1234}, False),
    ({'credential': None}, False),
    ({}, False),
])
def test_credential_schema(credential, expected):
    assert expected == credential_validator.validate(credential)


@pytest.mark.parametrize('lcd_size, expected', [
    ({'lcd_size': 20}, True),
    ({'lcd_size': '20'}, False),
    ({'lcd_size': None}, False),
    ({}, False),
])
def test_lcd_size_schema(lcd_size, expected):
    assert expected == lcd_size_validator.validate(lcd_size)


@pytest.mark.parametrize('display, expected', [
    ({
         'display': {
             'type': 'console',
         }
     }, True),
    ({
         'display': {
             'type': 'lcd',
             'lcd': {
                 'columns': 16,
                 'rows': 2,
             }
         },
     }, True),
    ({
         'display': {
             'type': 'foo',
         },
     }, False),
    ({
         'display': {
             'type': 'lcd',
         },
     }, False),
    ({
         'display': {
             'lcd': {
                 'columns': 16,
                 'rows': 2,
             }
         },
     }, False),
    ({
         'display': {
             'type': None,
         },
     }, False),
    ({'display': {}}, False),
])
def test_display_schema(display, expected):
    assert expected == display_validator.validate(display)
