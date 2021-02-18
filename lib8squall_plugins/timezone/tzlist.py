# -*- coding: utf-8 -*-
import datetime

from . import common

def _prepare_current_value(identifier):
    (timezone, expected_identifier) = common.get_timezone(identifier)
    
    current_value = timezone.fromutc(datetime.datetime.utcnow())
    
    if expected_identifier is not None:
        if current_value.tzname() != expected_identifier:
            return (current_value, True)
    return (current_value, False)
    
def handle_timezone_list(identifiers):
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
