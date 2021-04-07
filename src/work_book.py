#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 12:53:27 2021

@author: saravana.kumar
"""
import datetime
from functools import reduce
from collections import Counter
from datetime import timedelta
class Bitcoin():
    __bitcoin_price_today=100
    
    def __init__(self):
        self.a=0
        
    def buy_bitcoin(self,amount):
        no_of_bitcoints = amount / self.__bitcoin_price_today 
        self.a += no_of_bitcoints
        
    def sell_bit_coins(self,amount):
        print(f"current available bit coin quantity {self.a}")
        no_of_bitcoints = amount / self.__bitcoin_price_today 
        self.a -= no_of_bitcoints
    def display_bit_coin(self):
        print(f"current available bit coin quantity {self.a}")
        
            
def main():
    bitcoin = Bitcoin()
    bitcoin.buy_bitcoin(1000)
    bitcoin.display_bit_coin()
    bitcoin.sell_bit_coins(500)
    bitcoin.display_bit_coin()
    
if __name__  ==   "__main__":
    main()
    
    
def monkey_smile(monkeya_smile, monkeyb_smile):
    return (monkeya_smile and monkeyb_smile) or not (monkeya_smile or monkeyb_smile)    


print(monkey_smile(True,True))
print(monkey_smile(True,False))
print(monkey_smile(False,True))
print(monkey_smile(False,False))




square_of = lambda x:(x * x)
list_my = [1,2,3,4,5,6,7,8,9]
print(list(map(square_of,list_my)))


square_of = filter(lambda x: (x % 2 ==0),list_my)
print(list(square_of))

square_of = reduce(lambda x: (x % 2 ==0),list_my)
print(list(square_of))

String_1 = "madam"
String_2 = "madam"   
txt = String_1[::-1]
if String_2 == txt and len(String_2) == len(txt):
    print("Anagram")
else:
    print('not Anagram')    
    
try:
    print("some_variable")
except Exception as e: 
    print(e)
    print('ERR')
        #sys.exit(1)
finally:
    print("finally")
    
package_enumerator = lambda package_name:dir(package_name)
print(list(map(package_enumerator,".")))
    

with open('a.txt', 'w') as file:
    file.write("this is a test")
    
dt_now = datetime.datetime(2020,1,17,hour=9,minute=15)
print(dt_now)
date_param=(dt_now+timedelta(hours=6,minutes=15))
print (date_param)