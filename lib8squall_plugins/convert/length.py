# -*- coding: utf-8 -*-
#intermediate format: Metre

DECODERS = {}
ENCODERS = {}

def _from_metres(quantity):
    return (quantity, 'm')
DECODERS['M'] = _from_metres
DECODERS['Metre'] = _from_metres
DECODERS['Metres'] = _from_metres
DECODERS['Meter'] = _from_metres
DECODERS['Meters'] = _from_metres

def _to_metres(intermediate):
    return (intermediate, 'm')
ENCODERS['M'] = _to_metres
ENCODERS['Metre'] = _to_metres
ENCODERS['Metres'] = _to_metres
ENCODERS['Meter'] = _to_metres
ENCODERS['Meters'] = _to_metres


def _from_millimetres(quantity):
    return (quantity / 1000.0, 'mm')
DECODERS['Mm'] = _from_millimetres
DECODERS['Millimetre'] = _from_millimetres
DECODERS['Millimetres'] = _from_millimetres
DECODERS['Millimeter'] = _from_millimetres
DECODERS['Millimeters'] = _from_millimetres

def _to_millimetres(intermediate):
    return (intermediate * 1000.0, 'mm')
ENCODERS['Mm'] = _to_millimetres
ENCODERS['Millimetre'] = _to_millimetres
ENCODERS['Millimetres'] = _to_millimetres
ENCODERS['Millimeter'] = _to_millimetres
ENCODERS['Millimeters'] = _to_millimetres


def _from_centimetres(quantity):
    return (quantity / 100.0, 'cm')
DECODERS['Cm'] = _from_centimetres
DECODERS['Centimetre'] = _from_centimetres
DECODERS['Centimetres'] = _from_centimetres
DECODERS['Centimeter'] = _from_centimetres
DECODERS['Centimeters'] = _from_centimetres

def _to_centimetres(intermediate):
    return (intermediate * 100.0, 'cm')
ENCODERS['Cm'] = _to_centimetres
ENCODERS['Centimetre'] = _to_centimetres
ENCODERS['Centimetres'] = _to_centimetres
ENCODERS['Centimeter'] = _to_centimetres
ENCODERS['Centimeters'] = _to_centimetres


def _from_kilometres(quantity):
    return (quantity * 1000.0, 'km')
DECODERS['Km'] = _from_kilometres
DECODERS['Kilometre'] = _from_kilometres
DECODERS['Kilometres'] = _from_kilometres
DECODERS['Kilometer'] = _from_kilometres
DECODERS['Kilometers'] = _from_kilometres

def _to_kilometres(intermediate):
    return (intermediate / 1000.0, 'km')
ENCODERS['Km'] = _to_kilometres
ENCODERS['Kilometre'] = _to_kilometres
ENCODERS['Kilometres'] = _to_kilometres
ENCODERS['Kilometer'] = _to_kilometres
ENCODERS['Kilometers'] = _to_kilometres


def _from_inches(quantity):
    return (quantity * 0.02539999999997257, "''")
DECODERS['In'] = _from_inches
DECODERS['Inch'] = _from_inches
DECODERS['Inches'] = _from_inches

def _to_inches(intermediate):
    return (intermediate * 39.3700787402, "''")
ENCODERS['In'] = _to_inches
ENCODERS['Inch'] = _to_inches
ENCODERS['Inches'] = _to_inches


def _from_feet(quantity):
    return (quantity * 0.3048000000012192, "'")
DECODERS['Ft'] = _from_feet
DECODERS['Foot'] = _from_feet
DECODERS['Feet'] = _from_feet

def _to_feet(intermediate):
    return (intermediate * 3.280839895, "'")
ENCODERS['Ft'] = _to_feet
ENCODERS['Foot'] = _to_feet
ENCODERS['Feet'] = _to_feet


def _from_yards(quantity):
    return (quantity * 0.9144000000315285, "'''")
DECODERS['Y'] = _from_yards
DECODERS['Yd'] = _from_yards
DECODERS['Yds'] = _from_yards
DECODERS['Yard'] = _from_yards
DECODERS['Yards'] = _from_yards

def _to_yards(intermediate):
    return (intermediate * 1.0936132983, "'''")
ENCODERS['Y'] = _to_yards
ENCODERS['Yd'] = _to_yards
ENCODERS['Yds'] = _to_yards
ENCODERS['Yard'] = _to_yards
ENCODERS['Yards'] = _to_yards


def _from_miles(quantity):
    return (quantity * 1609.3439798947877, "mi")
DECODERS['Mi'] = _from_miles
DECODERS['Mile'] = _from_miles
DECODERS['Miles'] = _from_miles

def _to_miles(intermediate):
    return (intermediate * 0.0006213712, "mi")
ENCODERS['Mi'] = _to_miles
ENCODERS['Mile'] = _to_miles
ENCODERS['Miles'] = _to_miles
