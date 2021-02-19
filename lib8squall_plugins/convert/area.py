# -*- coding: utf-8 -*-
#intermediate format: square Metre

DECODERS = {}
ENCODERS = {}

def _from_sqm(quantity):
    return (quantity, 'sqm')
DECODERS['Sqm'] = _from_sqm
DECODERS['M2'] = _from_sqm

def _to_sqm(intermediate):
    return (intermediate, 'sqm')
ENCODERS['Sqm'] = _to_sqm
ENCODERS['M2'] = _to_sqm


def _from_sqcm(quantity):
    return (quantity / 10000.0, 'sqcm')
DECODERS['Sqcm'] = _from_sqcm
DECODERS['Cm2'] = _from_sqcm

def _to_sqcm(intermediate):
    return (intermediate * 10000.0, 'sqcm')
ENCODERS['Sqcm'] = _to_sqcm
ENCODERS['Cm2'] = _to_sqcm


def _from_sqkm(quantity):
    return (quantity * 1000000.0, 'sqkm')
DECODERS['Sqkm'] = _from_sqkm
DECODERS['Km2'] = _from_sqkm

def _to_sqkm(intermediate):
    return (intermediate / 1000000.0, 'sqkm')
ENCODERS['Sqkm'] = _to_sqkm
ENCODERS['Km2'] = _to_sqkm


def _from_sqin(quantity):
    return (quantity / 1550.0031000062, 'sqin')
DECODERS['Sqin'] = _from_sqin
DECODERS['In2'] = _from_sqin

def _to_sqin(intermediate):
    return (intermediate * 1550.0031000062, 'sqin')
ENCODERS['Sqin'] = _to_sqin
ENCODERS['In2'] = _to_sqin


def _from_sqft(quantity):
    return (quantity / 10.76391041671, 'sqft')
DECODERS['Sqft'] = _from_sqft
DECODERS['Ft2'] = _from_sqft

def _to_sqft(intermediate):
    return (intermediate * 10.76391041671, 'sqft')
ENCODERS['Sqft'] = _to_sqft
ENCODERS['Ft2'] = _to_sqft


def _from_sqyd(quantity):
    return (quantity / 1.19599, 'sqyd')
DECODERS['Sqyd'] = _from_sqyd
DECODERS['Yd2'] = _from_sqyd

def _to_sqyd(intermediate):
    return (intermediate * 1.19599, 'sqyd')
ENCODERS['Sqyd'] = _to_sqyd
ENCODERS['Yd2'] = _to_sqyd


def _from_sqmi(quantity):
    return (quantity * 2589988.110285327, 'sqmi')
DECODERS['Sqmi'] = _from_sqmi
DECODERS['Mi2'] = _from_sqmi

def _to_sqmi(intermediate):
    return (intermediate / 2589988.110285327, 'sqmi')
ENCODERS['Sqmi'] = _to_sqmi
ENCODERS['Mi2'] = _to_sqmi


def _from_acre(quantity):
    return (quantity * 4046.8564224, 'acre')
DECODERS['Ac'] = _from_acre
DECODERS['Acre'] = _from_acre
DECODERS['Acres'] = _from_acre

def _to_acre(intermediate):
    return (intermediate / 4046.8564224, 'acre')
ENCODERS['Ac'] = _to_acre
ENCODERS['Acre'] = _to_acre
ENCODERS['Acres'] = _to_acre


def _from_hectare(quantity):
    return (quantity * 10000.0, 'ha')
DECODERS['Ha'] = _from_hectare
DECODERS['Hectare'] = _from_hectare
DECODERS['Hectares'] = _from_hectare

def _to_hectare(intermediate):
    return (intermediate / 10000.0, 'ha')
ENCODERS['Ha'] = _to_hectare
ENCODERS['Hectare'] = _to_hectare
ENCODERS['Hectares'] = _to_hectare
