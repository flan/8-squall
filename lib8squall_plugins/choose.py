# -*- coding: utf-8 -*-
import random

def get_help_summary(client, message):
    return ("`!choose <choices delimited by common separators>` to have one picked.",)

async def handle_message(client, message):
    if message.content.startswith(('!choose ', '!choose\n')):
        request = message.content[8:].strip()
        
        for delimiter in ('\n', ';', ',', ' '):
            choices = [i for i in (j.strip() for j in request.split(delimiter)) if i]
            if len(choices) > 1:
                break
        else:
            choices = ()
            
        if len(choices) > 1:
            await message.reply(random.choice(choices))
        else:
            await message.reply("There was nothing to choose between; provide a list separated by spaces, commas, semicolons, or linebreaks.")
        return True
    return False
