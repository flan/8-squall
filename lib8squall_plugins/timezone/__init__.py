# -*- coding: utf-8 -*-
import collections
import datetime
import re
import time

import pytz

HELP_SUMMARY = "`!tz <time> <timezone>` or `!tz <timezone> [timezone...]` for time conversion."

_HALF_DAY = 12 * 3600
_ONE_DAY = 24 * 3600

_TimezoneMapping = collections.namedtuple("TimezoneMapping", (
    "canonical_identifier",
    "expected_identifier",
))
_TIMEZONE_MAPPING = {
    'AT': _TimezoneMapping('Canada/Atlantic', None),
    'ADT': _TimezoneMapping('Canada/Atlantic', 'ADT'),
    'AST': _TimezoneMapping('Canada/Atlantic', 'AST'),
    'CT': _TimezoneMapping('Canada/Central', None),
    'CDT': _TimezoneMapping('Canada/Central', 'CDT'),
    'CST': _TimezoneMapping('Canada/Central', 'CST'),
    'ET': _TimezoneMapping('Canada/Eastern', None),
    'EDT': _TimezoneMapping('Canada/Eastern', 'EDT'),
    'EST': _TimezoneMapping('Canada/Eastern', 'EST'),
    'MT': _TimezoneMapping('Canada/Mountain', None),
    'MDT': _TimezoneMapping('Canada/Mountain', 'MDT'),
    'MST': _TimezoneMapping('Canada/Mountain', 'MST'),
    'NT': _TimezoneMapping('Canada/Newfoundland', None),
    'NDT': _TimezoneMapping('Canada/Newfoundland', 'NDT'),
    'NST': _TimezoneMapping('Canada/Newfoundland', 'NST'),
    'PT': _TimezoneMapping('Canada/Pacific', None),
    'PST': _TimezoneMapping('Canada/Pacific', 'PST'),
    'PDT': _TimezoneMapping('Canada/Pacific', 'PDT'),
    'AZ': _TimezoneMapping('MST7MDT', None), #Arizona
    
    'HST': _TimezoneMapping('Pacific/Honolulu', 'HST'),
    'HDT': _TimezoneMapping('Pacific/Honolulu', 'HDT'),
    
    'AKT': _TimezoneMapping('US/Alaska', None),
    'AKDT': _TimezoneMapping('US/Alaska', 'AKDT'),
    'AKST': _TimezoneMapping('US/Alaska', 'AKST'),
    
    'AET': _TimezoneMapping('Australia/Sydney', None),
    'AEST': _TimezoneMapping('Australia/Sydney', 'AEST'),
    'AEDT': _TimezoneMapping('Australia/Sydney', 'AEDT'),
    'ACT': _TimezoneMapping('Australia/Adelaide', None),
    'ACST': _TimezoneMapping('Australia/Adelaide', 'ACST'),
    'ACDT': _TimezoneMapping('Australia/Adelaide', 'ACDT'),
    'AWT': _TimezoneMapping('Australia/Perth', None),
    'AWST': _TimezoneMapping('Australia/Perth', 'AWST'),
    'AWDT': _TimezoneMapping('Australia/Perth', 'AWDT'),
    
    'NZT': _TimezoneMapping('Pacific/Auckland', None),
    'NZDT': _TimezoneMapping('Pacific/Auckland', 'NZDT'),
    'NZST': _TimezoneMapping('Pacific/Auckland', 'NZST'),
    'CHAT': _TimezoneMapping('Pacific/Chatham', None),
    'CHADT': _TimezoneMapping('Pacific/Chatham', 'CHADT'),
    'CHAST': _TimezoneMapping('Pacific/Chatham', 'CHAST'),
    
    'CAT': _TimezoneMapping('Africa/Gaborone', None),
    'EAT': _TimezoneMapping('Africa/Nairobi', None),
    'WAT': _TimezoneMapping('Africa/Casablanca', None),
    
    'CET': _TimezoneMapping('Europe/Brussels', None),
    'CEDT': _TimezoneMapping('Europe/Brussels', None),
    'CEST': _TimezoneMapping('Europe/Brussels', None),
    'EET': _TimezoneMapping('Europe/Athens', None),
    'EEDT': _TimezoneMapping('Europe/Athens', None),
    'EEST': _TimezoneMapping('Europe/Athens', None),
    'WET': _TimezoneMapping('Europe/Iceland', None),
    'WEDT': _TimezoneMapping('Europe/London', None),
    'WEST': _TimezoneMapping('Europe/London', None),
    
    'MSK': _TimezoneMapping('Europe/Moscow', 'MSK'),
    'MSD': _TimezoneMapping('Europe/Moscow', 'MSD'),
    
    'JT': _TimezoneMapping('Asia/Tokyo', None),
    'JDT': _TimezoneMapping('Asia/Tokyo', 'JDT'),
    'JST': _TimezoneMapping('Asia/Tokyo', 'JST'),
    'KT': _TimezoneMapping('Asia/Seoul', None),
    'KDT': _TimezoneMapping('Asia/Seoul', 'KDT'),
    'KST': _TimezoneMapping('Asia/Seoul', 'KST'),
    
    #China uses "CST", which conflicts with the American zone
    'CHINA': _TimezoneMapping('Asia/Shanghai', None),
    'BEIJING': _TimezoneMapping('Asia/Shanghai', None),
    'BT': _TimezoneMapping('Asia/Shanghai', None),
    
    'HKT': _TimezoneMapping('Asia/Hong_Kong', None),
    
    'ICT': _TimezoneMapping('Asia/Bangkok', None),
    'MMT': _TimezoneMapping('Asia/Yangon', None),
    
    'WIB': _TimezoneMapping('Asia/Jakarta', None),
    'WITA': _TimezoneMapping('Asia/Makassar', None),
    'WIT': _TimezoneMapping('Asia/Jayapura', None),
    
    'SST': _TimezoneMapping('Asia/Singapore', None),
    'SGT': _TimezoneMapping('Asia/Singapore', None),
    'MYT': _TimezoneMapping('Asia/Kuala_Lumpur', None),
    'PHT': _TimezoneMapping('Asia/Manila', None),
}

def _prepare_localised_value(identifier, dt):
    if '/' not in identifier:
        identifier = identifier.upper()
    tzmapping = _TIMEZONE_MAPPING.get(identifier) or _TimezoneMapping(identifier, None)
    timezone = pytz.timezone(tzmapping.canonical_identifier)
    
    localised_value = timezone.localize(dt, is_dst=None)
    if tzmapping.expected_identifier is not None:
        if localised_value.tzname() != tzmapping.expected_identifier:
            return (localised_value, True)
    return (localised_value, False)
    
_AM_PM_RE = re.compile(r"\s*(?P<hour>\d|1[0-2])(?:\s+|:|\.)?(?P<minute>[0-5]\d)?\s*(?P<am_pm>[aApP][mM]?)\s+(?P<timezone>\w+(?:/\w+)?)")
_24H_RE = re.compile(r"\s*(?P<hour>1?\d|2[0-4])(?:\s+|:|\.)?(?P<minute>[0-5]\d)?\s*(?:[hH])?\s+(?P<timezone>\w+(?:/\w+)?)")

def _parse_timestamp_request(request):
    match = _AM_PM_RE.match(request) or _24H_RE.match(request)
    if not match:
        return (None, False)
        
    gd = match.groupdict()
    hour = int(gd['hour'])
    minute = int(gd['minute'] or 0)
    if 'am_pm' in gd and gd['am_pm'].startswith(('p', 'P')):
        hour += 12
    hour %= 24
    
    current_time = datetime.datetime.now()
    return _prepare_localised_value(gd['timezone'], datetime.datetime(
        current_time.year, current_time.month, current_time.day,
        hour, minute,
    ))
    
def _format_timestamp(timestamp):
    if timestamp.hour <= 12:
        return timestamp.strftime("%H:%M %Z (UTC%z)")
    return timestamp.strftime("%H:%M (%I:%M%P) %Z (UTC%z)")
    
def _format_delta(delta):
    delta_hours = int(delta / 3600)
    delta_minutes = int((delta - (delta_hours * 3600)) / 60)
    
    return "{} hour{}, {} minute{}".format(
        delta_hours, delta_hours != 1 and 's' or '',
        delta_minutes, delta_minutes != 1 and 's' or '',
    )
    
def _handle_timezone_delta(target, timzeone_mismatch):
    target_time = target.timestamp()
    current_time = time.time()
    
    value_in_past = False
    if target_time < current_time:
        delta = current_time - target_time
        if delta <= _HALF_DAY:
            value_in_past = True
        else:
            while target_time < current_time: #The internaional date line is annoying
                target_time += _ONE_DAY
            delta = target_time - current_time
    else:
        delta = target_time - current_time
        
    if not value_in_past:
        response_core = "{} is {} from now".format(
            _format_timestamp(target),
            _format_delta(delta),
        )
    else:
        response_core = "{} was {} ago".format(
            _format_timestamp(target),
            _format_delta(delta),
        )
        
    return "{}{}.".format(
        response_core,
        timezone_mismatch and "; your requested timezone was corrected for current DST" or "",
    )
    

def _prepare_current_value(identifier):
    if '/' not in identifier:
        identifier = identifier.upper()
    tzmapping = _TIMEZONE_MAPPING.get(identifier) or _TimezoneMapping(identifier, None)
    timezone = pytz.timezone(tzmapping.canonical_identifier)
    
    current_value = timezone.fromutc(datetime.datetime.utcnow())
    
    if tzmapping.expected_identifier is not None:
        if current_value.tzname() != tzmapping.expected_identifier:
            return (current_value, True)
    return (current_value, False)
    
def _handle_timezone_list(identifiers):
    responses = []
    for identifier in identifiers:
        if identifier:
            (current_value, timezone_mismatch) = _prepare_current_value(identifier)
            responses.append("{}{}".format(
                _format_timestamp(current_value),
                timezone_mismatch and "; your requested timezone was corrected for current DST" or "",
            ))
            
    if responses:
        return '\n'.join(responses)
    else:
        return "No timezones were specified."
        

async def handle_message(client, message):
    if message.content.startswith('!tz '):
        request = message.content[4:]
        try:
            (target, timezone_mismatch) = _parse_timestamp_request(request)
            if target:
                await message.reply(_handle_timezone_delta(target, timezone_mismatch))
            else:
                await message.reply(_handle_timezone_list(tz.strip() for tz in request.split()))
        except pytz.exceptions.UnknownTimeZoneError as e:
            await message.reply("Unsupported timezone: {}".format(e))
        return True
    return False
