# -*- coding: utf-8 -*-
import merriam_webster.api as mw

import requests

def get_help_summary(client, message):
    return (
        "`!dict[ionary] <word>` to get a definition; alias: `!word`",
        "`!urbandict[ionary] <phrase>` to get a definition; aliases: `!udict`, `!uword`",
    )

_MW_API_KEY = open("./m-w.dictionary.key").read().strip()
def _get_merriam_webster(word):
    q = mw.CollegiateDictionary(_MW_API_KEY)
    return {
        result.function: [sense.definition for sense in result.senses]
        for result in q.lookup(word)
    }
_DICT_PATTERNS = ('!word ', '!dict ', '!dictionary ')
        
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
        if thumbs_up / float(thumbs_down) >= 1.5:
            definitions.append(entry['definition'].replace('[', '').replace(']', ''))
    if definitions:
        return {
            "slang": definitions,
        }
    return None
_UDICT_PATTERNS = ('!udict ', '!uword ' , '!urbandict ', '!urbandictionary ')

def _format_response(response):
    output = []
    for (kind, definitions) in sorted(response.items()):
        output.append("*{}*".format(kind))
        output.extend(
            "> {}) {}".format(i + 1, definition.replace('\n', '\n> '))
            for (i, definition) in enumerate(definitions)
        )
    return output
    
async def handle_message(client, message):
    for (patternset, handler) in (
        (_DICT_PATTERNS, _get_merriam_webster),
        (_UDICT_PATTERNS, _get_urbandictionary),
    ):
        for pattern in patternset:
            if message.content.startswith(pattern):
                subject = message.content[len(pattern):].strip()
                if subject:
                    try:
                        response = handler(subject.lower())
                        if response:
                            await message.reply('\n'.join(_format_response(response)))
                        else:
                            await message.reply("No definitions were found.")
                    except mw.WordNotFoundException as e:
                        await message.reply(str(e))
                    except Exception:
                        await message.reply("Something didn't go quite right.")
                        raise
                return True
    return False
