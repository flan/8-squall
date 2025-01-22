# -*- coding: utf-8 -*-
#intermediate format: Celsius

DECODERS = {}
ENCODERS = {}

def _from_celsius(quantity):
    return (quantity, '°C')
DECODERS['C'] = _from_celsius
DECODERS['Celsius'] = _from_celsius

def _to_celsius(intermediate):
    return (intermediate, '°C')
ENCODERS['C'] = _from_celsius
ENCODERS['Celsius'] = _from_celsius


def _from_kelvin(quantity):
    return (quantity - 273.15, '°K')
DECODERS['K'] = _from_kelvin
DECODERS['Kelvin'] = _from_kelvin

def _to_kelvin(intermediate):
    return (intermediate + 273.15, '°K')
ENCODERS['K'] = _to_kelvin
ENCODERS['Kelvin'] = _to_kelvin


def _from_fahrenheit(quantity):
    return ((quantity - 32) / 1.8, '°F')
DECODERS['F'] = _from_fahrenheit
DECODERS['Fahrenheit'] = _from_fahrenheit

def _to_fahrenheit(intermediate):
    return ((intermediate * 1.8) + 32, '°F')
ENCODERS['F'] = _to_fahrenheit
ENCODERS['Fahrenheit'] = _to_fahrenheit
