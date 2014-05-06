#! /usr/bin/env python
"""
Parse dates and times.
"""

import datetime

def validate_date(date_text):
    '''Make sure string is in YYYY-MM-DD format.'''
    if date_text == "now', 'localtime":
        return 0
    else:
        try:
            datetime.datetime.strptime(date_text, '%Y-%m-%d')
            return 0
        except ValueError:
            raise ValueError("Incorrect date format.  Should be YYYY-MM-DD")
        
def validate_time(time_text):
    '''Make sure string is in HH:MM:SS format.'''
    if time_text == "now', 'localtime":
        return 0
    else:
        try:
            datetime.datetime.strptime(time_text, '%H:%M:%S')
            return 0
        except ValueError:
            raise ValueError("Incorrect date format.  Should be 24-hour, HH:MM")
            
            
