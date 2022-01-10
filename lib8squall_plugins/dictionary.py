# -*- coding: utf-8 -*-
import merriam_webster.api as mw

def get_help_summary(client, message):
    return (
        "Dictionary-lookup",
        (
            "`!dict <word>` to get a definition.",
            "Lookups are performed against Merriam-Webster, so only a single word is evaluated.",
            "Aliases: `!dictionary`, `!word`",
        ),
    )

_MW_API_KEY = open("./m-w.dictionary.key").read().strip()
def _get_merriam_webster(word):
    q = mw.CollegiateDictionary(_MW_API_KEY)
    return {
        result.function: [sense.definition for sense in result.senses if sense.definition]
        for result in q.lookup(word)
        if result.function
    }

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
    for pattern in ('!word ', '!dict ', '!dictionary '):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern):].strip()
            if subject:
                try:
                    response = _get_merriam_webster(subject.split()[0].lower())
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
