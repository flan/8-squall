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
_LLM_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer no-key",
}

_CHANNEL_BUFFERS = collections.defaultdict(lambda : collections.deque(maxlen=5))
_CHANNEL_BUFFERS_LOCK = threading.Lock()

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

async def _llm_augment(tyuo_content, prompt, context):
    if context:
        context = "Use these messages to inform context:\n\n{context}".format(
            context='\n\n\n'.join(context),
        )
    else:
        context=''

    response = requests.request(
        "POST",
        _LLM_URL,
        headers=_LLM_HEADERS,
        params={
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Provide a tangential response that incorporates the following idea: {tyuo_content}{context}".format(
                                tyuo_content=tyuo_content,
                                context=context,
                            ),
                        }
                    ]
                }
            ]
        },
    )

    return response.json()['choices'][0]['message']['content']

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
                    await message.reply("You are currently teaching the chatbot on this server. Thank you!\nIf you want to stop, use `!tyuo disable`.")
                else:
                    await message.reply("You are not currently teaching the chatbot on this server.\nIf you want to start, use `!tyuo enable`.")
            elif content == 'enable':
                _grant_permission(guild_id, user_id)
                await message.reply("Thank you for opting in to teaching the chatbot; use `!tyuo status` if you forget that you did this.")
            elif content == 'disable':
                _revoke_permission(guild_id, user_id)
                await message.reply("Done. You're no longer teaching the chatbot; use `!tyuo status` if you forget that you did this.")
                
            return True
        elif client.user in message.mentions: #speak request
            if not context.responding:
                return False
                
            c = message.content

            debug_display = False
            llm_process = False
            if ' --debug' in message.content:
                c = c.replace(' --debug', '')
                debug_display = True
            if ' --llm' in message.content:
                c = c.replace(' --llm', '')
                llm_process = True

            c = DISCORD_MAGIC_TOKEN_RE.sub('', c.strip())
            if not c: #don't respond to empty pings, since these are intended to trigger help
                return False
                
            try:
                r = requests.post('http://localhost:48100/speak',
                    json={
                        "ContextId": context.id,
                        "Input": c,
                    },
                    timeout=5.0,
                )
                results = r.json()
            except Exception:
                await message.reply("Something went wrong. The chatbot might be down.")
                raise
            else:
                if results:
                    if debug_display:
                        await message.reply("""```javascript
{}
```""".format(json.dumps(["{:.2f}: {}".format(r['Score'], r['Utterance']) for r in results], indent=2)))
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
                            with _CHANNEL_BUFFERS_LOCK:
                                channel_history = tuple(_CHANNEL_BUFFERS[message.channel.id])
                            utterance = await _llm_augment(utterance, c, channel_history)

                        await message.reply(utterance)
                else:
                    if _query_permission(guild_id, user_id):
                        await message.reply("I don't know enough to respond; please converse in my presence so I can learn more.")
                    else:
                        await message.reply("I don't know enough to respond; talk to others around me so I can learn.")
                        
            return True
        else:
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

            with _CHANNEL_BUFFERS_LOCK:
                _CHANNEL_BUFFERS[message.channel.id].append(message.content)
    return False
