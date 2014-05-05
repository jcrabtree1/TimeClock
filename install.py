#! /usr/bin/env python
'''
Use this script to "install" the TimeClock application.
'''

import os

# Make a place for the data
HOME = os.getenv('USERPROFILE')
os.makedirs(r"%s\AppData\Local\TimeClock" % HOME)
