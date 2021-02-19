# -*- coding: utf-8 -*-
#intermediate format: Pascal

DECODERS = {}
ENCODERS = {}

def _from_pascals(quantity):
    return (quantity, 'Pa')
DECODERS['Pa'] = _from_pascals
DECODERS['Pascal'] = _from_pascals
DECODERS['Pascals'] = _from_pascals

def _to_pascals(intermediate):
    return (intermediate, 'Pa')
ENCODERS['Pa'] = _to_pascals
ENCODERS['Pascal'] = _to_pascals
ENCODERS['Pascals'] = _to_pascals


def _from_bars(quantity):
    return (quantity * 100000.0, 'bar')
DECODERS['Bar'] = _from_bars
DECODERS['Bars'] = _from_bars

def _to_bars(intermediate):
    return (intermediate / 100000.0, 'bar')
ENCODERS['Bar'] = _to_bars
ENCODERS['Bars'] = _to_bars


def _from_millibars(quantity):
    return (quantity * 100.0, 'millibar')
DECODERS['Millibar'] = _from_millibars
DECODERS['Millibars'] = _from_millibars

def _to_millibars(intermediate):
    return (intermediate / 100.0, 'millibar')
ENCODERS['Millibar'] = _to_millibars
ENCODERS['Millibars'] = _to_millibars


def _from_pounds(quantity):
    return (quantity / 0.020885, 'psf')
DECODERS['Psf'] = _from_pounds
DECODERS['Pound'] = _from_pounds
DECODERS['Pounds'] = _from_pounds

def _to_pounds(intermediate):
    return (intermediate * 0.020885, 'psf')
ENCODERS['Psf'] = _to_pounds
ENCODERS['Pound'] = _to_pounds
ENCODERS['Pounds'] = _to_pounds
