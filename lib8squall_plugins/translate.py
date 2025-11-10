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
_LLM_MODEL = _LLM_PARAMETERS['model']
_LLM_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {_LLM_PARAMETERS.get('key', 'no-key')}",
}

async def _translate(simple, content):
    response = requests.post(
        _LLM_URL + "chat/completions",
        headers=_LLM_HEADERS,
        data={
            "model": _LLM_MODEL,
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
                        },
                    ],
                },
            ],
        },
    )

    return response.json()['choices'][0]['message']['content']

async def handle_message(client, message):
    for pattern in ('!tr ', '!tr\n', '!translate ', '!translate\n'):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern):].strip()
            if subject:
                try:
                    response = await _translate(pattern in ('!tr ', '!tr\n'), subject)
                    if response:
                        await message.reply(response)
                    else:
                        await message.reply("Unable to translate.")
                except Exception:
                    await message.reply("Something didn't go quite right.")
                    raise
            return True
    return False
