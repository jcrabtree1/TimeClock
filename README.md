**TimeClock**
=============
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

Usage
-----

 $ TimeClock --in

 $ TimeClock --out

 $ TimeClock --lookup 2014-04-28

 $ TimeClock --report 2014-04-01 2014-04-30

Times are saved into a SQLite database timeclock.db, which
can be further queried, though this goes beyond the scope of
this module.

Please use the GitHub page (http://github.com/jcrabtree1/TimeClock) to
submit any issues, bug reports, or suggestions.


Dependencies
------------
 - sqlite3
 - gnuplot
 
Setup and Installation on Windows
---------------------------------

From source:
 1. Download the source repository from http://github.com/jcrabtree1/TimeClock
 2. Open a CMD console in the newly-created directory
 3. Run the following command:
    $ python setup.py py2exe
    
Adding application to system PATH:
 1. Click on the Start menu, right click on Computer, and select Properties
 2. Select Advanced system settings, then Environment variables
 3. In the list of System variables, select "PATH" and click Edit
 4. Add ";C:\Apps" (without quotes) to the end of the PATH variable (Note:  DO NOT remove anything from the existing variable.)
