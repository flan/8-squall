# -*- coding: utf-8 -*-
#intermediate format: Joule

DECODERS = {}
ENCODERS = {}

def _from_joules(quantity):
    return (quantity, 'J')
DECODERS['J'] = _from_joules
DECODERS['Joule'] = _from_joules
DECODERS['Joules'] = _from_joules

def _to_joules(intermediate):
    return (intermediate, 'J')
ENCODERS['J'] = _to_joules
ENCODERS['Joule'] = _to_joules
ENCODERS['Joules'] = _to_joules


def _from_kilojoules(quantity):
    return (quantity * 1000.0, 'kJ')
DECODERS['Kj'] = _from_kilojoules
DECODERS['Kilojoule'] = _from_kilojoules
DECODERS['Kilojoules'] = _from_kilojoules

def _to_kilojoules(intermediate):
    return (intermediate / 1000.0, 'kJ')
ENCODERS['Kj'] = _to_kilojoules
ENCODERS['Kilojoule'] = _to_kilojoules
ENCODERS['Kilojoules'] = _to_kilojoules


def _from_calories(quantity):
    return (quantity * 4.184, 'cal')
DECODERS['Cal'] = _from_calories
DECODERS['Calorie'] = _from_calories
DECODERS['Calories'] = _from_calories

def _to_calories(intermediate):
    return (intermediate / 4.184, 'cal')
ENCODERS['Cal'] = _to_calories
ENCODERS['Calorie'] = _to_calories
ENCODERS['Calories'] = _to_calories


def _from_kilocalories(quantity):
    return (quantity * 4184.0, 'kcal')
DECODERS['Kcal'] = _from_kilocalories
DECODERS['Kilocalorie'] = _from_kilocalories
DECODERS['Kilocalories'] = _from_kilocalories

def _to_kilocalories(intermediate):
    return (intermediate / 4184.0, 'kcal')
ENCODERS['Kcal'] = _to_kilocalories
ENCODERS['Kilocalorie'] = _to_kilocalories
ENCODERS['Kilocalories'] = _to_kilocalories
