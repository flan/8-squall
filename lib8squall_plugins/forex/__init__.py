# -*- coding: utf-8 -*-
import re

from . import currencies
from . import rates

def get_help_summary(client, message):
    return ("`!curr [quantity] <symbol> [to] <symbol>` for currency conversion.",)

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
            if quantity is None or quantity == '.': #the regex allows '.' for the sake of readability
                quantity = 1.0
            else:
                quantity = float(quantity)
                
            try:
                current_rate = rates.get_rates(cur1)[cur2]
            except Exception:
                await message.reply("Unable to fetch current currency data; please try again later.")
                raise
            else:
                await message.reply("{}{:,.2f} {} = {}{:,.2f} {}".format(
                    cur1.symbol, quantity, cur1.code,
                    cur2.symbol, quantity * current_rate, cur2.code,
                ))
        return True
    return False
