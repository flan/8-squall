# -*- coding: utf-8 -*-
import collections
import threading
import time

import requests

from . import currencies

_CACHE_LAST_UPDATED = 0.0
_CACHE_MAX_AGE = 3600.0
_CACHE = {}
_CACHE_LOCK = threading.Lock()

_FIXER_API_KEY = open("./fixer.key").read().strip()

def get_rates(currency):
    global _CACHE
    global _CACHE_LAST_UPDATED
    with _CACHE_LOCK:
        if time.time() - _CACHE_LAST_UPDATED > _CACHE_MAX_AGE:
            rates_data = requests.get("http://data.fixer.io/api/latest", params={
                "access_key": _FIXER_API_KEY,
                "base": "EUR",
                "symbols": ','.join(currencies.CURRENCIES.keys()),
            }).json()
            print("fixer.io response: {}".format(rates_data))
            
            _CACHE = {currencies.get_currency(k): v for (k, v) in rates_data['rates'].items()}
            _CACHE_LAST_UPDATED = rates_data['timestamp']
            
        relative_rate = _CACHE[currency]
        return {k:(v / relative_rate) for (k, v) in _CACHE.items()}
        
