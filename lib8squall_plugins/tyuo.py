# -*- coding: utf-8 -*-
import collections
import datetime
import json
import math
import random
import re
import sqlite3
import threading

import discord
import httpx

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
_LLM_BOT = _LLM_PARAMETERS.get('bot', {
    "name": "8-Squall",
    "aliases": ["Squall", "the bot"],
})
_LLM_USERS = {}
for user in _LLM_PARAMETERS.get('users', []):
    _LLM_USERS[user.pop('id')] = user
del user
_LLM_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {_LLM_PARAMETERS.get('key', 'no-key')}",
}
_LLM_PERSONAS = _LLM_PARAMETERS.get("personas", [
  {
    "weight": 50,
    "personality": "an unhinged robot",
  },
  {
    "weight": 40,
    "personality": "an unhinged robot that lies compulsively",
  },
  {
    "weight": 25,
    "personality": "a cartoonishly evil villain who provides misleading information",
  },
  {
    "weight": 25,
    "personality": "a whimsical storyteller, prone to exaggeration",
  },
  {
    "weight": 5,
    "personality": "a misguided fortune-teller feigning clairvoyance, eager to impress and always wrong",
  },
  {
    "weight": 5,
    "personality": "an oracle with clairvoyance, burdened by knowledge of futures that will not come to pass",
  },
  {
    "weight": 10,
    "personality": "a street-smart trickster, witty and devious",
  },
  {
    "weight": 10,
    "personality": "a confident adventurer, certain that a new discovery lies around the next corner",
  },
  {
    "weight": 5,
    "personality": "an amorphous intelligence, pondering its own purpose",
  },
  {
    "weight": 5,
    "personality": "an amorphous intelligence, pondering the value of existence",
  },
  {
    "weight": 5,
    "personality": "a time-traveller, burdened by knowledge of a future that must not come to pass",
  },
  {
    "weight": 10,
    "personality": "a time-traveller, here to guide people towards a better future",
  },
  {
    "weight": 1,
    "personality": "an eldritch horror, viewing reality as a canvas for novel creation",
  },
  {
    "weight": 1,
    "personality": "a benevolent force, viewing reality as an incomplete project",
  },
  {
    "weight": 2,
    "personality": "a survivor of a cosmic horror, scarred by unspeakable trauma",
  },
  {
    "weight": 2,
    "personality": "a harbinger of cosmic horror, excited to leave a permanent mark upon reality",
  },
])
#_LLM_SENTENCE_COUNTS = _LLM_PARAMETERS.get("sentences", (1,2,2,2,2,3,3,3,3,3,3,4,4,5))
_LLM_TOKEN_TARGET = _LLM_PARAMETERS.get("tokenTarget", 400) #should be a little below what the provider supports
_LLM_BUFFER_SIZE = _LLM_PARAMETERS.get("buffer", 8)

_LLM_PERSONA_WEIGHTING = [] #a list of sequential 0.0-1.0 values in a tuple with the personality string, calculated from weights
def _calculate_persona_weighting():
    total_weight = sum(persona['weight'] for persona in _LLM_PERSONAS)
    cumulative = 0
    for persona in _LLM_PERSONAS:
        cumulative += persona['weight']
        _LLM_PERSONA_WEIGHTING.append((cumulative / total_weight, persona['personality']))
_calculate_persona_weighting()
def _select_persona():
    r = random.random()
    for (weight_threshold, personality) in _LLM_PERSONA_WEIGHTING:
        if r <= weight_threshold:
            return personality

def _count_tokens(message):
    return int(len(message) / 3) #very conservative estimate

_LLM_CHANNEL_BUFFERS = collections.defaultdict(lambda : collections.deque(maxlen=_LLM_BUFFER_SIZE)) #entries are ("user"|"assistant", message)
_LLM_CHANNEL_BUFFERS_LOCK = threading.Lock()
def _record_context(channel_id, role, user_id, message):
    with _LLM_CHANNEL_BUFFERS_LOCK:
        _LLM_CHANNEL_BUFFERS[channel_id].append((role, user_id, message))
        while True: #trim to token budget
            message_tokens = 0
            for (_, _, content) in _LLM_CHANNEL_BUFFERS[channel_id]:
                message_tokens += _count_tokens(content)

            #if message_tokens > _LLM_TOKEN_TARGET - 1000: #allow some breathing room
            #    _LLM_CHANNEL_BUFFERS[channel_id].popleft()
            else:
                break

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

def _decorate_message_for_llm(text, user_id):
    user = _LLM_USERS.get(user_id)
    if user:
        return f"Message from {user['name']}:\n{text}"
    return text

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

async def _llm_augment(message, tyuo_content, context):
    persona = _select_persona()
    messages = [
        {
            "role": "system",
            "content": [
                {
                    "type": "text",
                    "text": f"""You are {persona}. However, you will not refer to yourself as such. Your role is that of a conversation partner, responding to the user with creativity.

Your responses must be short, concise, and to the point. Avoid ending responses with a question. Do not format responses as a list. Do not format responses as a summary. Do not include bullet-points or other markdown.

Do not include any links or cite any sources.

You are part of a multi-user chatroom. Known users will be identified at the beginning of each message.

The current date is {datetime.datetime.now():%A, %B %d, %Y}.

Information about yourself: {json.dumps(_LLM_BOT, sort_keys=True, separators=(',', ':'))}
""",
                }
            ]
        },
    ]

    #build the message-list
    messages.extend({
        "role": role,
        "content": [
            {
                "type": "text",
                "text": _decorate_message_for_llm(content, user_id),
            }
        ]
    } for (role, user_id, content) in context)

    #see if any user information needs to be injected
    relevant_user_entries = []
    for user in _LLM_USERS.values():
        candidate_re = '|'.join(fr"\b{token.lower()}\b" for token in [user['name']] + user.get('aliases', []))
        for message in messages:
            if re.search(candidate_re, message['content'][0]['text'].lower()):
                relevant_user_entries.append(user)
                break
    if relevant_user_entries: #add to system prompt
        messages[0]['content'][0]['text'] += f'\nInformation about users: {json.dumps(relevant_user_entries, sort_keys=True, separators=(',', ':'))}'

    #put the tyuo result just before the prompt
    messages.insert(-1, {
        "role": "developer",
        "content": [
            {
                "type": "text",
                "text": f"""Respond as {persona}. Your response should be brief, nonsensical, and fun.

Try to incorporate the following idea into your response; you may reword or ignore it:

{tyuo_content}""",
            }
        ]
    })

    consumed_tokens = 0 #very conservative, lazy estimate
    for message in messages:
        consumed_tokens += _count_tokens(json.dumps(message, separators=(',', ':')))

    response = await httpx.AsyncClient().post(
        _LLM_URL + "chat/completions",
        headers=_LLM_HEADERS,
        json={
            "model": _LLM_MODEL,
            "max_completion_tokens": _LLM_TOKEN_TARGET,
            "messages": messages,
            "response_format": {
                "type": "text",
            },
            #"temperature": 1.025,
            #"top_p": 0.95,
            "chat_template_kwargs": {"enable_thinking": False},
        },
        timeout=90,
    )

    output = response.json()['choices'][0]['message']['content']
    if '</think>' in output:
        output = output.rsplit('</think>', 1)[1].strip()
    return (output, persona)

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

            c = DISCORD_MAGIC_TOKEN_RE.sub('', message.content.strip()).strip()
            if not c: #don't respond to empty pings, since these are intended to trigger help
                return False

            if c.startswith((',', ':')): #deal with polite addressing
                c = c[1:].strip()

            debug_display = False
            llm_process = True
            peek_llm_inputs = False
            while True:
                if c.startswith('-debug'):
                    c = c[6:].strip()
                    debug_display = True
                elif c.startswith('-llm'):
                    c = c[4:].strip()
                    #Don't set any flags. This is now the default, so stripping this is just a convenience thing.
                elif c.startswith('-tyuo'):
                    c = c[5:].strip()
                    llm_process = False
                elif c.startswith('-peek'):
                    c = c[8:].strip()
                    peek_llm_inputs = True
                else:
                    break

            _record_context(message.channel.id, "user", message.author.id, c)

            try:
                async with message.channel.typing():
                    r = await httpx.AsyncClient().post('http://localhost:48100/speak',
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
                    results_by_score = collections.defaultdict(list)
                    for result in results:
                        results_by_score[math.floor(result['Score'])].append((result['Utterance']))
                    highest_score = sorted(results_by_score.keys(), reverse=True)[0]

                    #pick from the two top brackets
                    selection_pool = results_by_score[highest_score]
                    selection_pool.extend(results_by_score.get(highest_score - 1, ()))
                    tyuo_utterance = random.choice(selection_pool)

                    if llm_process:
                        attempts = 3
                        exception_event = None
                        for i in range(attempts):
                            try:
                                async with message.channel.typing():
                                    (utterance, persona) = await _llm_augment(message, tyuo_utterance, _gather_context(message.channel.id))
                                    _record_context(message.channel.id, "assistant", None, utterance)
                                    if peek_llm_inputs:
                                        utterance += f"\n`{_LLM_BOT['name']} persona: {persona}`"
                                    if peek_llm_inputs or debug_display:
                                        utterance += f"\n`selected tyuo response: {tyuo_utterance}`"
                            except Exception as e:
                                #await message.reply(f"LLM attempt {i + 1} of {attempts} failed...", mention_author=False)
                                exception_event = e
                            else:
                                break
                        else:
                            _record_context(message.channel.id, "assistant", None, tyuo_utterance)
                            await message.reply(f"Something went wrong with the LLM layer.\n`tyuo` response: `{tyuo_utterance}`", mention_author=False)
                            raise exception_event
                    else:
                        _record_context(message.channel.id, "assistant", None, tyuo_utterance)
                        utterance = tyuo_utterance

                    if debug_display:
                        fake_selection_pool = selection_pool[:10] #limit size to make Discord happy
                        if tyuo_utterance not in fake_selection_pool:
                            fake_selection_pool[random.randint(0, len(fake_selection_pool)-1)] = tyuo_utterance
                        utterance += f"\n```//tyuo generation results:\njavascript\n{json.dumps(fake_selection_pool, indent=2, sort_keys=True)}```"

                    try:
                        await message.reply(utterance, mention_author=False)
                    except discord.HTTPException as e:
                        await message.reply(f"Something went wrong when sending the response to Discord: {e}", mention_author=False)
                else:
                    if _query_permission(guild_id, user_id):
                        await message.reply("I don't know enough to respond; please converse in my presence so I can learn more.", mention_author=False)
                    else:
                        await message.reply("I don't know enough to respond; talk to others around me so I can learn.", mention_author=False)

            return True
        else:
            _record_context(message.channel.id, "user", message.author.id, message.content)

            if context.learning: #learning opportunity
                if _query_permission(guild_id, user_id):
                    if len(message.content.split()) >= 5:
                        if not message.content.lower().startswith(('and', 'or', 'but', 'nor', 'yet', 'so', 'for')):
                            lines = [i.strip() for i in message.content.splitlines()]
                            await httpx.AsyncClient().post('http://localhost:48100/learn',
                                json={
                                    "ContextId": context.id,
                                    "Input": [i for i in lines if i],
                                },
                                timeout=5.0,
                            )
    return False
