#! /usr/bin/env python
'''
Helper functions for repeated SQL code.
'''

import time

TODAY = time.strftime("%Y-%m-%d", time.localtime())

def update_record(conn, column, date=TODAY, time="now', 'localtime"):
    '''
    Update a record that already exists.  Column name must be provided, but
    date and time default to the current date and/or time.
    '''
    try:
        conn.execute('''
                     UPDATE times SET %s=time('%s')
                     WHERE date=date('%s');
                     ''' % (column, time, date)
                     )
        conn.commit()
    except OperationalError:
        print "Something went wrong setting the %s column for %s." % (column, date)
    else:
        print "Punch accepted!"
    return 0

def new_record(conn, column, date=TODAY, time="now', 'localtime"):
    '''
    Create a new record.  Column name must be provided, but
    date and time default to the current date and/or time.
    '''
    try:
        conn.execute('''
                     INSERT INTO times (date, %s)
                     VALUES (date('%s'), time('%s'));
                     ''' % (column, date, time)
                     )
        conn.commit()
    except OperationalError:
        print "Something went wrong setting the %s column for %s." % (column, date)
    else:
        print "Punch accepted!"
    return 0

def check_record_exists(conn, date=TODAY):
    '''
    Check whether a record for a given date already exists.
    '''
    try:
        res = conn.execute('''
                           SELECT COUNT(*) FROM times
                           WHERE date='%s';
                           ''' % date
                           )
    except OperationalError:
        print "Something went wrong running the SQL command."
    else:
        return bool(res.fetchone()[0])

