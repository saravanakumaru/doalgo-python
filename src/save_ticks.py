#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:42:22 2020

@author: saravana.kumar
"""

from kiteconnect import KiteTicker, KiteConnect
from sutils import round_nearest
from getinstruments import getInstrumentDump
from getinstruments import getInstrumentTradingSymbolForExpiry,getInstrumentTokenMap
import datetime
import sys
import pandas as pd
import os
import sqlite3

cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

db = sqlite3.connect('/Users/saravana.kumar/algo.db')

#get dump of all NSE instruments
instrument_df = getInstrumentDump("NSE")
instrument_nfo= getInstrumentDump("NFO")

def create_tables(instruments):
    c=db.cursor()
    for i in instruments:
        c.execute("CREATE TABLE IF NOT EXISTS {} (ts datetime primary key,price real(15,5), volume integer)".format(i))
    try:
        db.commit()
    except:
        db.rollback()

def insert_ticks(ticks,instruments):
    getInstrumentTokenDict= getInstrumentTokenMap(instruments,instrument_nfo)
    c=db.cursor()
    for tick in ticks:
        try:
           # tok = "TOKEN"+str(tick['instrument_token'])
            vals = [tick['timestamp'],tick['last_price'], tick['last_quantity']]
            query = "INSERT INTO {}(ts,price,volume) VALUES (?,?,?)".format(getInstrumentTokenDict[tick['instrument_token']])
            c.execute(query,vals)
        except:
            pass
    try:
        db.commit()
    except:
        db.rollback()    

def dbclose():
    if db:
        db.close()
        

def resampledata(instrument):
    data = pd.read_sql('''SELECT * FROM %s WHERE ts >=  date() - '1 min';''' %instrument, con=db)                
    data = data.set_index(['ts'])
    data.index = pd.to_datetime(data.index)
    ticks = data.loc[:, ['price']]   
    df=ticks['price'].resample('1min').ohlc().dropna()
    return df
        