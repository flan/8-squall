# -*- coding: utf-8 -*-
import json

import requests

def get_help_summary(client, message):
    return (
        "LLM-backed translation",
        (
            "`!tr <message>` to get a simple translation; the input may span multiple lines.",
            "`!translate <message>` will produce a translation with commentary.",
            "While multiple languages are supported for input, only English is supported for output.",
        ),
    )

_LLM_PARAMETERS = json.load(open("./llm-translate.json"))
_LLM_URL = _LLM_PARAMETERS['url']
_LLM_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer no-key",
}

async def _translate(simple, content):
    response = requests.post(
        _LLM_URL + "/v1/chat/completions",
        headers=_LLM_HEADERS,
        data={
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Translate the following into English{scope}:\n\n{content}".format(
                                content=content,
                                scope=(simple and " without adding any commentary or explanations" or ", explaining sub-phrases"),
                            ),
                        }
                    ]
                }
            ]
        },
    )

    return response.json()['choices'][0]['message']['content']

async def handle_message(client, message):
    for pattern in ('!tr ', '!translate '):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern):].strip()
            if subject:
                try:
                    response = await _translate(pattern == '!tr ', subject)
                    if response:
                        await message.reply(response)
                    else:
                        await message.reply("Unable to translate.")
                except Exception:
                    await message.reply("Something didn't go quite right.")
                    raise
            return True
    return False
