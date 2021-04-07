#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 20:41:11 2020

@author: saravana.kumar
"""

import math

def roundToNSEPrice(price):
  x = round(price, 2) * 20
  y = math.ceil(x)
  return y / 20


def round_nearest(x,num=50):
    return int(round(float(x)/num)*num)

def tokenLookup(instrument_df,symbol_list):
    token_list = []
    for symbol in symbol_list:
        token_list.append(int(instrument_df[instrument_df.tradingsymbol==symbol].instrument_token.values[0]))
    return token_list



