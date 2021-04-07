#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan  9 12:38:25 2021

@author: saravana.kumar
"""
import pandas as pd

def string_a(string):
    dict_string={}
    for chars in string:
        dict_string[chars]=string.count(chars)
    print(dict_string)    
        

pets = ('cats','dogs','cats','dogs','cats','cats')
totalcount=len(pets)
print(totalcount)
count_cats=pets.count('cats')
print(count_cats)
if ((count_cats / totalcount) > 0.5):
    print("more cats")
else:
    print("none")    
string_a('Pythonn')

a={'P': 1, 'y': 1, 't': 1}
b={'h': 1, 'o': 1, 'n': 2}
print(a.update(b))
print(a)


df = pd.DataFrame({"A":[12, 4, 5, 44, 1], 
                   "B":[5, 2, 54, 3, 2], 
                   "C":[20, 16, 7, 3, 8],  
                   "D":[14, 3, 17, 2, 6]}) 
  
# Print the dataframe 
df_pending = df[(df['A']< 10) & (df['C']<10)]