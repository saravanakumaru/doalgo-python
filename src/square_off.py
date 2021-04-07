#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 28 20:47:07 2020

@author: saravana.kumar
"""


import os
import sys
sys.path.append("/Users/saravana.kumar/opt/anaconda3/envs/algo/lib/python3.8/site-packages")

import pandas as pd
from kiteconnect import KiteConnect

cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")
#generate trading session
access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)
nifty_included = False


def placeMarketOrder(symbol,buy_sell,quantity,p_exchange):    
    # Place an intraday market order on NSE
    if buy_sell == "buy":
        t_type=kite.TRANSACTION_TYPE_BUY
    elif buy_sell == "sell":
        t_type=kite.TRANSACTION_TYPE_SELL
    kite.place_order(tradingsymbol=symbol,
                    exchange=p_exchange,
                    transaction_type=t_type,
                    quantity=quantity,
                    order_type=kite.ORDER_TYPE_MARKET,
                    product=kite.PRODUCT_MIS,
                    variety=kite.VARIETY_REGULAR)
    
def CancelOrder(order_id,order_variety):    
    # Modify order given order id
    kite.cancel_order(order_id=order_id,
                    variety=order_variety)  


#fetching orders and position information   
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


# closing all pending orders
pending = ord_df[ord_df['status'].isin(["TRIGGER PENDING","OPEN"])]["order_id"].tolist()
drop = []
attempt = 0
while len(pending)>0 and attempt<5:
    pending = [j for j in pending if j not in drop]
    for order in pending:
        try:
            order_variety = ord_df[ord_df['order_id']== order]['variety'].values[0]
            print(f"Order id is {order} and order Variety is {order_variety}")
            CancelOrder(order,order_variety)
            drop.append(order)
        except:
            print("unable to delete order id : ",order)
            attempt+=1
            
#closing all open position      
for i in range(len(pos_df)):
    ticker = pos_df["tradingsymbol"].values[i]
    exchange = kite.EXCHANGE_NSE
    if nifty_included:
        checker_list = ["NIFTY"]
        if len(ticker) > 5 and ticker[0:5] in checker_list:
            exchange = kite.EXCHANGE_NFO
    print(f"Going to close position for {ticker} in {exchange}")
    if (pos_df["quantity"].values[i] >0 and pos_df["product"].values[i] == kite.PRODUCT_MIS):
        quantity = pos_df["quantity"].values[i]
        print(f"Quantities for sell to be placed {quantity}")
        placeMarketOrder(ticker,"sell", quantity,exchange)
    if (pos_df["quantity"].values[i] <0 and pos_df["product"].values[i] == kite.PRODUCT_MIS):
        quantity = abs(pos_df["quantity"].values[i])
        print(f"Quantities for buy to be placed {quantity}")
        placeMarketOrder(ticker,"buy", quantity,exchange)

       