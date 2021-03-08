# -*- coding: utf-8 -*-
import PyDictionary

def get_help_summary(client, message):
    return (
        "`!dict[ionary] <word> [word...]` to get definitions",
        "`!syn[onyms] <word> [word...]` to get synonyms",
        "`!ant[onyms] <word> [word...]` to get antonyms",
    )

_DICT_PATTERNS = ('!dict ', '!dictionary ')
_SYN_PATTERNS = ('!syn ', '!synonyms ')
_ANT_PATTERNS = ('!ant ', '!antonyms ')

def _dict_format_definition(definitions):
    output = []
    for (i, d) in enumerate(definitions[:3]):
        output.append("> {}) {}".format(i + 1, d))
    if len(definitions) > 3:
        output.append("> *additional definitions not shown*")
    return output
    
def _dict(tokens):
    d = PyDictionary.PyDictionary()
    output = []
    for token in tokens:
        try:
            details = d.meaning(token)
        except Exception:
            output.append("{}: no definitions found".format(token))
        else:
            if details:
                for (kind, definitions) in sorted(details.items()):
                    output.append("{} *{}*".format(token, kind))
                    if definitions:
                        output.extend(_dict_format_definition(definitions))
                    else:
                        output.append("> no definitions found")
            else:
                output.append("{}: no definitions found".format(token))
    return output
    
def _syn(tokens):
    d = PyDictionary.PyDictionary()
    output = []
    for token in tokens:
        try:
            details = d.synonym(token)
        except Exception:
            output.append("{}: no synonyms found".format(token))
        else:
            if details:
                output.append("{}: {}".format(token, ', '.join(details)))
            else:
                output.append("{}: no synonyms found".format(token))
    return output
    
def _ant(tokens):
    d = PyDictionary.PyDictionary()
    output = []
    for token in tokens:
        try:
            details = d.antonym(token)
        except Exception:
            output.append("{}: no antonyms found".format(token))
        else:
            if details:
                output.append("{}: {}".format(token, ', '.join(details)))
            else:
                output.append("{}: no antonyms found".format(token))
    return output
    
    
async def handle_message(client, message):
    for (patternset, handler) in (
        (_DICT_PATTERNS, _dict),
        (_SYN_PATTERNS, _syn),
        (_ANT_PATTERNS, _ant),
    ):
        for pattern in patternset:
            if message.content.startswith(pattern):
                tokens = message.content[len(pattern):].split()
                if tokens:
                    response = handler(tokens)
                    if response:
                        await message.reply('\n'.join(response))
                    else:
                        await message.reply("I wasn't able to find anything useful.")
                return True
    return False
