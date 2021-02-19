# -*- coding: utf-8 -*-
#intermediate format: Litre

DECODERS = {}
ENCODERS = {}

def _from_litres(quantity):
    return (quantity, 'L')
DECODERS['L'] = _from_litres
DECODERS['Litre'] = _from_litres
DECODERS['Litres'] = _from_litres
DECODERS['Liter'] = _from_litres
DECODERS['Liters'] = _from_litres

def _to_litres(intermediate):
    return (intermediate, 'L')
ENCODERS['L'] = _to_litres
ENCODERS['Litre'] = _to_litres
ENCODERS['Litres'] = _to_litres
ENCODERS['Liter'] = _to_litres
ENCODERS['Liters'] = _to_litres


def _from_millilitres(quantity):
    return (quantity / 1000.0, 'mL')
DECODERS['Ml'] = _from_millilitres
DECODERS['Millilitre'] = _from_millilitres
DECODERS['Millilitres'] = _from_millilitres
DECODERS['Milliliter'] = _from_millilitres
DECODERS['Milliliters'] = _from_millilitres

def _to_millilitres(intermediate):
    return (intermediate * 1000.0, 'mL')
ENCODERS['Ml'] = _to_millilitres
ENCODERS['Millilitre'] = _to_millilitres
ENCODERS['Millilitres'] = _to_millilitres
ENCODERS['Milliliter'] = _to_millilitres
ENCODERS['Milliliters'] = _to_millilitres


def _from_ounces(quantity):
    return (quantity / 33.814, 'floz')
DECODERS['Oz'] = _from_ounces
DECODERS['Floz'] = _from_ounces
DECODERS['Ounce'] = _from_ounces
DECODERS['Ounces'] = _from_ounces

def _to_ounces(intermediate):
    return (intermediate * 33.814, 'floz')
ENCODERS['Oz'] = _to_ounces
ENCODERS['Floz'] = _to_ounces
ENCODERS['Ounce'] = _to_ounces
ENCODERS['Ounces'] = _to_ounces


def _from_pints(quantity):
    return (quantity / 2.11338, 'pt')
DECODERS['Pt'] = _from_pints
DECODERS['Pint'] = _from_pints
DECODERS['Pints'] = _from_pints

def _to_pints(intermediate):
    return (intermediate * 2.11338, 'pt')
ENCODERS['Pt'] = _to_pints
ENCODERS['Pint'] = _to_pints
ENCODERS['Pints'] = _to_pints


def _from_quarts(quantity):
    return (quantity / 1.05669, 'qt')
DECODERS['Qt'] = _from_quarts
DECODERS['Quart'] = _from_quarts
DECODERS['Quarts'] = _from_quarts

def _to_quarts(intermediate):
    return (intermediate * 1.05669, 'qt')
ENCODERS['Qt'] = _to_quarts
ENCODERS['Quart'] = _to_quarts
ENCODERS['Quarts'] = _to_quarts


def _from_gallons(quantity):
    return (quantity * 0.2641720524, 'gal')
DECODERS['Gal'] = _from_gallons
DECODERS['Gallon'] = _from_gallons
DECODERS['Gallons'] = _from_gallons

def _to_gallons(intermediate):
    return (intermediate / 0.2641720524, 'gal')
ENCODERS['Gal'] = _to_gallons
ENCODERS['Gallon'] = _to_gallons
ENCODERS['Gallons'] = _to_gallons


def _from_teaspoons(quantity):
    return (quantity / 202.884136, 'tsp')
DECODERS['Tsp'] = _from_teaspoons
DECODERS['Teaspoon'] = _from_teaspoons
DECODERS['Teaspoons'] = _from_teaspoons

def _to_teaspoons(intermediate):
    return (intermediate * 202.884136, 'tsp')
ENCODERS['Tsp'] = _to_teaspoons
ENCODERS['Teaspoon'] = _to_teaspoons
ENCODERS['Teaspoons'] = _to_teaspoons


def _from_tablespoons(quantity):
    return (quantity / 67.628045, 'tbsp')
DECODERS['Tbsp'] = _from_tablespoons
DECODERS['Tablespoon'] = _from_tablespoons
DECODERS['Tablespoons'] = _from_tablespoons

def _to_tablespoons(intermediate):
    return (intermediate * 67.628045, 'tbsp')
ENCODERS['Tbsp'] = _to_tablespoons
ENCODERS['Tablespoon'] = _to_tablespoons
ENCODERS['Tablespoons'] = _to_tablespoons


def _from_cups(quantity):
    return (quantity / 4.226753, 'c')
DECODERS['C'] = _from_cups
DECODERS['Cup'] = _from_cups
DECODERS['Cups'] = _from_cups

def _to_cups(intermediate):
    return (intermediate * 4.226753, 'c')
ENCODERS['C'] = _to_cups
ENCODERS['Cup'] = _to_cups
ENCODERS['Cups'] = _to_cups
