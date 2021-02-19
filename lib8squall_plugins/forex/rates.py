# -*- coding: utf-8 -*-
import collections
import threading
import time

import requests

from . import currencies

_Rates = collections.namedtuple("Rates", (
    "date",
    "rates",
))
_CACHE = {}
_CACHE_LOCK = threading.Lock()

def get_rates(currency):
    current_time = time.gmtime()
    
    with _CACHE_LOCK:
        rates = _CACHE.get(currency)
        
        if rates:
            date_difference = current_time.tm_yday - rates.date.tm_yday
            if current_time.tm_year == rates.date.tm_year and (
                date_difference == 0 or #today's data already available
                (date_difference == 1 and current_time.tm_hour < 15) #upstream data hasn't updated
            ):
                return rates.rates
                
        rates_data = requests.get("https://api.ratesapi.io/api/latest", params={"base": currency.code}).json()
        
        _CACHE[currency] = rates = _Rates(
            time.strptime(rates_data['date'], '%Y-%m-%d'),
            {currencies.get_currency(k): v for (k, v) in rates_data['rates'].items()},
        )
        
        return rates.rates
