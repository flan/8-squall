# -*- coding: utf-8 -*-
import random

def get_help_summary(client, message):
    return (
        "Dice-simulation",
        (
            "`!dice <#d#> [#d#...]` to simulate dice rolls, like `!dice 2d10 5d6`",
            "The value before the `d` is the number of dice to roll and the second is the number of faces.",
            "Alias: `!roll`",
        ),
    )

async def handle_message(client, message):
    if message.content.startswith(('!dice ', '!roll ')):
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
                    
                results = [random.randint(1, kind) for i in range(qty)]
                response.append('{} `{{{}}}`'.format(
                    token,
                    ', '.join(str(i) for i in results),
                ))
                if len(results) > 1:
                    response.append('    sum: `{:,}`, mean: `{:,.1f}`, min: `{:,}`, max: `{:,}`'.format(
                        sum(results),
                        sum(results) / float(len(results)),
                        min(results),
                        max(results),
                    ))
                    
        if response:
            await message.reply('\n'.join(response))
        else:
            await message.reply("There were no dice-rolls to process; try something like `4d20`.")
        return True
    return False
