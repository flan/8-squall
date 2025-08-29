# -*- coding: utf-8 -*-
import requests

def get_help_summary(client, message):
    return (
        "Urban Dictionary-lookup",
        (
            "`!udict <word>` to get a definition.",
            "Lookups are performed using an unstable API that may be intermittently unavailable; only one word is evaluated.",
            "Aliases: `!urbandictionary`, `!urbandict`, `!uword`",
        ),
    )

_URBAN_DICTIONARY_URL = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
_URBAN_DICTIONARY_HEADERS = {
    'x-rapidapi-key': open("./rapidapi.ud.key").read().strip(),
    'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
}
def _get_urbandictionary(phrase):
    response = requests.request(
        "GET",
        _URBAN_DICTIONARY_URL,
        headers=_URBAN_DICTIONARY_HEADERS,
        params={"term": phrase},
    )
    
    definitions = []
    for entry in response.json()['list']:
        thumbs_up = entry['thumbs_up']
        thumbs_down = entry['thumbs_down']
        if thumbs_down < 10:
            if thumbs_up < 25:
                continue
        elif thumbs_up / float(thumbs_down) < 1.5:
            continue
        definitions.append((thumbs_up, thumbs_down, entry['definition'].replace('[', '').replace(']', '')))
    if definitions:
        return {
            "slang": definitions,
        }
    return None

def _format_response(response):
    output = []
    for (kind, definitions) in sorted(response.items()):
        output.append("*{}*".format(kind))
        output.extend(
            "> {}) ||{}|| | 👍 {} | 👎 {}".format(i + 1, definition.replace('\n', '\n> '), thumbs_up, thumbs_down)
            for (i, (thumbs_up, thumbs_down, definition,)) in enumerate(sorted(definitions, reverse=True))
        )
        
    return output
    
async def handle_message(client, message):
    for pattern in ('!udict ', '!uword ', '!urbandict ', '!urbandictionary '):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern):].strip()
            if subject:
                try:
                    response = _get_urbandictionary(subject.lower())
                    if response:
                        await message.reply('\n'.join(_format_response(response)))
                    else:
                        await message.reply("No definitions were found.")
                except Exception:
                    await message.reply("Something didn't go quite right.")
                    raise
            return True
    return False
