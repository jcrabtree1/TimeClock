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
import matplotlib
import glob
import py2exe

options = {'py2exe' : {'includes' : ['matplotlib', 'pandas', 'numpy', 
                                     'matplotlib.backends.backend_qt4agg'],
                       'excludes' : ['_gtkagg', '_tkagg', '_agg2', '_cairo', '_cocoaagg', 
                                     'matplotlib.numerix.fft', 'PyQt4._qt',
                                     'matplotlib.numerix.linear_algebra',
                                     'matplotlib.numerix.random_array', 
                                     '_fltkagg', '_gtk', '_gtkcairo'],
                       'dll_excludes' : ['libgdk-win32-2.0-0.dll',
                                         'libgobject-2.0-0.dll']
                      }
          }

data_files = [(r'mpl-data', glob.glob(r'C:\Python27\Lib\site-packages\matplotlib\mpl-data\*.*')),
              (r'mpl-data', [r'C:\Python27\Lib\site-packages\matplotlib\mpl-data\matplotlibrc']),
              (r'mpl-data\images',glob.glob(r'C:\Python27\Lib\site-packages\matplotlib\mpl-data\images\*.*')),
              (r'mpl-data\fonts',glob.glob(r'C:\Python27\Lib\site-packages\matplotlib\mpl-data\fonts\*.*'))]

setup(name='TimeClock',
      version='0.1.0',
      description='A utility for keeping track of hours worked',
      author='Jacob Crabtree',
      author_email='jacrabtree86@gmail.com',
      packages=['timeclock'],
      package_data={'timeclock': ['data/timeclock.db']},
      console=['timeclock/timeclock.py'],
      # data_files=matplotlib.get_py2exe_datafiles(),
      options=options,
      data_files=data_files,
     )
