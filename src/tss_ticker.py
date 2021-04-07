    #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 26 21:14:26 2020

@author: saravana.kumar
"""

import logging
import os
import pandas as pd
import datetime
import sys
import sqlite3 as lite

from save_ticks import create_tables,insert_ticks,dbclose
from kiteconnect import KiteConnect,KiteTicker
from getinstruments import getInstrumentDump
from sutils import tokenLookup
from datetime import timedelta


cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#get dump of all NSE instruments
instrument_df = getInstrumentDump("NSE")
instrument_nfo= getInstrumentDump("NFO")

def get_instrument_price_dict(date):
    db = None
    try:
        db = lite.connect('/Users/saravana.kumar/algo.db')
        sql = """select ID,STRIKE,AVG_PRICE,QTY,DATE
         from TSS_SELL
         where DATE = {0} """
        sql=sql.format('?') 
        print(sql)
        data = pd.read_sql(sql,con=db,params={date})  
        print(data)
        price_dict = dict(zip(data.STRIKE, data.AVG_PRICE))
        print(price_dict)
        instrument_list=[]
        for key, value in price_dict.items():
            instrument_list.append(key)
        print(instrument_list)
        return instrument_list
    except Exception as e: 
        print(e)
        print('ERR')
        #sys.exit(1)
    finally:
        if db:
            db.close()

#date_param=(datetime.date.today()-timedelta(1)).strftime('%y-%m-%d')
date_param=(datetime.date.today()).strftime('%y-%m-%d')
print(date_param)
get_instrument_price_dict(date_param)

def on_ticks(ws,ticks):
    table_list=get_instrument_price_dict(date_param)
    insert_tick=insert_ticks(ticks,table_list)
    print(ticks)

def on_connect(ws,response):
    table_list=get_instrument_price_dict(date_param)
    tokens_tss = tokenLookup(instrument_nfo,table_list)
    print(tokens_tss)
    ws.subscribe(tokens_tss)
    ws.set_mode(ws.MODE_FULL,tokens_tss)
    

now = datetime.datetime.now()
print('date time now:'+str(now.hour)+str(now.minute))


kws = KiteTicker(key_secret[0],kite.access_token)
while True:
    now = datetime.datetime.now()
   # print('date time now:'+str(now.hour)+str(now.minute))
    if (now.hour >= 10 and now.minute >= 15 ):
        print('About to connect')
        kws.on_ticks=on_ticks
        kws.on_connect=on_connect
        kws.connect()
    if (now.hour >= 18 and now.minute >= 00):
        dbclose()
        sys.exit()
