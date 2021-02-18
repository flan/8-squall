# -*- coding: utf-8 -*-
from . import tzdelta
from . import tzlist

HELP_SUMMARY = "`!tz <time> <timezone>` or `!tz <timezone> [timezone...]` for time conversion."

async def handle_message(client, message):
    if message.content.startswith('!tz '):
        request = message.content[4:]
        try:
            (target, timezone_mismatch) = _parse_timestamp_request(request)
            if target:
                await message.reply(tzdelta.handle_timezone_delta(target, timezone_mismatch))
            else:
                await message.reply(tzlist.handle_timezone_list(tz.strip() for tz in request.split()))
        except pytz.exceptions.UnknownTimeZoneError as e:
            await message.reply("Unsupported timezone: {}".format(e))
        return True
    return False
