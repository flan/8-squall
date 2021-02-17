# -*- coding: utf-8 -*-
import random

HELP_SUMMARY = "`!choose <choices delimited by commas, semicolons, or linebreaks>` to have one picked"

async def handle_message(client, message):
    if message.content.startswith(('!choose ', '!choose\n')):
        request = message.content[8:]
        
        if '\n' in request:
            choices = request.split('\n')
        elif ';' in request:
            choices = request.split(';')
        elif ',' in request:
            choices = request.split(',')
        else:
            choices = ()
        choices = [i for i in (j.strip() for j in choices) if i]
        
        if len(choices) >= 2:
            await message.channel.send("{}, {}".format(
                message.author.display_name,
                random.choice(choices),
            ))
        else:
            await message.channel.send("There was nothing to choose between, {}; give me a list separated by commas, semicolons, or linebreaks.".format(message.author.display_name))
        return True
    return False
