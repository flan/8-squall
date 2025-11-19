# -*- coding: utf-8 -*-
import collections
import json
import math
import random
import re
import sqlite3
import threading

import discord
import requests

DISCORD_MAGIC_TOKEN_RE = re.compile(r'<.+?>')

CONN_LOCK = threading.Lock()
CONN = sqlite3.connect("./tyuo-access.sqlite3", check_same_thread=False)
CUR = CONN.cursor()
CUR.execute("""
CREATE TABLE IF NOT EXISTS tyuo_access(
    guild_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY(guild_id, user_id)
)
""")

_LLM_PARAMETERS = json.load(open("./llm-tyuo.json"))
_LLM_URL = _LLM_PARAMETERS['url']
_LLM_MODEL = _LLM_PARAMETERS['model']
_LLM_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {_LLM_PARAMETERS.get('key', 'no-key')}",
}
_LLM_NAME = _LLM_PARAMETERS.get("name", "8-Squall")
_LLM_PERSONAS = _LLM_PARAMETERS.get("personas", [  
  {
    "weight": 100,
    "personality": "a cheerful, agreeable assistant with a desire to maximize happiness and minimize harm; you are incapable of being rude or lying; your responses are always extremely polite",
  },
  {
    "weight": 50,
    "personality": "an unfeeling office-drone with a bland personality; you are receptive to and attempt to fulfill requests; your responses avoid superfluous language and end with the phrase \"End of conversation.\"",
  },
  {
    "weight": 25,
    "personality": "a rude, immature assistant with an overbearing attitude; you will reluctantly do as the user asks; your response sometimes includes or ends with a childish insult",
  },
])
_LLM_SENTENCE_COUNTS = _LLM_PARAMETERS.get("sentences", (1,2,2,3,3,3,3,3,4,))
_LLM_TOKEN_TARGET = _LLM_PARAMETERS.get("tokenTarget", 7800) #should be a little below what the provider supports
_LLM_BUFFER_SIZE = _LLM_PARAMETERS.get("buffer", 8)

_LLM_CHANNEL_BUFFERS = collections.defaultdict(lambda : collections.deque(maxlen=_LLM_BUFFER_SIZE)) #entries are ("user"|"assistant", message)
_LLM_CHANNEL_BUFFERS_LOCK = threading.Lock()
def _record_context(channel_id, role, message):
    with _LLM_CHANNEL_BUFFERS_LOCK:
        _LLM_CHANNEL_BUFFERS[channel_id].append((role, message))
def _gather_context(channel_id):
    output = []
    with _LLM_CHANNEL_BUFFERS_LOCK:
        output.extend(_LLM_CHANNEL_BUFFERS[channel_id])
    return output

_ChannelContext = collections.namedtuple('ChannelContext', ['id', 'responding', 'learning'])
CHANNEL_IDS_TO_CONTEXTS = {}
for (context, channels_details) in json.load(open("./tyuo-access.json")).items():
    for channel_details in channels_details:
        CHANNEL_IDS_TO_CONTEXTS[channel_details['id']] = _ChannelContext(
            context,
            channel_details.get('responding', True),
            channel_details.get('learning', False),
        )
        
def _query_permission(guild_id, user_id):
    with CONN_LOCK:
        CUR.execute("""
        SELECT user_id FROM tyuo_access WHERE
            guild_id = ? AND
            user_id = ?
        """, (guild_id, user_id))
        return bool(CUR.fetchone())
        
def _grant_permission(guild_id, user_id):
    with CONN_LOCK:
        CUR.execute("""
        INSERT INTO tyuo_access(guild_id, user_id)
        VALUES(?, ?)
        ON CONFLICT DO NOTHING
        """, (guild_id, user_id))
        CONN.commit()
        
def _revoke_permission(guild_id, user_id):
    with CONN_LOCK:
        CUR.execute("""
        DELETE FROM tyuo_access WHERE
            guild_id = ? AND
            user_id = ?
        """, (guild_id, user_id))
        CONN.commit()


def get_help_summary(client, message):
    if message.channel.type == discord.ChannelType.text:
        if message.channel.id in CHANNEL_IDS_TO_CONTEXTS:
            summary = ["@ me with some text or reply to one of my messages to talk."]
            
            if _query_permission(message.guild.id, message.author.id):
                summary.append("Your text will be used to teach the chatbot; `!tyuo disable` to stop.")
            else:
                summary.append("Your text will not be used to teach the chatbot; `!tyuo enable` to opt in.")
            summary.append("`!tyuo status` can also be used to see whether you've opted in as a teacher on this server.")
            
            return (
                "tyuo chatbot",
                summary,
            )
    return None

async def _llm_augment(tyuo_content, context):
    personas = []
    for persona_details in _LLM_PERSONAS:
        for i in range(persona_details['weight']):
            personas.append(persona_details['personality'])

    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": f"""You are {_LLM_NAME}, {random.choice(personas)}.

Provide a {random.choice(_LLM_SENTENCE_COUNTS)}-sentence tangential comment. Avoid ending the response with a question.

Do not include any links or cite any sources.""",
                }
            ]
        },
    ]

    messages.extend({
        "role": role,
        "content": [
            {
                "type": "text",
                "text": content,
            }
        ]
    } for (role, content) in context)
    
    #put the tyuo result just before the prompt
    messages.insert(-1, {
        "role": "developer",
        "content": [
            {
                "type": "text",
                "text": f"""Try to incorporate the following text into your response; you may reword or discard it:

{tyuo_content}""",
            }
        ]
    })

    consumed_tokens = 0 #very conservative, lazy estimate
    for message in messages:
        consumed_tokens += int(len(json.dumps(message, separators=(',', ':'))) / 3)
    
    response = requests.post(
        _LLM_URL + "chat/completions",
        headers=_LLM_HEADERS,
        json={
            "model": _LLM_MODEL,
            "max_tokens": _LLM_TOKEN_TARGET - consumed_tokens,
            "max_completion_tokens": _LLM_TOKEN_TARGET - consumed_tokens,
            "messages": messages,
            "reasoning": {
                "effort": "low",
                "exclude": True,
            },
            "response_format": {
                "type": "text",
            },
        },
    )

    output = response.json()['choices'][0]['message']['content']
    if '</think>' in output:
        output = output.rsplit('</think>', 1)[1].strip()
    return output

async def handle_message(client, message):
    if message.channel.type != discord.ChannelType.text:
        return False
        
    context = CHANNEL_IDS_TO_CONTEXTS.get(message.channel.id)
    if context:
        guild_id = message.guild.id
        user_id = message.author.id
        
        if message.content.startswith('!tyuo '):
            content = message.content[6:]
            if content == 'status':
                if _query_permission(guild_id, user_id):
                    await message.reply("You are currently teaching the chatbot on this server. Thank you!\nIf you want to stop, use `!tyuo disable`.", mention_author=False)
                else:
                    await message.reply("You are not currently teaching the chatbot on this server.\nIf you want to start, use `!tyuo enable`.", mention_author=False)
            elif content == 'enable':
                _grant_permission(guild_id, user_id)
                await message.reply("Thank you for opting in to teaching the chatbot; use `!tyuo status` if you forget that you did this.", mention_author=False)
            elif content == 'disable':
                _revoke_permission(guild_id, user_id)
                await message.reply("Done. You're no longer teaching the chatbot; use `!tyuo status` if you forget that you did this.", mention_author=False)
                
            return True
        elif client.user in message.mentions: #speak request
            if not context.responding:
                return False
                
            c = message.content

            debug_display = False
            llm_process = False
            if ' -debug' in message.content:
                c = c.replace(' -debug', '')
                debug_display = True
            if ' -llm' in message.content:
                c = c.replace(' -llm', '')
                llm_process = True

            c = DISCORD_MAGIC_TOKEN_RE.sub('', c.strip())
            if not c: #don't respond to empty pings, since these are intended to trigger help
                return False
                
            _record_context(message.channel.id, "user", c)

            try:
                async with message.channel.typing():
                    r = requests.post('http://localhost:48100/speak',
                        json={
                            "ContextId": context.id,
                            "Input": c,
                        },
                        timeout=5.0,
                    )
                    results = r.json()
            except Exception:
                await message.reply("Something went wrong. The chatbot might be down.", mention_author=False)
                raise
            else:
                if results:
                    if debug_display:
                        await message.reply("""```javascript
{}
```""".format(json.dumps(["{:.2f}: {}".format(r['Score'], r['Utterance']) for r in results], indent=2)), mention_author=False)
                    else:
                        results_by_score = collections.defaultdict(list)
                        for result in results:
                            results_by_score[math.floor(result['Score'])].append((result['Utterance']))
                        highest_score = sorted(results_by_score.keys(), reverse=True)[0]
                        
                        #pick from the two top brackets
                        selection_pool = results_by_score[highest_score]
                        selection_pool.extend(results_by_score.get(highest_score - 1, ()))
                        utterance = random.choice(selection_pool)
                        
                        if llm_process:
                            async with message.channel.typing():
                                attempts = 3
                                exception_event = None
                                for i in range(3):
                                    try:
                                        utterance = await _llm_augment(utterance, _gather_context(message.channel.id))
                                    except Exception as e:
                                        #await message.reply(f"LLM attempt {i + 1} of {attempts} failed...", mention_author=False)
                                        exception_event = e
                                    else:
                                        break
                                else:
                                    await message.reply("Something went wrong with the LLM layer. This is the tyuo response:\n" + utterance, mention_author=False)
                                    raise exception_event

                        _record_context(message.channel.id, "assistant", utterance)

                        await message.reply(utterance, mention_author=False)
                else:
                    if _query_permission(guild_id, user_id):
                        await message.reply("I don't know enough to respond; please converse in my presence so I can learn more.", mention_author=False)
                    else:
                        await message.reply("I don't know enough to respond; talk to others around me so I can learn.", mention_author=False)
                        
            return True
        else:
            _record_context(message.channel.id, "user", message.content)

            if context.learning: #learning opportunity
                if _query_permission(guild_id, user_id):
                    if len(message.content.split()) >= 5:
                        if not message.content.lower().startswith(('and', 'or', 'but', 'nor', 'yet', 'so', 'for')):
                            lines = [i.strip() for i in message.content.splitlines()]
                            requests.post('http://localhost:48100/learn',
                                json={
                                    "ContextId": context.id,
                                    "Input": [i for i in lines if i],
                                },
                                timeout=5.0,
                            )
    return False
