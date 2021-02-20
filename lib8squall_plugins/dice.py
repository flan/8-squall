# -*- coding: utf-8 -*-
import random

def get_help_summary(client, message):
    return ("`!dice <#d#r> [#d#...]` to simulate dice rolls, like 2d10.",)

async def handle_message(client, message):
    if message.content.startswith('!dice '):
        response = []
        for token in message.content[6:].split():
            token = token.strip().lower()
            tokens = token.split('d', 1)
            if len(tokens) != 2:
                continue
                
            try:
                if tokens[0]:
                    qty = int(tokens[0])
                else:
                    qty = 1
                kind = int(tokens[1])
            except ValueError:
                continue
            else:
                if qty <= 0 or kind <= 0:
                    continue
                    
                response.append('{} `{{{}}}`'.format(
                    token,
                    ', '.join([str(random.randint(1, kind)) for i in range(qty)]),
                ))
                
        if response:
            await message.reply('\n'.join(response))
        else:
            await message.reply("There were no dice-rolls to process; try something like '4d20'.")
        return True
    return False
