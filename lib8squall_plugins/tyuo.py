# -*- coding: utf-8 -*-
import json
import threading
import sqlite3

import discord
import requests


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

CHANNEL_IDS_TO_CONTEXTS = {}
for (context, channel_ids) in json.load(open("./tyuo-access.json")).items():
    for channel_id in channel_ids:
        CHANNEL_IDS_TO_CONTEXTS[channel_id] = context
        
        
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
    if message.channel.type != discord.ChannelType.text:
        return ()
    responses = ["@ me to talk; `!tyuo status` to see whether you've opted in as a teacher."]
    if message.channel.id in CHANNEL_IDS_TO_CONTEXTS:
        if _query_permission(message.guild.id, message.author.id):
            responses.append("`!tyuo disable` to stop teaching the chatbot.")
        else:
            responses.append("`!tyuo enable` to start teaching the chatbot.")
    return responses
    
    
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
            try:
                r = requests.post('http://localhost:48100/speak',
                    json={
                        "ContextId": context,
                        "Input": message.content,
                    },
                    timeout=5.0,
                )
                results = r.json()
            except Exception:
                await message.reply("Something went wrong. The chatbot might be down.")
                raise
            else:
                if results:
                    await message.reply(results[0]['Utterance'])
                else:
                    if _query_permission(guild_id, user_id):
                        await message.reply("I don't know enough to respond; please converse in my presence so I can learn more.")
                    else:
                        await message.reply("I don't know enough to respond; use `!tyuo enable` to help me learn.")
                        
            return True
        else: #learning opportunity
            if _query_permission(guild_id, user_id):
                if len(message.content) > 20:
                    if not message.content.lower().startswith(('and', 'or', 'but', 'nor', 'yet', 'so', 'for')):
                        lines = [i.strip() for i in message.content.splitlines()]
                        requests.post('http://localhost:48100/learn',
                            json={
                                "ContextId": context,
                                "Input": [i for i in lines if i],
                            },
                            timeout=5.0,
                        )
    return False
