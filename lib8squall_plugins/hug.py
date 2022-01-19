# -*- coding: utf-8 -*-
import sqlite3
import threading

from typing import Iterable, List

import discord
import validators


#HACK: simple hug-permissions ACL
_HUGGERS = [int(id) for id in (line.strip() for line in open('./hugs.acl', 'r')) if id]


def get_help_summary(client: discord.Client, message: discord.message):
    summary = ["`!hug` to get a (hopefully) nice hug from a robot."]
    
    if message.channel.type == discord.ChannelType.private and message.author.id in _HUGGERS:
        summary.append("`!hugadd <url> [url...]` to add new hug images to the database; these URLs should be permalinks.")
        summary.append("`!hugdel <url> [url...]` to remove hug images from the database.")
        
    return (
        "Hugs",
        summary,
    )


INITIAL_HUGS: List = [
    "https://media.giphy.com/media/dQj2Cp0Gw8uLC/giphy.gif",
    "https://media.giphy.com/media/3M4NpbLCTxBqU/giphy.gif",
    "https://media.giphy.com/media/yidUzriaAGJbsxt58k/giphy.gif",
    "https://media.giphy.com/media/ZBQhoZC0nqknSviPqT/giphy.gif",
    "https://media.giphy.com/media/VbawWIGNtKYwOFXF7U/giphy.gif",
    "https://media.giphy.com/media/llmZp6fCVb4ju/giphy.gif",
    "https://media.giphy.com/media/EvYHHSntaIl5m/giphy.gif",
    "https://media.giphy.com/media/wsSssszJkPBYs/giphy.gif",
    "https://media.giphy.com/media/QbkL9WuorOlgI/giphy.gif",
    "https://media.giphy.com/media/117o9BJASzmLNC/giphy.gif",
    "https://media.giphy.com/media/8tpiC1JAYVMFq/giphy.gif",
    "https://media.giphy.com/media/xUOwGdD7RGT4CTnUaY/giphy.gif",
    "https://media.giphy.com/media/l4q7Z7ycv6YqX7fr2/giphy.gif",
    "https://media.giphy.com/media/L39JgFH6sDjJfJ72na/giphy.gif",
]
CONN_LOCK: threading.Lock = threading.Lock()
CONN: sqlite3.Connection = sqlite3.connect("./hugs.sqlite3", check_same_thread=False)
CUR: sqlite3.Cursor = CONN.cursor()
with CONN:
    CUR.execute("""CREATE TABLE IF NOT EXISTS hugs(
        id INTEGER NOT NULL,
        submitter INTEGER DEFAULT NULL,
        url TEXT NOT NULL,
        PRIMARY KEY(id),
        UNIQUE(url)
    )""")


def _insert_hugs(user_id: int, urls: Iterable):
    """Add the given list of hugs."""
    with CONN_LOCK:
        with CONN:
            for url in urls:
                CUR.execute(
                    """
                INSERT OR IGNORE INTO hugs(submitter, url)
                VALUES(?, ?)
                """,
                    (user_id, url,),
                )

# Setup initial hugs list.
_insert_hugs(None, INITIAL_HUGS)


def _delete_hugs(urls: Iterable):
    """Delete the given list of hugs."""

    with CONN_LOCK:
        with CONN:
            for url in urls:
                CUR.execute(
                    """
                DELETE FROM hugs WHERE
                    url = ?
                """,
                    (url,),
                )


def _get_random_hug():
    """Fetch and return a random hug url."""
    with CONN_LOCK:
        CUR.execute(
            """
        SELECT url
        FROM hugs
        ORDER BY RANDOM()
        LIMIT 1
        """
        )
        return CUR.fetchone()[0]


def _validate_urls(message_content: str):
    """Checks if the given urls in a message are formatted properly."""

    given_urls = message_content.rstrip().split(" ")[1:]
    bad_urls = set()
    good_urls = set()
    for url in given_urls:
        valid = validators.url(url)
        if valid:
            good_urls.add(url)
        else:
            bad_urls.add(url)

    return good_urls, bad_urls


async def handle_message(_: discord.Client, message: discord.message):
    if message.channel.type == discord.ChannelType.private:
        if message.content.startswith("!hugadd ") and message.author.id in _HUGGERS:
            valid_urls, bad_urls = _validate_urls(message.content)
            if bad_urls:
                response = "Oh no, you had invalid URLs in there! Fix them and try again:\n  {}".format(
                    "\n  ".join(bad_urls)
                )
                await message.reply(response)
                return True
            _insert_hugs(message.author.id, valid_urls)
            response = "I've added {} new hugs - if they weren't already there!".format(
                len(valid_urls)
            )
            await message.reply(response)
            return True

        if message.content.startswith("!hugdel ") and message.author.id in _HUGGERS:
            valid_urls, bad_urls = _validate_urls(message.content)
            if bad_urls:
                response = "Oh no, you had invalid URLs in there! Fix them and try again:\n  {}".format(
                    "\n  ".join(bad_urls)
                )
                await message.reply(response)
                return True
            _delete_hugs(valid_urls)
            response = "I've deleted {} hugs - if they existed!".format(len(valid_urls))
            await message.reply(response)
            return True

    if message.content.strip() == "!hug":
        await message.reply(_get_random_hug())
        return True

    return False
