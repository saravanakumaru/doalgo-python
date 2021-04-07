#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 21:59:59 2021

@author: saravana.kumar
"""

import sys
sys.path.append("/Users/saravana.kumar/opt/anaconda3/envs/algo/lib/python3.8/site-packages")
import pandas as pd
import os




from kiteconnect import KiteConnect

cwd = os.chdir("/Users/saravana.kumar/Downloads/Personal/doalgo/zerodha/")

access_token = open("access_token.txt",'r').read()
key_secret = open("api_key.txt",'r').read().split()
kite = KiteConnect(api_key=key_secret[0])
kite.set_access_token(access_token)


    
"""
We can just use the order data frame and position date frame to itereate and identify the  
pending orders to check the count if its still there or cancelled if cancelled we can just 
exit the positions with just firing a Market order

"""
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

#pos_df,ord_df
def closeBuyHedgePosition(pos_df_nfo):
         pos_df_nfo_copy = pos_df_nfo.copy()
         for i in range(len(pos_df_nfo_copy)):
              print(f"value of i is {i}")
              ticker = pos_df_nfo_copy["tradingsymbol"].values[i]
              quantity = pos_df_nfo_copy["quantity"].values[i]
              indexv = pos_df_nfo_copy["tradingsymbol"].index
              print(f"index value is {indexv}")
              last_2_chars = ticker[-2:]
              print(f"the last two characters for {ticker} is {last_2_chars}")
              pos_df_nfo_copy.loc[pos_df_nfo_copy["tradingsymbol"] == ticker,"type"] = last_2_chars
              if quantity < 0 :
                       pos_df_nfo_copy.loc[pos_df_nfo_copy["tradingsymbol"] == ticker,"status"] = "sell"
              elif quantity > 0:
                       pos_df_nfo_copy.loc[pos_df_nfo_copy["tradingsymbol"] == ticker,"status"] = "buy"
              else:
                       pos_df_nfo_copy.loc[pos_df_nfo_copy["tradingsymbol"] == ticker,"status"] = "exit"
                       
         pe_exit_list = pos_df_nfo_copy[(pos_df_nfo_copy['status'] == "exit") & (pos_df_nfo_copy['type'] == "PE")]["tradingsymbol"].tolist()
         ce_exit_list = pos_df_nfo_copy[(pos_df_nfo_copy['status'] == "exit") & (pos_df_nfo_copy['type'] == "CE")]["tradingsymbol"].tolist()
         if (len(pe_exit_list) == 2):
             print("condition set to close PE buy position")
             pe_buy_trading_symbol = pos_df_nfo_copy[(pos_df_nfo_copy['status'] == "buy") & (pos_df_nfo_copy['type'] == "PE")]["tradingsymbol"]
             pe_buy_trading_quantity = pos_df_nfo_copy[(pos_df_nfo_copy['status'] == "buy") & (pos_df_nfo_copy['type'] == "PE")]["quantity"]
             placeMarketOrder(pe_buy_trading_symbol,"sell", pe_buy_trading_quantity,kite.EXCHANGE_NFO)
         if (len(ce_exit_list) == 2):    
             print("condition set to close PE buy position")
             ce_buy_trading_symbol = pos_df_nfo_copy[(pos_df_nfo_copy['status'] == "buy") & (pos_df_nfo_copy['type'] == "CE")]["tradingsymbol"]
             ce_buy_trading_quantity = pos_df_nfo_copy[(pos_df_nfo_copy['status'] == "buy") & (pos_df_nfo_copy['type'] == "CE")]["quantity"]
             placeMarketOrder(ce_buy_trading_symbol,"sell", ce_buy_trading_quantity,kite.EXCHANGE_NFO) 


pos_df = pd.DataFrame(kite.positions()["day"])
pos_df_nfo = pos_df[pos_df['exchange']==kite.EXCHANGE_NFO] 
ord_df = pd.DataFrame(kite.orders())

for i in range(len(pos_df_nfo)):
    ticker = pos_df_nfo["tradingsymbol"].values[i]
    quantity = abs(pos_df_nfo["quantity"].values[i])
    order_status_list = ord_df[(ord_df['status'].isin(["TRIGGER PENDING"])) & (ord_df['tradingsymbol'] == ticker)]["order_id"].tolist()
    order_status_count = len(order_status_list)
    print(f"Order status count for {ticker} at the moment is {order_status_count} and {quantity}")
    if order_status_count == 0 and quantity > 0 :
        print(f"Order status count for {ticker} at the moment looks changed so we need to exit the positions")
    #     if (pos_df_nfo["quantity"].values[i] >0 and pos_df_nfo["product"].values[i] == kite.PRODUCT_MIS):
    #         quantity = pos_df_nfo["quantity"].values[i]
    #         print(f"Quantities for sell to be placed {quantity}")
    #         placeMarketOrderForAnExchange(ticker,"sell", quantity,kite.EXCHANGE_NFO)
    #     if (pos_df_nfo["quantity"].values[i] <0 and pos_df_nfo["product"].values[i] == kite.PRODUCT_MIS):
    #         quantity = abs(pos_df_nfo["quantity"].values[i])
    #         print(f"Quantities for buy to be placed {quantity}")
    #         placeMarketOrderForAnExchange(ticker,"buy", quantity,kite.EXCHANGE_NFO)

