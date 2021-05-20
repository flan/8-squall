# -*- coding: utf-8 -*-
import collections

_Currency = collections.namedtuple("Currency", (
    "code",
    "symbol",
))
CURRENCIES = {currency.code: currency for currency in (
    _Currency('AUD', '$'),
    _Currency('BGN', ''),
    _Currency('BRL', '$'),
    _Currency('BTC', '₿'),
    _Currency('CAD', '$'),
    _Currency('CHF', ''),
    _Currency('CNY', '¥'),
    _Currency('CZK', ''),
    _Currency('DKK', ''),
    _Currency('EUR', '€'),
    _Currency('GBP', '£'),
    _Currency('HKD', '$'),
    _Currency('HRK', ''),
    _Currency('HUF', ''),
    _Currency('IDR', ''),
    _Currency('ILS', '₪'),
    _Currency('INR', '₹'),
    _Currency('ISK', ''),
    _Currency('JPY', '¥'),
    _Currency('KRW', ''),
    _Currency('MXN', '$'),
    _Currency('MYR', ''),
    _Currency('NOK', ''),
    _Currency('NZD', '$'),
    _Currency('PHP', '₱'),
    _Currency('PLN', 'ł'),
    _Currency('RON', ''),
    _Currency('RUB', ''),
    _Currency('SEK', ''),
    _Currency('SGD', '$'),
    _Currency('THB', '฿'),
    _Currency('TRY', ''),
    _Currency('USD', '$'),
    _Currency('ZAR', ''),
)}

def get_currency(symbol):
    return CURRENCIES.get(symbol.upper())
    
