#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 18 20:38:46 2020

@author: saravana.kumar
"""

import sqlite3 as lite
from datetime import datetime
import sys


'''
Function to insert values to tables pass rows as strings and values as Strings as well 
'''
def createTableRecord(table,rows,values):

    db = None
    try:
        db = lite.connect('/Users/saravana.kumar/algo.db')
        cur=db.cursor()
        query="INSERT INTO TSS_SELL ("+rows+") VALUES (?,?,?,?)"
        cur.execute(query,values)
        db.commit()
    except:
        print('ERR')
        #sys.exit(1)
    finally:
        if db:
            db.close()
