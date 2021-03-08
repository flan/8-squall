# -*- coding: utf-8 -*-
import merriam_webster.api as mw
import urbandict
import urllib.error

def get_help_summary(client, message):
    return (
        "`!dict[ionary] <word>` to get a definition; alias: `!word`",
        "`!urbandict[ionary] <phrase>` to get a definition; alias: `!udict`",
    )

_MW_API_KEY = open("./m-w.dictionary.key").read().strip()
def _get_merriam_webster(word):
    q = mw.CollegiateDictionary(_MW_API_KEY)
    results = q.lookup(word)
    return {
        result.function: [sense.definition for sense in result.senses]
        for result in results
    }
_DICT_PATTERNS = ('!word ', '!dict ', '!dictionary ')
        
def _get_urban_dictionary(phrase):
    results = urbandict.define(phrase)
    return {
        "slang": [results[0]['def']],
    }
_UDICT_PATTERNS = ('!udict ', '!urbandict ', '!urbandictionary ')

def _format_response(response):
    output = []
    for (kind, definitions) in sorted(response.items()):
        output.append("*{}*".format(kind))
        output.extend(
            "> {}) {}".format(i + 1, definition)
            for (i, definition) in enumerate(definitions)
        )
    return output
    
async def handle_message(client, message):
    for (patternset, handler) in (
        (_DICT_PATTERNS, _get_merriam_webster),
        (_UDICT_PATTERNS, _get_urban_dictionary),
    ):
        for pattern in patternset:
            if message.content.startswith(pattern):
                subject = message.content[len(pattern):].strip()
                if subject:
                    try:
                        response = handler(subject)
                        if response:
                            await message.reply('\n'.join(_format_response(response)))
                        else:
                            await message.reply("No definitions were found.")
                    except urllib.error.HTTPError as e:
                        if e.code == 404:
                            await message.reply("No definitions were found.")
                        else:
                            await message.reply("The dictionary-server had a {} problem.".format(e.code))
                            raise
                    except mw.WordNotFoundException as e:
                        await message.reply(str(e))
                    except Exception:
                        await message.reply("Something didn't go quite right.")
                        raise
                return True
    return False
