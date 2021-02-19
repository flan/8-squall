# -*- coding: utf-8 -*-
#intermediate format: second

DECODERS = {}
ENCODERS = {}

def _from_second(quantity):
    return (quantity, 's')
DECODERS['S'] = _from_second
DECODERS['Second'] = _from_second
DECODERS['Seconds'] = _from_second

def _to_second(intermediate):
    return (intermediate, 's')
ENCODERS['S'] = _to_second
ENCODERS['Second'] = _to_second
ENCODERS['Seconds'] = _to_seconds


def _from_minute(quantity):
    return (quantity * 60.0, 's')
DECODERS['M'] = _from_minute
DECODERS['Minute'] = _from_minute
DECODERS['Minutes'] = _from_minute

def _to_minute(intermediate):
    return (intermediate / 60.0, 's')
ENCODERS['M'] = _to_minute
ENCODERS['Minute'] = _to_minute
ENCODERS['Minutes'] = _to_minute


def _from_hour(quantity):
    return (quantity * 3600.0, 'h')
DECODERS['H'] = _from_hour
DECODERS['Hour'] = _from_hour
DECODERS['Hours'] = _from_hour

def _to_hour(intermediate):
    return (intermediate / 3600.0, 'h')
ENCODERS['H'] = _to_hour
ENCODERS['Hour'] = _to_hour
ENCODERS['Hours'] = _to_hour


def _from_day(quantity):
    return (quantity * 86400.0, 'd')
DECODERS['D'] = _from_day
DECODERS['Day'] = _from_day
DECODERS['Days'] = _from_day

def _to_day(intermediate):
    return (intermediate / 86400.0, 'd')
ENCODERS['D'] = _to_day
ENCODERS['Day'] = _to_day
ENCODERS['Days'] = _to_day


def _from_week(quantity):
    return (quantity * 604800.0, 'w')
DECODERS['W'] = _from_week
DECODERS['Week'] = _from_week
DECODERS['Weeks'] = _from_week

def _to_week(intermediate):
    return (intermediate / 604800.0, 'w')
ENCODERS['W'] = _to_week
ENCODERS['Week'] = _to_week
ENCODERS['Weeks'] = _to_week
