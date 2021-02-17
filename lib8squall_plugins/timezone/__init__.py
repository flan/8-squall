If given one or more timezones, display the current time there and in UTC, plus each timezone's UTC offset

!tz MST EST
<you>, it is currently <datetime> MST (UTC-7), <datetime> EST (UTC-5), and <datetime> UTC.
#if a DST target is incorrectly specified, add a final line saying "a DST timezone was specified, but DST is not in effect" or "a non-DST timezone was specified, but DST is in effect"
#try to find a database of DST values to make this possible
#the first draft might either omit this check or only do it for North American locations, since
#those seem to have the least-worldly populace

If given a timestamp and a timezone, display the amount of time between now and then, and that timestamp in UTC.

!tz 7pm mst
you, <time> MST (UTC-7) is 6 hours, 34 minutes from now.
#or, if it was less than three hours ago
you, <time> MST (UTC-7) was 2 hours, 34 minutes ago.

#don't use dateutil; instead, just apply reasonable inference against input strings
7pm
7:30 pm
1400
1400h
14:00
14h
725am
7 25 am
125pm
125
125h

import re

_AM_PM_RE = re.compile(r"\s*(?<hour>\d{1,2})(?:\s+|:|\.)?(?<minute>\d{2})?\s*(?<am_pm>[aApP][mM])\s+")
_24H_RE = re.compile(r"\s*(?<hour>\d{1,2})(?:\s+|:|\.)?(?<minute>\d{2})?\s*(?:[hH])?\s+")

#try am/pm matching first, then 24h; normalise either one to 24h, then build a timestamp value
