#! /usr/bin/env python
'''
Use this script to "install" the TimeClock application.
'''

import os
import sys
import shutil

# Check OS compatibility
WINDOWS = sys.platform == 'win32'
LINUX = sys.platform == 'linux2'

if not (WINDOWS or LINUX):
    print "Unknown or unsupported OS.  Exiting script."
    exit(1)


# Set location of application data
if LINUX:
    app_data = r"%s/.timeclock" % os.getenv('HOME')
    if not os.path.exists(app_data):
        os.mkdir(app_data)
if WINDOWS:
    app_data = r"%s\AppData\TimeClock" % os.getenv('USERPROFILE')
    if not os.path.exists(app_data):
        os.makedirs(app_data)

# Copy data templates to app_data directory
shutil.copyfile("data/timeclock_test.db", r"%s/timeclock_test.db" % app_data)
shutil.copyfile("data/hoursreport.plt", r"%s/hoursreport.plt" % app_data)
