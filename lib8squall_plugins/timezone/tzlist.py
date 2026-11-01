# -*- coding: utf-8 -*-
import datetime

from . import common

def _prepare_current_value(identifier):
    """
    Current wall-clock time in a timezone, plus its display name.

    Returns (current_value, display_name, mismatch).
    """
    (timezone, expected_identifier, permanent) = common.get_timezone(identifier)

    current_value = timezone.fromutc(datetime.datetime.now(datetime.UTC).replace(tzinfo=None))

    (display_name, mismatch) = common.resolve_localised_value(
        current_value, expected_identifier, permanent)
    return (current_value, display_name, mismatch)

def handle_timezone_list(identifiers):
    """
    Render the current time for each requested zone, one per line.
    """
    responses = []
    for identifier in identifiers:
        if identifier:
            (current_value, display_name, timezone_mismatch) = _prepare_current_value(identifier)
            responses.append("{}{}".format(
                common.format_timestamp(current_value, display_name),
                timezone_mismatch and "; your requested timezone was corrected for current DST" or "",
            ))

    if responses:
        return '\n'.join(responses)
    else:
        return "No timezones were specified."
