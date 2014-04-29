#! /usr/bin/env python
"""
Report on time data using pandas.
"""

import pandas as pd
import pandas.io.sql as psql
import sqlite3

conn = sqlite3.connect('../data/timeclock.db')
with conn:
    sql = "SELECT * FROM times WHERE date BETWEEN '2014-04-01' AND '2014-04-30';"
    df = psql.frame_query(sql, conn)
    print df.shape
    
