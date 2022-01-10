# -*- coding: utf-8 -*-
import re

from . import currencies
from . import rates

def get_help_summary(client, message):
    return ("`!curr [quantity] <symbol> [to] <symbol>` for currency-conversion.",)

_QUERY_RE = re.compile(r'(?P<qty>-?\d*\.?\d*)?\s*(?P<cur1>[a-zA-Z]{3,4})\s+(?:to\s+)?(?P<cur2>[a-zA-Z]{3,4})')

async def handle_message(client, message):
    if message.content.startswith('!curr '):
        query_match = _QUERY_RE.search(message.content[6:])
        if query_match:
            cur1 = currencies.get_currency(query_match.group('cur1'))
            if not cur1:
                await message.reply("{} is not a supported currency.".format(query_match.group('cur1').upper()))
                return True
            cur2 = currencies.get_currency(query_match.group('cur2'))
            if not cur2:
                await message.reply("{} is not a supported currency.".format(query_match.group('cur2').upper()))
                return True
                
            quantity = query_match.group('qty')
            if not quantity or quantity == '.': #the regex allows '.' for the sake of readability
                quantity = 1.0
            else:
                quantity = float(quantity)
                
            try:
                current_rate = rates.get_rates(cur1)[cur2]
            except Exception:
                await message.reply("Unable to fetch current currency data; please try again later.")
                raise
            else:
                await message.reply("{symbol1}{base:,.2f} {code1} = {symbol2}{rate:,.2f} {code2}\n{symbol2}{base:,.2f} {code2} = {symbol1}{inverted_rate:,.2f} {code1}".format(
                    symbol1=cur1.symbol,
                    symbol2=cur2.symbol,
                    code1=cur1.code,
                    code2=cur2.code,
                    base=quantity,
                    rate=(quantity * current_rate),
                    inverted_rate=(quantity / current_rate),
                ))
        return True
    return False
