# -*- coding: utf-8 -*-
import random

def get_help_summary(client, message):
    return ("@ me and include a question-mark to get an 8-ball response.",)

_RESPONSES_8SQUALL = (
 "Meh.",
 "Whatever.",
 "Go away.",
 "...",
 "You're on your own.",
 "Leave me alone.",
 "Just give up.",
 "My sources say '...'",
 "All signs point to 'whatever'.",
)

_RESPONSES_8BALL = (
 "Don't count on it.",
 "Most certainly.",
 "Probably.",
 "My sources say no.",
 "No.",
 "The outlook is promising.",
 "The outlook is bleak.",
 "All signs point to yes.",
 "As I see it, yes.",
 "Based on all I know, no.",
 "You're better off not knowing.",
)

async def handle_message(client, message):
    if '?' in message.content and client.user in message.mentions:
        if random.randint(0, 2) == 2: #33% chance of getting Squall
            response = random.choice(_RESPONSES_8SQUALL)
        else:
            response = "The 8-Ball has concluded: {}".format(random.choice(_RESPONSES_8BALL))
        await message.reply(response)
        return True
    return False
