#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 20:47:07 2020

@author: saravana.kumar
"""

from kiteconnect import KiteConnect
import os
import pandas as pd


#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


def CancelOrder(order_id):    
    # Modify order given order id
    kite.cancel_order(order_id=order_id,variety='co') 
    
a,b = 0,0
while a < 10:
    try:
        pos_df = pd.DataFrame(kite.positions()["day"])
        break
    except:
        print("can't extract position data..retrying")
        a+=1
while b < 10:
    try:
        ord_df = pd.DataFrame(kite.orders())
        break
    except:
        print("can't extract order data..retrying")
        b+=1

pending = ord_df[ord_df['status'].isin(["TRIGGER PENDING","OPEN"])]["order_id"].tolist()
# drop = []
# attempt = 0
# while len(pending)>0 and attempt<5:
#     pending = [j for j in pending if j not in drop]
#     for order in pending:
#         try:
#             CancelOrder(order)
#             drop.append(order)
#         except:
#             print("unable to delete order id : ",order)
#             attempt+=1