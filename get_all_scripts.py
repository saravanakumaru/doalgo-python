#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 15:57:23 2020

@author: saravana.kumar
"""

from kiteconnect import KiteConnect
import logging
import os
import pandas as pd

cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")

#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


instrument_dump = kite.instruments('NSE')
instrument_df = pd.DataFrame(instrument_dump)

values=instrument_df[instrument_df.tradingsymbol=='INFY'].instrument_token.values[0]



  
