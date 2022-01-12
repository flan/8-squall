# -*- coding: utf-8 -*-
import datetime
import sqlite3
import threading
import time

from typing import Iterable, List, Union

import discord
import dateparser
import humanize
import validators


def get_help_summary(client: discord.Client, message: discord.message):
    return (
        "Reminders",
        (
            "`!remember <description> [(on <day>|in <offset>)]` adds a reminder, optionally also anchoring a timestamp.",
            "There is a reasonable effort to guess intended time from natural language, like `!remind eat a food in 3 days` or `!remind take a shower on feb 18th`.",
            "If you specify a more ISO-like timestamp, timezones and offsets are processed and the date-format is DMY or YMD, not the American MDY; all absolute timestamps assume {} if unspecified.".format(datetime.datetime.now().astimezone().tzinfo),
            "`!recall [text]` will list all reminders, optionally filtered by the given text. When using DMs, all reminders are displayed; when using this within a server, only reminders set on that server will be displayed.",
            "`!forget <ids> [ids]` removes the enumerated reminders. IDs may be delimited by commas or a range can be supplied, like `1,3-5`.",
            "Please be aware that these reminders are not stored securely. Do not trust this system to store private or essential information.",
        ),
    )

CONN_LOCK: threading.Lock = threading.Lock()
CONN: sqlite3.Connection = sqlite3.connect("./reminders.sqlite3", check_same_thread=False)
CUR: sqlite3.Cursor = CONN.cursor()
CUR.execute("""CREATE TABLE IF NOT EXISTS reminders(
    id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    guild_id INTEGER,
    recorded_timestamp INTEGER NOT NULL,
    description TEXT NOT NULL,
    context_url TEXT,
    relevant_timestamp INTEGER,
    PRIMARY KEY(id)
)""")

def _enumerate_reminders(user_id: int, guild_id: int):
    with CONN_LOCK:
        if guild_id is None:
            CUR.execute("""SELECT id, recorded_timestamp, description, context_url, relevant_timestamp FROM reminders
                WHERE user_id = ?
                ORDER BY relevant_timestamp ASC NULLS LAST, recorded_timestamp ASC, id ASC
            """, (user_id,))
        else:
            CUR.execute("""SELECT id, recorded_timestamp, description, context_url, relevant_timestamp FROM reminders
                WHERE user_id = ?
                  AND guild_id = ?
                ORDER BY relevant_timestamp ASC NULLS LAST, recorded_timestamp ASC, id ASC
            """, (user_id, guild_id))
        return CUR.fetchall()

def _add_reminder(user_id: int, guild_id: int, description: str, context_url: Union[str, type(None)], relevant_timestamp: Union[int, type(None)]):
    with CONN_LOCK:
        with CONN:
            CUR.execute("""INSERT INTO reminders(user_id, guild_id, recorded_timestamp, description, context_url, relevant_timestamp)
                VALUES(?, ?, ?, ?, ?, ?)
            """, (user_id, guild_id, int(time.time()), description, context_url, relevant_timestamp,))

def _delete_reminders(user_id: int, guild_id: int, reminder_ids: Iterable):
    parsed_reminder_ids = []
    for reminder_id in reminder_ids:
        for token in reminder_id.split(','):
            try:
                (range_start, range_end) = token.split('-', 1)
                parsed_reminder_ids.extend(range(int(range_start), int(range_end) + 1))
            except ValueError:
                parsed_reminder_ids.append(int(token))
                
    if not parsed_reminder_ids:
        return
        
    reminders = _enumerate_reminders(user_id, guild_id)
    resolved_reminder_ids = []
    for reminder_id in parsed_reminder_ids:
        resolved_reminder_ids.append(str(reminders[reminder_id - 1][0])) #1-indexed
        
    with CONN_LOCK:
        with CONN:
            CUR.execute("""DELETE FROM reminders
                WHERE id IN ({})
            """.format(','.join(resolved_reminder_ids)))

def _prepare_reminders(user_id: int, guild_id: int, filter_text: Union[str, type(None)]):
    chunks = []
    chunk = ''
    
    if filter_text is not None:
        filter_text = filter_text.lower()
        
    for (i, (_, recorded_timestamp, description, context_url, relevant_timestamp)) in enumerate(_enumerate_reminders(user_id, guild_id)):
        if filter_text is not None: #filtering is done here to ensure the reminder-ID is usable for deletion
            if filter_text not in description.lower():
                continue
                
        current_time = datetime.datetime.now()
        new_chunk = "{}) {}\n> Recorded {}".format(
            i + 1, #1-indexed
            description,
            humanize.naturaltime(
                current_time - datetime.datetime.fromtimestamp(recorded_timestamp),
            ),
        )
        
        if relevant_timestamp is not None:
            new_chunk += "; relevant {}\n".format(
                humanize.naturaltime(
                    datetime.datetime.now() - datetime.datetime.fromtimestamp(relevant_timestamp),
                ),
            )
        else:
            new_chunk += '\n'
            
        if context_url is not None:
            new_chunk += "> <{}>\n".format(context_url)
            
        if len(chunk) + len(new_chunk) < 2000:
            chunk += new_chunk #+ '\n'
        else:
            chunks.append(chunk)
            chunk = new_chunk #+ '\n'
    if chunk:
        chunks.append(chunk)
        
    return chunks

def _parse_reminder(reminder: str):
    timestamp = None
    
    for time_delimiter in (' in ', ' on '):
        if time_delimiter in reminder:
            (sliced_description, timestring) = reminder.rsplit(time_delimiter, 1)
            
            parsed_timestamp = dateparser.parse(
                time_delimiter + timestring,
                languages=['en'],
                settings={
                    'DATE_ORDER': 'DMY',
                    'PREFER_DAY_OF_MONTH': 'first',
                },
            )
            
            if parsed_timestamp is not None:
                timestamp = int(parsed_timestamp.timestamp())
                description = sliced_description
                break
    else:
        description = reminder
        
    return (description.strip(), timestamp)


async def handle_message(_: discord.Client, message: discord.message):
    if message.content.startswith('!recall'):
        content = message.content[7:]
        if content:
            if content[0] == ' ': #filtering requested
                filter_text = content.strip()
            else: #not a match for this plugin
                return False
        else:
            filter_text = None
            
        if message.guild:
            guild_id = message.guild.id
        else:
            guild_id = None
            
        reminders = _prepare_reminders(message.author.id, guild_id, filter_text)
        if reminders:
            for reminder in reminders:
                await message.reply(reminder)
        else:
            await message.reply("There are no relevant reminders to display.")
            
        return True
        
    try:
        if message.content.startswith('!remember '):
            (description, timestamp) = _parse_reminder(message.content[10:])
            
            if message.guild:
                guild_id = message.guild.id
            else:
                guild_id = None
                
            _add_reminder(message.author.id, guild_id, description, message.jump_url, timestamp)
            
            await message.add_reaction('\N{THUMBS UP SIGN}')
            
            return True
        
        if message.content.startswith('!forget '):
            if message.guild:
                guild_id = message.guild.id
            else:
                guild_id = None
                
            _delete_reminders(message.author.id, guild_id, message.content.split()[1:])
            
            await message.add_reaction('\N{THUMBS UP SIGN}')
            
            return True
            
    except Exception as e:
        print("reminder error for {}, '{}': {}".format(message.author.name, message.content, e))
        await message.add_reaction('\N{THUMBS DOWN SIGN}')
        return True
        
    return False
