#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 12:31:07 2021

@author: saravana.kumar
"""
import pandas as pd


def monkey_smile(no1,no2):
    bool1 = no1 and no2
    if (bool1) or not(bool1):
        print("you are in trouble")
    else:
        print("you are in safe")
        
monkey_smile(True,False)
df = pd.DataFrame({"A":[12, 4, 5, 44, 1], 
                   "B":[5, 2, 54, 3, 2], 
                   "C":[20, 16, 7, 3, 8],  
                   "D":[14, 3, 17, 2, 6]}) 
print(df)
avg_candle_size = abs(df['A'] - df['D']).median()
# value = abs(df['close'] - df['open']) <= ( 0.05 * avg_candle_size)


   
