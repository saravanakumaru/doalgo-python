#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  8 20:13:44 2020

@author: saravana.kumar
"""

import sys
sys.path.append("/Users/saravana.kumar/opt/anaconda3/envs/algo/lib/python3.8/site-packages")
import logging
import os
import pandas as pd
import datetime
import time

from algo_utils import round_nearest
from algo_database_connector import createTableRecord
from getinstruments import getInstrumentDump
from getinstruments import getInstrumentTradingSymbolForExpiry
from placing_orders import placeMarketOrderForAnExchange,placeSLMarketOrderForAnExchange
from kiteconnect import KiteConnect
from datetime import date

logging.getLogger('').handlers = []

logging.basicConfig(
    filename = "tss.log",
    filemode="w",
    level = logging.INFO)

cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)

#get dump of all NSE instruments
instrument_df = getInstrumentDump("NSE")
instrument_nfo= getInstrumentDump("NFO")

#TOS Strategy 
#1 lot of ATM calculate the ATM by getting the current LTP of Nifty 

tickers = ["NIFTY 50"]
ltplist=["NSE:NIFTY 50","NSE:INFY"]
buy_flag = False

def tokenLookup(instrument_df,symbol_list):
    token_list = []
    for symbol in symbol_list:
        token_list.append(int(instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]))
    return token_list

def instrumentLastPriceExtractor(instrumentlist,lookupinstrument):
    ltp = kite.ltp(instrumentlist).get(lookupinstrument).get('last_price')
    return ltp

#tokenlist=tokenLookup(instrument_df,tickers)
#print(tokenlist[0])

ltp=instrumentLastPriceExtractor(ltplist,"NSE:NIFTY 50")
rounded_ltp = round_nearest(ltp)
print(round_nearest(ltp))
print(f"Nifty Tradig at the strike {ltp} decided to trade ATM {rounded_ltp}")
logging.info("Nifty Tradig at the strike %f decided to trade ATM %f",ltp,rounded_ltp)

# instrument_type,expiry,strike
currentDay = date.today().day
currentMonth = date.today().month
currentYear = date.today().year
print(f"{currentDay},{currentMonth},{currentYear}")
strikeCE=getInstrumentTradingSymbolForExpiry(instrument_nfo,currentYear,currentMonth,currentDay,"NIFTY","CE",rounded_ltp)
strikePE=getInstrumentTradingSymbolForExpiry(instrument_nfo,currentYear,currentMonth,currentDay,"NIFTY","PE",rounded_ltp)

strike_strangleCE=getInstrumentTradingSymbolForExpiry(instrument_nfo,currentYear,currentMonth,currentDay,"NIFTY","CE",rounded_ltp+50)
strike_stranglePE=getInstrumentTradingSymbolForExpiry(instrument_nfo,currentYear,currentMonth,currentDay,"NIFTY","PE",rounded_ltp-50)

global table_list_tss;
global getInstrumentTokenDict;

#we can take the position here 
#we create the table and start storing the ticks in there and 
table_list_tss=[strikeCE,strikePE,strike_strangleCE,strike_stranglePE]
print(table_list_tss)
#Entry done - lets complete the entry first and wait for 10 secs and place the SL order 
for strike in table_list_tss:
    print(strike)
    quantity = 75
    entry_price = 0
    if table_list_tss.index(strike)>1:
        quantity = 150
    placeMarketOrderForAnExchange(strike,'sell',quantity,kite.EXCHANGE_NFO)
    
#letting the market to finish taking our orders    
print("Entry completed for all the legs we will sleep for 10 secs from here and will set up stop loss orders")
time.sleep(15)   

if buy_flag:
    strike_strangle_buy_CE=getInstrumentTradingSymbolForExpiry(instrument_nfo,currentYear,currentMonth,currentDay,"NIFTY","CE",rounded_ltp+300)
    strike_strangle_buy_PE=getInstrumentTradingSymbolForExpiry(instrument_nfo,currentYear,currentMonth,currentDay,"NIFTY","PE",rounded_ltp-300)
    buy_strike_list = [strike_strangle_buy_CE,strike_strangle_buy_PE]
    for strike in buy_strike_list:
        quantity = 150
        placeMarketOrderForAnExchange(strike,'buy',quantity,kite.EXCHANGE_NFO)
    time.sleep(10)  
        
#['NIFTY21FEB15150CE', 'NIFTY21FEB15150PE', 'NIFTY21FEB15200CE', 'NIFTY21FEB15100PE']        
# here we will be taking up the SL postitions 
pos_df = pd.DataFrame(kite.positions()["day"])
pos_df_nfo = pos_df[pos_df['exchange']==kite.EXCHANGE_NFO] 
for strike in table_list_tss:

    entry_price=0;
    if len(pos_df_nfo.index) == 0:
        logging.error('UNABLE TO TAKE POSITIONS.. SOME ERROR HAPPENED BREAKING THE AUTO ENTRY')
        break
    elif len(pos_df_nfo.index) > 0:
        entry_price=pos_df_nfo[pos_df_nfo['tradingsymbol']==strike]['average_price'].values[0] 
    sl_price_tss = (0.5 * entry_price) + entry_price
    sl_price_tss = round((sl_price_tss - (sl_price_tss % 0.05)),2) # we are converting the price to multiples of .05 other wise zerodha might throw error
    quantity = abs(pos_df_nfo[pos_df_nfo['tradingsymbol']==strike]['quantity'].values[0])
    print(f"Quantity to place stop loss order for {strike} is {quantity}")
    placeSLMarketOrderForAnExchange(strike,'buy',quantity,sl_price_tss,kite.EXCHANGE_NFO)
    today=datetime.date.today().strftime('%y-%m-%d')
    createTableRecord('TSS_SELL', 'STRIKE,AVG_PRICE,QTY,DATE', [strike,entry_price,quantity,today]) 
print("Entry and SL set up completed for all the legs")    

# table_list_tss = ['NIFTY21FEB15150CE', 'NIFTY21FEB15150PE', 'NIFTY21FEB15200CE', 'NIFTY21FEB15100PE']   
# buy_strike_list = ['NIFTY21FEB15450CE', 'NIFTY21FEB15450PE',] 
# with open('/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/TSS_today_positions.txt', 'a') as fd:
#     for strike in table_list_tss:
#         fd.write(f"{strike},sell")
#         fd.write("\n")
#     for strike in buy_strike_list:
#         fd.write(f"{strike},buy")
#         fd.write("\n")
    
#create_tables(table_list_tss)	

