# -*- coding: utf-8 -*-
import collections

import pytz

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

def get_timezone(identifier):
    if '/' not in identifier:
        identifier = identifier.upper()
    tzmapping = _TIMEZONE_MAPPING.get(identifier) or _TimezoneMapping(identifier, None)
    return (pytz.timezone(tzmapping.canonical_identifier), tzmapping.expected_identifier)
    
def format_timestamp(timestamp):
    if timestamp.hour <= 12:
        value = timestamp.strftime("%H:%M %Z (UTC%z)")
    else:
        subvalue = timestamp.strftime("%I:%M%P")
        if subvalue[0] == '0':
            subvalue = subvalue[1:]
        value = timestamp.strftime("%H:%M ({}) %Z (UTC%z)".format(subvalue))
        
    if value[0] == '0':
        return value[1:]
    return value
    
