# -*- coding: utf-8 -*-
import random

def get_help_summary(client, message):
    return (
        "Decision-making",
        (
            "`!choose <choices>` to have one picked.",
            "Choices may be delimited by space, comma, or semicolon, in ascending order of precedence.",
            "For example, in \"hello, world; goodbye\", the presence of a semicolon means there are two choices: \"hello, world\" and \"goodbye\"; \"pie cake\" also has two choices because space is the highest-precedence (and only) delimiter.",
        ),
    )

def _parse_choices(message_body):
    for delimiter in ('\n', ';', ',', ' '):
        #see if the delimiter splits anything
        choices = [i for i in (j.strip() for j in message_body.split(delimiter)) if i]
        if len(choices) > 1: #found the most-significant delimiter
            return choices
    else:
        return []

async def handle_message(client, message):
    if message.content.startswith(('!choose ', '!choose\n')):
        choices = _parse_choices(message.content[8:].strip())
        if len(choices) > 1:
            await message.reply(random.choice(choices), mention_author=False)
        else:
            await message.reply("There was nothing to choose between; provide a list separated by spaces, commas, semicolons, or linebreaks.", mention_author=False)
        return True
    return False
