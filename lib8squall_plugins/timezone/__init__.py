# -*- coding: utf-8 -*-
import pytz

from . import tzdelta
from . import tzlist

def get_help_summary(client, message):
    return (
        "Timezone-conversion",
        (
            "`!tz <timezone> [timezone...]`, like `!tz edt`, will show the current time in the given timezones.",
            "`!tz <time> <timezone>`, like `!tz 7pm mst`, will give time remaining/elapsed relative to the target value.",
            "Times default to 24h without an `a[m]`/`p[m]` specifier; minutes are optional (colons and dots are recognised as delimiters; values like `730` will be guessed at).",
        ),
    )

async def handle_message(client, message):
    if message.content.startswith('!tz '):
        request = message.content[4:]
        try:
            (target, timezone_mismatch) = tzdelta.parse_timestamp_request(request)
            if target:
                await message.reply(tzdelta.handle_timezone_delta(target, timezone_mismatch), mention_author=False)
            else:
                await message.reply(tzlist.handle_timezone_list(tz.strip() for tz in request.split()), mention_author=False)
        except pytz.exceptions.UnknownTimeZoneError as e:
            await message.reply("Unsupported timezone: `{}`".format(e), mention_author=False)
        return True
    return False
