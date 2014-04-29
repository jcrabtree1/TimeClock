#! /usr/bin/env python
'''
Database functions.
'''

import sqlite3
import TimeClock.utils.validation as valid

def update_row(colname, date_str='now', time_str='now')
    fnargs = locals()
    try:
        valid.validate_date(date_str)
        valid.validate_time(time_str)
    except ValueError:
        print "Invalid date or time format."
    
    try:
        if colname not in ['clockin', 'clockout', 'lunchin', 'lunchout']:
        raise ValueError
    except ValueError:
        print "Column name does not exist in database."
        
    else:
        conn = sqlite3.connect("../data/timeclock.db")
        conn.execute('''UPDATE times
                        SET :colname=:time_str
                        WHERE date=:date_str;''', fnargs
                    )
        conn.commit()
        conn.close()
        