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
import os
import sys
import sqlite3
from sqlite3 import OperationalError
import argparse
from TimeClock.utils.validation import validate_date, validate_time
from TimeClock.utils.sqlhelpers import update_record, new_record, check_record_exists

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

LINUX = sys.platform == 'linux2'
WINDOWS = sys.platform == 'win32'

if not (LINUX or WINDOWS):
    print "Unknown or unsupported OS. Exiting script."
    exit(1)

today = time.strftime("%Y-%m-%d", time.localtime())
now = time.strftime("%H:%M:%S", time.localtime())

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update', nargs='?', const=today, default="",
                    help="Update a previous record.")
parser.add_argument('--in', nargs='?', const="now', 'localtime", default='',
                    help="Clock in for the day.")
parser.add_argument('--out', nargs='?', const="now', 'localtime", default='',
                    help="Clock out for the day.")
parser.add_argument('--lout', nargs='?', const="now', 'localtime", default='',
                    help="Go to lunch.")
parser.add_argument('--lin', nargs='?', const="now', 'localtime", default='',
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

# Find correct DB location based on platform
if LINUX:
    DB_PATH = r"%s/.timeclock/timeclock.db" % os.getenv('HOME')
    TEST_DB_PATH = r"%s/.timeclock/timeclock_test.db" % os.getenv('HOME')
if WINDOWS:
    DB_PATH = r"%s\AppData\Local\TimeClock\timeclock.db" % os.getenv('USERPROFILE')
    TEST_DB_PATH = r"%s\AppData\Local\TimeClock\timeclock_test.db" % os.getenv('USERPROFILE')

# Connect to database
if args.test:
    db = TEST_DB_PATH
else:
    db = DB_PATH

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

        if check_record_exists(conn, args.update):
            update_record(conn, 'clockin', args.update, vars(args)['in'])
        else:
            new_record(conn, 'clockin', args.update, vars(args)['in'])

    else:
        if args.debug:
            print "Creating new clockin time for today"
        if check_record_exists(conn):
            update_record(conn, 'clockin', time=vars(args)['in'])
        else:
            new_record(conn, 'clockin', time=vars(args)['in'])

# Go to lunch.
if args.lout:
    if args.update:
        if args.debug:
            print "Updating lunch out time for ", args.update

        if check_record_exists(conn, args.update):
            update_record(conn, 'lunchout', args.update, args.lout)
        else:
            new_record(conn, 'lunchout', args.update, args.lout)

    else:
        if args.debug:
            print "Creating new lunch out time for today"
        if check_record_exists(conn):
            update_record(conn, 'lunchout', time=args.lout)
        else:
            new_record(conn, 'lunchout', time=args.lout)

# Return from lunch
if args.lin:
    if args.update:
        if args.debug:
            print "Updating lunch in time for ", args.update

        if check_record_exists(conn, args.update):
            update_record(conn, 'lunchin', args.update, args.lin)
        else:
            new_record(conn, 'lunchin', args.update, args.lin)

    else:
        if args.debug:
            print "Creating new lunch in time for today"
        if check_record_exists(conn):
            update_record(conn, 'lunchin', time=args.lin)
        else:
            new_record(conn, 'lunchin', time=args.lin)

# Clock out
if args.out:
    if args.update:
        if args.debug:
            print "Updating clock out time for ", args.update

        if check_record_exists(conn, args.update):
            update_record(conn, 'clockout', args.update, args.out)
        else:
            new_record(conn, 'clockout', args.update, args.out)

    else:
        if args.debug:
            print "Creating new clock out time for today"
        if check_record_exists(conn):
            update_record(conn, 'clockout', time=args.out)
        else:
            new_record(conn, 'clockout', time=args.out)

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
    if args.report in ['ytd', 'YTD']:
        start_date = "date('2014-01-01')"
        end_date = "date('now', 'localtime')"
        label = "YTD"
    elif int(args.report) in range(1, 13):
        start_date = "date('2014-%s-01')" % args.report.zfill(2)
        end_date = "date('2014-%s-01', 'start of month', '+1 month', '-1 day')" % args.report.zfill(2)
        label = "Month %s" % args.report
    else:
        print "Unrecognized argument.  Please use and integer from 1 to 12 or 'YTD'."
        exit(1)

    # Check if a report table already exists and delete it if so
    try:
        conn.execute("SELECT * FROM report LIMIT 1;")
    except OperationalError:
        conn.execute('''
                     CREATE TABLE report (
                     date TEXT,
                     clockin TEXT,
                     lunchout TEXT,
                     lunchin TEXT,
                     clockout TEXT);
                     ''')
    else:
        conn.execute("DROP TABLE report;")
        conn.execute('''
                     CREATE TABLE report (
                     date TEXT,
                     clockin TEXT,
                     lunchout TEXT,
                     lunchin TEXT,
                     clockout TEXT);
                     ''')

    # Create a temporary reporting table
    conn.execute('''
                 INSERT INTO report
                 SELECT * FROM times WHERE date
                 BETWEEN %s AND %s
                 ORDER BY date(date);
                 ''' % (start_date, end_date)
                 )

    # Add gross, lunch, total, and average columns
    conn.execute('''
                 ALTER TABLE report
                 ADD COLUMN gross REAL;
                 ''')

    conn.execute('''
                 ALTER TABLE report
                 ADD COLUMN lunch REAL;
                 ''')

    conn.execute('''
                 ALTER TABLE report
                 ADD COLUMN total REAL;
                 ''')

    conn.execute('''
                 ALTER TABLE report
                 ADD COLUMN average REAL;
                 ''')
    conn.commit()

    # Fill with appropriate values
    conn.execute('''
                 UPDATE report
                 SET gross = (strftime('%s', clockout) - strftime('%s', clockin)) / 3600.
                 WHERE 1=1;
                 ''')


    conn.execute('''
                 UPDATE report
                 SET lunch = (strftime('%s', lunchin) - strftime('%s', lunchout)) / 3600.
                 WHERE 1=1;
                 ''')


    conn.execute("UPDATE report SET total = gross - lunch WHERE 1=1;")


    conn.execute('''
                 UPDATE report SET average = (
                 SELECT AVG(total) FROM report WHERE 1=1);
                 ''')
    conn.commit()

    if LINUX:
        RPT_DATAFILE = r"%s/.timeclock/hoursrpt" % os.getenv('HOME')
    if WINDOWS:
        RPT_DATAFILE = r"%s\AppData\Local\TimeClock\hoursrpt" % os.getenv('USERPROFILE')
    with open(RPT_DATAFILE, 'w') as out:
        for row in conn.execute("SELECT * FROM report;").fetchall():
            out.write("{}|{}|{}|{}|{}|{}|{}|{}|{}\n".format(row[0], row[1], row[2],
                                                          row[3], row[4], row[5],
                                                          row[6], row[7], row[8],))

    TOTAL = conn.execute("SELECT SUM(total) FROM report;").fetchone()[0]
    AVERAGE = conn.execute("SELECT average FROM report LIMIT 1;").fetchone()[0]
    conn.execute("DROP TABLE report;")

    # Print total and average
    print "\n\nTotal Hours: %3.2f" % TOTAL
    print "Average daily hours: %3.2f" % AVERAGE

    # Create a GNUPLOT .plt file
    if LINUX:
        PLT_TEMP = r"%s/.timeclock/hoursreport.plt" % os.getenv('HOME')
        PLT = r"%s/.timeclock/%shoursreport.plt" % (os.getenv('HOME'), args.report)
    if WINDOWS:
        PLT_TEMP = r"%s\AppData\Local\TimeClock\hoursreport.plt" % os.getenv('USERPROFILE')
        PLT = r"%s\AppData\Local\TimeClock\%shoursreport.plt" % (os.getenv('USERPROFILE'), args.report)
    with open(PLT, 'w') as newfile:
        newfile.write(open(PLT_TEMP).read().format(label, label))

    curr_dir = os.getcwd()
    if LINUX:
        os.chdir(r"%s/.timeclock" % os.getenv('HOME'))
    if WINDOWS:
        os.chdir(r"%s\AppData\Local\TimeClock" % os.getenv('USERPROFILE'))
    os.system('gnuplot %shoursreport.plt' % args.report)

    if LINUX:
        os.system("firefox \"%s Hours.png\"" % label)
    if WINDOWS:
        os.system("\"%s Hours.png\"" % label)

conn.commit()
conn.close()
