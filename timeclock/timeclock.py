#! /usr/bin/env python
'''
TimeClock is a utility to help keep track of your time.

Flags:

    --in [HH:MM]    : Clock in for the day. Defaults to now.

    --out [HH:MM]   : Clock out for the day.  Defaults to now.

    --lout [HH:MM]  : Clock out for lunch.  Defaults to now.

    --lin [HH:MM]   : Clock in from lunch.  Defaults to now.

    --update, -u YYYY-MM-DD : Update a time from a previous date.

    --lookup [YYYY-MM-DD] : Lookup time for given date.  Defaults to today.

    --report, -r MM : Show simple monthly report of time worked
                      in month MM (1-12).  Integer month argument required.

    --test, -t : Use the pre-populated test database.

    --debug, -d : Print debug messages to help find errors.

    --help, -h : View this help page.
    
Usage:

 $ TimeClock --in

 $ TimeClock --out

 $ TimeClock --lookup 2014-04-28

 $ TimeClock --report 2014-04-01 2014-04-30
 
Times are saved into a SQLite database timeclock.db, which
can be further queried, though this goes beyond the scope of
this module.

Please use the GitHub page (http://github.com/jcrabtree1/TimeClock) to
submit any issues, bug reports, or suggestions.

'''

import time
import sqlite3
import argparse
from TimeClock.utils.validation import validate_date, validate_time

LOOKUPSTRING = \
"""
==========================
   DATE    | %(date)s
--------------------------
 CLOCK IN  |  %(cin)s
 LUNCH OUT |  %(lout)s
 LUNCH IN  |  %(lin)s
 CLOCK OUT |  %(cout)s
==========================
"""

today = time.strftime("%Y-%m-%d", time.localtime())
now = time.strftime("%H:%M:%S", time.localtime())

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update', nargs='?', const=today, default="",
                    help="Update a previous record.")
parser.add_argument('--in', nargs='?', const="'now', 'localtime'", default='',
                    help="Clock in for the day.")
parser.add_argument('--out', nargs='?', const="'now', 'localtime'", default='',
                    help="Clock out for the day.")
parser.add_argument('--lout', nargs='?', const="'now', 'localtime'", default='',
                    help="Go to lunch.")
parser.add_argument('--lin', nargs='?', const="'now', 'localtime'", default='',
                    help="Return from lunch.")
parser.add_argument('--lookup', nargs='?', const=today, 
                    help="Look up times from a previous record")
parser.add_argument('-r', '--report', help='Report on monthly hours.')
parser.add_argument('-d', '--debug', action='store_true', 
                    help='Debug the program.', default=False)
parser.add_argument('-t', '--test', action='store_true', default=False,
                    help='Run the test suite.')

args = parser.parse_args()

if args.debug:
    print '\n', args, '\n'

# Validation
if args.update:
    validate_date(args.update)
if args.lookup:
    validate_date(args.lookup)
if vars(args)['in']:
    validate_time(vars(args)['in'])
if args.out:
    validate_time(args.out)
if args.lout:
    validate_time(args.lout)
if args.lin:
    validate_time(args.lin)

# Connect to database
if args.test:
    db = '../data/timeclock_test.db'
else:
    db = '../data/timeclock.db'
conn = sqlite3.connect(db)

# Check that DB is initialized with the correct schema
try:
    conn.execute('''SELECT * FROM times LIMIT 1;''')
except OperationalError:
    conn.execute('''
                 CREATE TABLE times (
                 date TEXT,
                 clockin TEXT,
                 lunchout TEXT,
                 lunchin TEXT,
                 clockout TEXT);
                 ''')

# Clock in
if vars(args)['in']:
    if args.update:
        if args.debug:
           print "Updating clockin time for ", args.update
        conn.execute(
            '''UPDATE times SET clockin=time('%s')
               WHERE date=date('%s');''' %
               (vars(args)['in'], args.update)
        )
        print "Successfully updated clockin time for %s" % args.update
    else:
        if args.debug:
           print "Creating new clockin time for today"
        conn.execute(
            '''INSERT INTO times (date, clockin) 
               VALUES (date('now'), time('%s'));''' %
               vars(args)['in']
        )
        print "Successfully clocked in at %s." % vars(args)['in']

# Go to lunch.
if args.lout:
    if args.update:
        if args.debug:
           print "Updating lunch out time for ", args.update
        conn.execute(
            '''UPDATE times SET lunchout=time('%s')
               WHERE date=date('%s');''' %
               (args.lout, args.update)
        )
        print "Successfully updated lunch clockout time for %s" % args.update
    else:
        if args.debug:
           print "Creating new lunch out time for today"
        conn.execute(
            '''UPDATE times SET lunchout=time('%s')
               WHERE date=date('now');''' % (args.lout)
        )
        print "Successfully clocked out for lunch at %s." % args.lout

# Return from lunch
if args.lin:
    if args.update:
        if args.debug:
           print "Updating lunch in time for ", args.update
        conn.execute(
            '''UPDATE times SET lunchin=time('%s')
               WHERE date=date('%s');''' % (args.lin, args.update)
        )
        print "Successfully updated lunch clockin time for %s" % args.update
    else:
        if args.debug:
           print "Creating new lunch in time for today"
        conn.execute(
            '''UPDATE times SET lunchin=time('%s')
               WHERE date=date('now');''' % (args.lin)
        )
        print "Successfully clocked in from lunch at %s." % args.lin
        
# Clock out
if args.out:
    if args.update:
        if args.debug:
           print "Updating clock out time for ", args.update
        conn.execute(
            '''UPDATE times SET clockout=time('%s')
               WHERE date=date('%s');''' % (args.out, args.update)
        )
        print "Successfully updated clock out time for %s" % args.update
    else:
        if args.debug:
           print "Creating new clock out time for today"
        conn.execute(
            '''UPDATE times SET clockout=time('%s')
               WHERE date=date('now');''' % (args.out)
        )
        print "Successfully clocked out at %s." % args.out

# Look up a previous record
if args.lookup:
    lu_date = args.lookup
    cursor = conn.execute(
        '''SELECT * FROM times WHERE date="%s";''' % (lu_date)
    )
    for row in cursor:
        print LOOKUPSTRING % dict(zip(['date', 'cin', 
                                   'lout', 'lin', 'cout'], row)), '\n'

# Reporting
if args.report:
    import pandas as pd
    import pandas.io.sql as psql
    import numpy as np
    import matplotlib.pyplot as plt

    sql = '''
          SELECT * FROM times 
          WHERE date BETWEEN date('2014-%s-01') 
          AND date('2014-%s-01', 'start of month', '+1 month', '-1 day');
          ''' % (args.report.zfill(2), args.report.zfill(2))
    df = psql.frame_query(sql, conn)

    # Convert strings to pandas datetime format
    df.date = pd.to_datetime(df.date)
    df.clockin = pd.to_datetime(df.clockin)
    df.lunchout = pd.to_datetime(df.lunchout)
    df.lunchin = pd.to_datetime(df.lunchin)
    df.clockout = pd.to_datetime(df.clockout)
    
    if args.debug:
        print "\n Data Types:\n", df.dtypes, df.index.dtype

    # Create 'gross', 'lunch', and 'total' columns
    df['gross'] = (df.clockout - df.clockin).astype('timedelta64[ns]') / np.timedelta64(1, 'h')
    df['lunch'] = (df.lunchin - df.lunchout).astype('timedelta64[ns]') / np.timedelta64(1, 'h')
    df['total'] = df.gross - df.lunch

    if args.debug:
        print "\n Data Types:\n", df.dtypes, df.index.dtype

    df = df.set_index('date')
    print "\n\nTotal Hours: %3.2f" % df['total'].sum()
    print "Average daily hours: %3.2f" % df['total'].mean()
    df['average'] = df.total.mean()
    totaldf = df.copy()
    totaldf[['Net Daily Hours', 'Average Daily Hours']] = totaldf[['total', 'average']]
    
    ax = totaldf[['Net Daily Hours', 'Average Daily Hours']].plot(
            title="Hours Worked in Month %s" % args.report, kind='line')
    ax.set_ylabel('Hours Worked')
    ax.set_xlabel('Date')
    plt.xticks(rotation=45)
    
    plt.show()

conn.commit()
conn.close()
