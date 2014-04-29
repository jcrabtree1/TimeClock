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

setup(name='TimeClock',
      version='0.1.0',
      description='A utility for keeping track of hours worked',
      author='Jacob Crabtree',
      author_email='jacrabtree86@gmail.com',
      packages=['timeclock'],
      package_data={'timeclock': ['data/timeclock.db']},
      console=['timeclock/timeclock.py'],
     )