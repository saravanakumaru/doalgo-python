#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 17:44:26 2020

@author: saravana.kumar
"""
from kiteconnect import KiteTicker, KiteConnect
from datetime import date

import datetime
import sys
import pandas as pd
import os


cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


def getInstrumentDump(exchange):
    #get dump of all instruments of exchange
    instrument_dump = kite.instruments(exchange)
    instrument_df = pd.DataFrame(instrument_dump)
    return instrument_df

def getInstrumentTradingSymbolForExpiry(instrument_nfo,year,month,day,name,instrument_type,strike):
    date_from = pd.Timestamp(date(year,month,day))
    thisweekinstruments=instrument_nfo[instrument_nfo.expiry==date_from]
    strike=thisweekinstruments[(thisweekinstruments.name==name)&(thisweekinstruments.instrument_type==instrument_type)&(thisweekinstruments.strike==strike)].tradingsymbol.values[0]
    return strike                                    

def getInstrumentTokenMap(instrument_trading_symbols,instrument_nfo):
    d={}
    for instrument_trading_symbol in instrument_trading_symbols:
        key=instrument_nfo[(instrument_nfo.tradingsymbol==instrument_trading_symbol)].instrument_token.values[0]
        d.update({key:instrument_trading_symbol})
    return d                                    


#get dump of all NSE instruments
#instrument_df = getInstrumentDump("NSE")
#instrument_nfo= getInstrumentDump("NFO")
#strikeCE=getInstrumentTradingSymbolForExpiry(instrument_nfo,2020,12,30,"NIFTY","CE",13750)    