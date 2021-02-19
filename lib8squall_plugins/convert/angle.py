# -*- coding: utf-8 -*-
#intermediate format: radian
import math

DECODERS = {}
ENCODERS = {}

def _from_radians(quantity):
    return (quantity, '𝞽')
DECODERS['Rad'] = _from_radians
DECODERS['Radian'] = _from_radians
DECODERS['Radians'] = _from_radians

def _to_radians(intermediate):
    return (intermediate, '𝞽')
ENCODERS['Rad'] = _to_radians
ENCODERS['Radian'] = _to_radians
ENCODERS['Radians'] = _to_radians


def _from_degrees(quantity):
    return (math.radians(quantity), '°')
DECODERS['Deg'] = _from_degrees
DECODERS['Degree'] = _from_degrees
DECODERS['Degrees'] = _from_degrees

def _to_degrees(intermediate):
    return (math.degrees(intermediate), '°')
ENCODERS['Deg'] = _to_degrees
ENCODERS['Degree'] = _to_degrees
ENCODERS['Degrees'] = _to_degrees


def _from_gradians(quantity):
    return (quantity * (math.pi / 200.0), 'ᵍ')
DECODERS['Gon'] = _from_gradians
DECODERS['Grad'] = _from_gradians
DECODERS['Grads'] = _from_gradians
DECODERS['Grade'] = _from_gradians
DECODERS['Gradien'] = _from_gradians
DECODERS['Gradiens'] = _from_gradians

def _to_gradiens(intermediate):
    return (intermediate * (200.0 / math.pi), 'ᵍ')
ENCODERS['Gon'] = _to_gradiens
ENCODERS['Grad'] = _to_gradiens
ENCODERS['Grads'] = _to_gradiens
ENCODERS['Grade'] = _to_gradiens
ENCODERS['Gradien'] = _to_gradiens
ENCODERS['Gradiens'] = _to_gradiens


def _from_turns(quantity):
    return (quantity * (2 * math.pi), 'τ')
DECODERS['Turn'] = _from_turns
DECODERS['Turns'] = _from_turns
DECODERS['Cyc'] = _from_turns
DECODERS['Cycle'] = _from_turns
DECODERS['Cycles'] = _from_turns
DECODERS['Rev'] = _from_turns
DECODERS['Revolution'] = _from_turns
DECODERS['Revolutions'] = _from_turns
DECODERS['Circle'] = _from_turns

def _to_turns(intermediate):
    return (intermediate / (2 * math.pi), 'τ')
ENCODERS['Turn'] = _to_turns
ENCODERS['Turns'] = _to_turns
ENCODERS['Cyc'] = _to_turns
ENCODERS['Cycle'] = _to_turns
ENCODERS['Cycles'] = _to_turns
ENCODERS['Rev'] = _to_turns
ENCODERS['Revolution'] = _to_turns
ENCODERS['Revolutions'] = _to_turns
ENCODERS['Circle'] = _to_turns
