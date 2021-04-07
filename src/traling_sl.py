#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:41:07 2021

@author: saravana.kumar
"""

import sys
sys.path.append("/Users/saravana.kumar/opt/anaconda3/envs/algo/lib/python3.8/site-packages")
import logging
import os
import pandas as pd
import datetime

from kiteconnect import KiteConnect

cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")
#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

'''
get the orders for the list of instruments passed 
get the trail points and sl trail points modify points
get the positions and get the entry price 
get the curretn LTP for the instrument 
if LTP - entry is positive and >= trail points 
    modify the order for by changing the price to price + sl trail points
'''


def instrumentLastPriceExtractor(instrumentlist,lookupinstrument):
    ltp = kite.ltp(instrumentlist).get(lookupinstrument).get('last_price')
    return ltp

def trail_stop_losses(tradingsymbols,instrument,trail_points,trail_price):
    print("coming in to trail profit method")
    b=0
    while b < 10:
        try:
            ord_df = pd.DataFrame(kite.orders())
            break
        except:
            print("can't extract order data..retrying")
            b+=1
            
    df_trailing_symbols_temp = ord_df[(ord_df['tradingsymbol'].isin(tradingsymbols)) & (ord_df['status'].isin(["TRIGGER PENDING"]))]      
    df_trailng_symbols = df_trailing_symbols_temp[['order_id','variety','exchange','tradingsymbol','order_type','product','quantity','price','trigger_price']]
    for index, row in df_trailng_symbols.iterrows(): 
        if(row["tradingsymbol"] == instrument):
            print (row["order_id"], row["price"],row['trigger_price'],row['tradingsymbol']) 
            # kite.modify_order(variety=row['variety'],
            #               order_id=row['order_id'],
            #               trigger_price = row['trigger_price'] - trail_price)
        

a,b = 0,0
while a < 10:
    try:
        pos_df = pd.DataFrame(kite.positions()["day"])
        break
    except Exception as e:
        print("can't extract position data..retrying"+ e)
        a+=1


pos_df_nfo = pos_df[pos_df['exchange']==kite.EXCHANGE_NFO] 
pos_df_nfo['instrument_name_with_exchange'] = pos_df_nfo.apply(lambda x :'%s%s%s' % (x['exchange'],':',x['tradingsymbol']),axis=1)
pos_df_nfo_entry_price = pos_df_nfo[['tradingsymbol','average_price','instrument_name_with_exchange']]
list_of_instruments_with_exchange = pos_df_nfo_entry_price['instrument_name_with_exchange'].tolist()
list_of_trading_symbols = pos_df_nfo_entry_price['tradingsymbol'].tolist()
# df_trailing_symbols_temp_list = order_df[(order_df['tradingsymbol'].isin(list_of_trading_symbols)) & (order_df['status'].isin(["TRIGGER PENDING"]))]['tradingsymbol'].tolist()

for instrument in list_of_instruments_with_exchange:
    ltp_of_instrument = instrumentLastPriceExtractor(list_of_instruments_with_exchange,instrument)
    print(f"{instrument},{ltp_of_instrument}")
    instrument_token = instrument.split(":")[1]
    print(instrument_token)
    average_price = pos_df_nfo[pos_df_nfo['tradingsymbol'] == instrument_token].average_price.values[0]
    print(average_price)
    if (ltp_of_instrument <= (average_price - 15)):
        trail_stop_losses(list_of_trading_symbols,instrument_token,15,5)
        
        