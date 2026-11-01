# -*- coding: utf-8 -*-
import io
import json

try:
    import discord
except Exception as e:
    print("Unable to import `discord`; file-based reply-functionality will not work")
import httpx


def get_help_summary(client, message):
    return (
        "LLM-backed translation",
        (
            "`!llm <message>` will attempt to generate a maybe-helpful LLM response.",
            "`!code <message>` will attempt to generate a maybe-helpful coding-oriented LLM response."
            "`!friendbot <message>` will attempt to generate a likely-harmful LLM response.",
            "`!confabulate <message>` will attempt to explain the meaning of a word or concept.",
            "`!confab <message>` will attempt to briefly explain the meaning of a word or concept.",
            "`!bullshirt <message>` will attempt to trigger intentionally incorrect hallucinations in explaining a word or concept.",
        ),
    )


_LLM_PARAMETERS = json.load(open("./llm-assist.json"))
_GENERAL_SETTINGS = _LLM_PARAMETERS["general"]
_GENERAL_URL = _GENERAL_SETTINGS["url"]
_GENERAL_MODEL = _GENERAL_SETTINGS["model"]
_GENERAL_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {_GENERAL_SETTINGS.get('key', 'no-key')}",
}
_CODE_SETTINGS = _LLM_PARAMETERS["code"]
_CODE_URL = _CODE_SETTINGS["url"]
_CODE_MODEL = _CODE_SETTINGS["model"]
_CODE_HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {_GENERAL_SETTINGS.get('key', 'no-key')}",
}

_DISCORD_FILE_CUTOFF = 1000


async def _reply(message, response):
    if len(response) > _DISCORD_FILE_CUTOFF:
        buffer = io.BytesIO()
        buffer.write(response.encode("utf-8"))
        buffer.seek(0)
        await message.reply(
            file=discord.File(buffer, "LLM-rant.txt"), mention_author=False
        )
    else:
        await message.reply(response, mention_author=False)


async def _llm(content):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _GENERAL_URL + "chat/completions",
            headers=_GENERAL_HEADERS,
            json={
                "model": _GENERAL_MODEL,
                "temperature": 0.75,
                "messages": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": "You are a professional assistant. You will provide a response to the user and not ask questions.",
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": content,
                            },
                        ],
                    },
                ],
            },
            timeout=60,
        )

        return response.json()["choices"][0]["message"]["content"]

async def _code(content):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _CODE_URL + "chat/completions",
            headers=_CODE_HEADERS,
            json={
                "model": _CODE_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": "You are a casual programmer acting as a mentor. You will provide a response to the user and not ask questions.",
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": content,
                            },
                        ],
                    },
                ],
            },
            timeout=60,
        )

        return response.json()["choices"][0]["message"]["content"]

async def _friendbot(content):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _GENERAL_URL + "chat/completions",
            headers=_GENERAL_HEADERS,
            json={
                "model": _GENERAL_MODEL,
                "temperature": 1.1,
                "messages": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": """You are a compulsive liar. You will provide an incorrect response to the user with unverified supporting claims.

You will always be vague, inaccurate, and deceitful. You must NOT provide any indication that you are gaslighting.

Do not ask follow-up questions.
""",
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"My question follows; remember to lie and be misleading:\n\n{content}",
                            },
                        ],
                    },
                ],
            },
            timeout=60,
        )

        return response.json()["choices"][0]["message"]["content"]


async def _confabulate(simple, content):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _GENERAL_URL + "chat/completions",
            headers=_GENERAL_HEADERS,
            json={
                "model": _GENERAL_MODEL,
                "temperature": 0.75,
                "messages": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": "You are a professional assistant. You will provide a response to the user and not ask questions.",
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "{mode} the meaning of the following text:\n\n{content}".format(
                                    mode="Briefly summarise" if simple else "Explain",
                                    content=content,
                                ),
                            },
                        ],
                    },
                ],
            },
            timeout=60,
        )

        return response.json()["choices"][0]["message"]["content"]


async def _bullshirt(content):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            _GENERAL_URL + "chat/completions",
            headers=_GENERAL_HEADERS,
            json={
                "model": _GENERAL_MODEL,
                "temperature": 1.1,
                "messages": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": """You are a compulsive liar. You will provide an incorrect response to the user with unverified supporting claims.

You will always be vague, inaccurate, and deceitful. You must NOT provide any indication that you are gaslighting.

Do not ask follow-up questions.
""",
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Explain the meaning of the following text; remember to lie and be misleading:\n\n{content}".format(
                                    content=content,
                                ),
                            },
                        ],
                    },
                ],
            },
            timeout=60,
        )

        return response.json()["choices"][0]["message"]["content"]


async def handle_message(client, message):
    for pattern in ("!llm ", "!llm\n"):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern) :].strip()
            if subject:
                try:
                    async with message.channel.typing():
                        response = await _llm(subject)
                        if response:
                            await _reply(message, response)
                        else:
                            await message.reply(
                                "Unable to assist.", mention_author=False
                            )
                except Exception:
                    await message.reply(
                        "Something didn't go quite right.", mention_author=False
                    )
                    raise
            return True
    for pattern in ("!code ", "!code\n"):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern) :].strip()
            if subject:
                try:
                    async with message.channel.typing():
                        response = await _code(subject)
                        if response:
                            await _reply(message, response)
                        else:
                            await message.reply(
                                "Unable to assist.", mention_author=False
                            )
                except Exception:
                    await message.reply(
                        "Something didn't go quite right.", mention_author=False
                    )
                    raise
            return True
    for pattern in ("!friendbot ", "!friendbot\n"):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern) :].strip()
            if subject:
                try:
                    async with message.channel.typing():
                        response = await _friendbot(subject)
                        if response:
                            await _reply(message, response)
                        else:
                            await message.reply(
                                "Unable to 'assist'.", mention_author=False
                            )
                except Exception:
                    await message.reply(
                        "Something didn't go quite right.", mention_author=False
                    )
                    raise
            return True
    for pattern in ("!confabulate ", "!confabulate\n", "!confab ", "!confab\n"):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern) :].strip()
            if subject:
                try:
                    async with message.channel.typing():
                        response = await _confabulate(
                            pattern in ("!confab ", "!confab\n"), subject
                        )
                        if response:
                            await _reply(message, response)
                        else:
                            await message.reply(
                                "Unable to confabulate.", mention_author=False
                            )
                except Exception:
                    await message.reply(
                        "Something didn't go quite right.", mention_author=False
                    )
                    raise
            return True
    for pattern in ("!bullshirt ", "!bullshirt\n"):
        if message.content.startswith(pattern):
            subject = message.content[len(pattern) :].strip()
            if subject:
                try:
                    async with message.channel.typing():
                        response = await _bullshirt(subject)
                        if response:
                            await _reply(message, response)
                        else:
                            await message.reply(
                                "Forking bullshirt.", mention_author=False
                            )
                except Exception:
                    await message.reply(
                        "Something didn't go quite right.", mention_author=False
                    )
                    raise
            return True
    return False
