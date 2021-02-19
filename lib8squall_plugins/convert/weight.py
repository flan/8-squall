# -*- coding: utf-8 -*-
#intermediate format: gram

DECODERS = {}
ENCODERS = {}

def _from_grams(quantity):
    return (quantity, 'g')
DECODERS['G'] = _from_grams
DECODERS['Gram'] = _from_grams
DECODERS['Grams'] = _from_grams

def _to_grams(intermediate):
    return (intermediate, 'g')
ENCODERS['G'] = _to_grams
ENCODERS['Gram'] = _to_grams
ENCODERS['Grams'] = _to_grams


def _from_milligrams(quantity):
    return (quantity / 1000.0, 'mg')
DECODERS['Mg'] = _from_milligrams
DECODERS['Milligram'] = _from_milligrams
DECODERS['Milligrams'] = _from_milligrams

def _to_milligrams(intermediate):
    return (intermediate * 1000.0, 'mg')
ENCODERS['Mg'] = _to_milligrams
ENCODERS['Milligram'] = _to_milligrams
ENCODERS['Milligrams'] = _to_milligrams


def _from_kilograms(quantity):
    return (quantity * 1000.0, 'kg')
DECODERS['Kg'] = _from_kilograms
DECODERS['Kilogram'] = _from_kilograms
DECODERS['Kilograms'] = _from_kilograms

def _to_kilograms(intermediate):
    return (intermediate / 1000.0, 'kg')
ENCODERS['Kg'] = _to_kilograms
ENCODERS['Kilogram'] = _to_kilograms
ENCODERS['Kilograms'] = _to_kilograms


def _from_tonnes(quantity):
    return (quantity * 1000000.0, 'Mg')
DECODERS['Tonne'] = _from_tonnes
DECODERS['Megagram'] = _from_tonnes
DECODERS['Megagrams'] = _from_tonnes

def _to_tonnes(intermediate):
    return (intermediate / 1000000.0, 'Mg')
ENCODERS['Tonne'] = _to_tonnes
ENCODERS['Megagram'] = _to_tonnes
ENCODERS['Megagrams'] = _to_tonnes


def _from_ounces(quantity):
    return (quantity * 28.34952, 'oz')
DECODERS['Oz'] = _from_ounces
DECODERS['Ounce'] = _from_ounces
DECODERS['Ounces'] = _from_ounces

def _to_ounces(intermediate):
    return (intermediate * 0.03527396195, 'oz')
ENCODERS['Oz'] = _to_ounces
ENCODERS['Ounce'] = _to_ounces
ENCODERS['Ounces'] = _to_ounces


def _from_pounds(quantity):
    return (quantity * 453.59237, 'lb')
DECODERS['Lb'] = _from_pounds
DECODERS['Lbs'] = _from_pounds
DECODERS['Pound'] = _from_pounds
DECODERS['Pounds'] = _from_pounds

def _to_pounds(intermediate):
    return (intermediate * 0.002204622621848776, 'lb')
ENCODERS['Lb'] = _to_pounds
ENCODERS['Lbs'] = _to_pounds
ENCODERS['Pound'] = _to_pounds
ENCODERS['Pounds'] = _to_pounds


def _from_tons(quantity):
    return (quantity * 907184.74, 't')
DECODERS['Ton'] = _from_tons
DECODERS['Tons'] = _from_tons

def _to_tons(intermediate):
    return (intermediate * 1.102311310924388e-06, 't')
ENCODERS['Ton'] = _to_tons
ENCODERS['Tons'] = _to_tons
