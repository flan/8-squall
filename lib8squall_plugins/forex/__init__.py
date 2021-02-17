# -*- coding: utf-8 -*-
import re

from . import currencies
from . import rates

HELP_SUMMARY = "`!curr [quantity] <symbol> [to|from] <symbol>` for currency conversion."

_QUERY_RE = re.compile(r'(?P<qty>\d*\.?\d*)?\s*(?P<cur1>[a-zA-Z]{3})\s+(?:(?P<dir>to|from)\s+)?(?P<cur2>[a-zA-Z]{3})')

async def handle_message(client, message):
    if message.content.startswith('!curr '):
        query_match = _QUERY_RE.search(message.content[6:])
        if query_match:
            query_match = query_match.groupdict()
            
            cur1 = currencies.get_currency(query_match['cur1'])
            if not cur1:
                await message.channel.send("{} is not a supported currency, {}.".format(query_match['cur1'], message.author.display_name))
                return True
            
            cur2 = currencies.get_currency(query_match['cur2'])
            if not cur2:
                await message.channel.send("{} is not a supported currency, {}.".format(query_match['cur2'], message.author.display_name))
                return True
                
            quantity = query_match['qty']
            if quantity is None or quantity == '.':
                quantity = 1.0
            else:
                quantity = float(quantity)
                
            if query_match['dir'] == 'from':
                current_rate = rates.get_rates(cur2)[cur1]
            else: #assume 'to'
                current_rate = rates.get_rates(cur1)[cur2]
            await message.channel.send("{}, {}{} {} = {}{} {}.".format(
                message.author.display_name,
                cur1.symbol, quantity, cur1.code,
                cur2.symbol, quantity * current_rate, cur2.code,
            ))
        return True
    return False
