# -*- coding: utf-8 -*-
#NOTE: this is very much naive of DST changes when looking backwards.
#I don't expect this to be a common case, nor one anyone will really care
#about, so I haven't put any effort into correcting for it around the date-line, but
#it is sufficient to warrant recommending users not trust this mechanism over a robust
#alarm.
import datetime
import re
import time

from . import common

_HALF_DAY = 12 * 3600
_ONE_DAY = 24 * 3600

def _prepare_localised_value(identifier, dt):
    (timezone, expected_identifier) = common.get_timezone(identifier)
    
    localised_value = timezone.localize(dt, is_dst=None)
    if expected_identifier is not None:
        if localised_value.tzname() != expected_identifier:
            return (localised_value, True)
    return (localised_value, False)
    
_AM_PM_RE = re.compile(r"\s*(?P<hour>\d|1[0-2])(?:\s+|:|\.)?(?P<minute>[0-5]\d)?\s*(?P<am_pm>[aApP][mM]?)\s+(?P<timezone>\w+(?:/\w+)?)")
_24H_RE = re.compile(r"\s*(?P<hour>1?\d|2[0-4])(?:\s+|:|\.)?(?P<minute>[0-5]\d)?\s*(?:[hH])?\s+(?P<timezone>\w+(?:/\w+)?)")

def parse_timestamp_request(request):
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
    
def _format_delta(delta):
    delta_hours = int(delta / 3600)
    delta_minutes = int((delta - (delta_hours * 3600)) / 60)
    
    return "{} hour{}, {} minute{}".format(
        delta_hours, delta_hours != 1 and 's' or '',
        delta_minutes, delta_minutes != 1 and 's' or '',
    )
    
def handle_timezone_delta(target, timezone_mismatch):
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
        response = "{} is {} from now".format(
            common.format_timestamp(target),
            _format_delta(delta),
        )
    else:
        response = "{} was {} ago".format(
            common.format_timestamp(target),
            _format_delta(delta),
        )
        
    if timezone_mismatch:
        response += " (corrected for current DST)"
        
    response += "\nThis is <t:{}:t> local time".format(int(target_time))
    
    return response
