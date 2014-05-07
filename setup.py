#! /usr/bin/env python
'''
Setup script for TimeClock

Dependencies
============
 - SQLite3
 - matplotlib
 - pandas
 
Considerations
==============
At install time, the user will need an empty database
with the established schema.  Not sure how to do this,
but perhaps it could be part of an install script.

'''

from distutils.core import setup
import py2exe
import os
import sys
import shutil

setup(name='TimeClock',
      version='0.1.0',
      description='A utility for keeping track of hours worked',
      author='Jacob Crabtree',
      author_email='jacrabtree86@gmail.com',
      packages=['timeclock'],
      package_data={'timeclock': ['data/timeclock_test.db']},
      console=['timeclock/timeclock.py'],
      datafiles = [("DLLs", 'DLLs/python27.dll')],
      zipfile=None,
      options={'py2exe' : {'bundle_files' : 1}},
     )

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
    app_data = r"%s\AppData\Local\TimeClock" % os.getenv('USERPROFILE')
    if not os.path.exists(app_data):
        os.makedirs(app_data)

# Copy data templates to app_data directory
shutil.copyfile("data/timeclock_test.db", r"%s/timeclock_test.db" % app_data)
shutil.copyfile("data/hoursreport.plt", r"%s/hoursreport.plt" % app_data)

if sys.argv[1] == 'py2exe':
    shutil.copyfile("dist/timeclock.exe", r"C:\Apps\timeclock.exe")