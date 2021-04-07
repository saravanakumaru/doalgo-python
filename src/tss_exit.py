#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 15:33:00 2020

@author: saravana.kumar
"""



import pandas as pd
import datetime
import sqlite3 as lite

from save_ticks import resampledata
from placing_orders import placeMarketOrderForAnExchange
from kiteconnect import KiteConnect
from datetime import timedelta

access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#list_of_instruments=list(tss.getInstrumentTokenDict)
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
        price_dict = dict(zip(data.STRIKE, data.AVG_PRICE))
        print(data)
        print(price_dict)
        return price_dict
    except Exception as e: 
        print(e)
        print('ERR')
        #sys.exit(1)
    finally:
        if db:
            db.close()
    
def get_instrument_qty_dict(date):
      
    db = None

    try:
        db = lite.connect('/Users/saravana.kumar/algo.db')
        sql = """select ID,STRIKE,AVG_PRICE,QTY,DATE
         from TSS_SELL
         where DATE = {0} """
        sql=sql.format('?') 
        print(sql)
        data = pd.read_sql(sql,con=db,params={date})  
        qty_dict = dict(zip(data.STRIKE, data.QTY))
        print(data)
        print(qty_dict)
        return qty_dict
    except Exception as e: 
        print(e)
        print('ERR')
        #sys.exit(1)
    finally:
        if db:
            db.close()
    

date_param=(datetime.date.today()-timedelta(1)).strftime('%y-%m-%d')
print(date_param)

list_of_instruments=get_instrument_price_dict(date_param)
for instrument_key in list_of_instruments:
    df=resampledata(instrument_key)
    close_value=df.tail(1).close.values[0]
    print(instrument_key+":"+str(close_value))
    fifty_percent_value=0.5*list_of_instruments[instrument_key] + list_of_instruments[instrument_key]
    print(instrument_key+":SL->"+str(fifty_percent_value))
    if close_value >= fifty_percent_value:
        qty_dict=get_instrument_qty_dict(date_param)
        quantity=qty_dict[instrument_key]
        print(quantity)
        #placeMarketOrderForAnExchange(instrument_key,'buy',quantity,kite.EXCHANGE_NFO)
        print('Time to Exit the leg')
     
              
    