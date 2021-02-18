"""
If given one or more timezones, display the current time there and in UTC, plus each timezone's UTC offset

!tz MST EST
<you>, it is currently <datetime> MST (UTC-7), <datetime> EST (UTC-5), and <datetime> UTC.
#if a DST target is incorrectly specified, add a final line saying "a DST timezone was specified, but DST is not in effect" or "a non-DST timezone was specified, but DST is in effect"
#try to find a database of DST values to make this possible
#the first draft might either omit this check or only do it for North American locations, since
#those seem to have the least-worldly populace

"""

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
    
def test(timezone):
    current_time = time.time()
    for t in tests:
        print(t)
        (target, timezone_mismatch) = _parse_timestamp_request('{} {}'.format(t, timezone))
        if target:
            target_time = target.timestamp()
            value_in_past = False
            if target_time < current_time:
                delta = current_time - target_time
                if delta <= _HALF_DAY:
                    value_in_past = True
                    delta_string = _format_delta(delta)
                else:
                    while target_time < current_time: #The internaional date line is annoying
                        target_time += _ONE_DAY
                        
            if not value_in_past:
                delta_string = _format_delta(target_time - current_time)
                
                print("{} is {} from now{}".format(
                    _format_timestamp(target), delta_string,
                    timezone_mismatch and "; your requested timezone was corrected for DST" or ""
                ))
            else:
                print("{} was {} ago{}".format(
                    _format_timestamp(target), delta_string,
                    timezone_mismatch and "; your requested timezone was corrected for DST" or ""
                ))
                
    

async def handle_message(client, message):
    if message.content.startswith('!tz '):
        try:
            (target, timezone_mismatch) = _parse_timestamp_request('{} {}'.format(t, timezone))
            if target: #it's a timezone delta request
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
                    
                await message.reply("{}{}.".format(
                    response_core,
                    timezone_mismatch and "; your requested timezone was corrected for current DST" or "",
                ))
        except pytz.exceptions.UnknownTimeZoneError as e:
            await message.reply("Unsupported timezone: {}".format(e))
        return True
    return False



x.fromutc(datetime.datetime.utcnow()).strftime('%T %Z (UTC%z)')
