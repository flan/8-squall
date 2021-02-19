# -*- coding: utf-8 -*-
#intermediate format: Newton

DECODERS = {}
ENCODERS = {}

def _from_newtons(quantity):
    return (quantity, 'N')
DECODERS['N'] = _from_newtons
DECODERS['Newton'] = _from_newtons
DECODERS['Newtons'] = _from_newtons

def _to_newtons(intermediate):
    return (intermediate, 'N')
ENCODERS['N'] = _to_newtons
ENCODERS['Newton'] = _to_newtons
ENCODERS['Newtons'] = _to_newtons


def _from_pounds(quantity):
    return (quantity * 4.4482216282509, 'lb')
DECODERS['Lb'] = _from_pounds
DECODERS['Lbs'] = _from_pounds
DECODERS['Pound'] = _from_pounds
DECODERS['Pounds'] = _from_pounds

def _to_pounds(intermediate):
    return (intermediate / 4.4482216282509, 'lb')
ENCODERS['Lb'] = _to_pounds
ENCODERS['Lbs'] = _to_pounds
ENCODERS['Pound'] = _to_pounds
ENCODERS['Pounds'] = _to_pounds
