**TimeClock**
=============

Command Line Arguments
----------------------
*Example*: ./timeclock -u 2014-04-29 --out 17:32:00

-  --in [HH:MM:SS] - Clock in for the day.  Optional time argument defaults 
                    to current time.
-  --out - Clock out for the day.  Optional time argument defaults to 
          current time.
-  --lout - Go to lunch.  Optional time argument defaults to current time.
-  --lin - Return from lunch.  Optional time argument defaults to current time.
-  -u, --update [YYYY-MM-DD] - Update a time from a previous record.  Optional
                              date argument defaults to today.
-  --lookup YYYY-MM-DD - Lookup times from a provided date.
-  -r, --report MM - Provide hours report for a given month.
-  -d, --debug - Give debug output from script.
-  -t, --test - Run the test suite to check for errors.
-  -h, --help - Display help page and exit.

Dependencies
------------
 - pandas
 - sqlite3

